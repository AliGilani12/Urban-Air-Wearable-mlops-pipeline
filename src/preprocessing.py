"""
Data preprocessing utilities
"""
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.model_selection import train_test_split


def augment_health_data(df: pd.DataFrame, augmentation_factor: int = 2, random_state: int = 42):
    """
    Augment health data by adding synthetic samples with small random variations
    This helps increase training data when dataset is small
    
    Args:
        df: Input DataFrame
        augmentation_factor: How many times to augment (2 = double the data)
        random_state: Random seed
    
    Returns:
        Augmented DataFrame
    """
    np.random.seed(random_state)
    augmented_dfs = [df.copy()]
    
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    # Exclude ID columns and encoded target
    exclude_cols = ['Record_ID', 'Activity_Status_Encoded', 'Secure_Transmission_Status']
    numeric_cols = [col for col in numeric_cols if col not in exclude_cols]
    
    for _ in range(augmentation_factor - 1):
        augmented = df.copy()
        for col in numeric_cols:
            if col in augmented.columns:
                # Add small Gaussian noise (5% of std)
                std = augmented[col].std()
                noise = np.random.normal(0, std * 0.05, size=len(augmented))
                augmented[col] = augmented[col] + noise
                # Clip to reasonable ranges
                if 'Heart_Rate' in col:
                    augmented[col] = augmented[col].clip(60, 200)
                elif 'Step_Count' in col:
                    augmented[col] = augmented[col].clip(0, 1000)
                elif 'Body_Temperature' in col:
                    augmented[col] = augmented[col].clip(36.0, 38.0)
                elif 'Blood_Oxygen' in col:
                    augmented[col] = augmented[col].clip(90, 100)
        
        augmented_dfs.append(augmented)
    
    return pd.concat(augmented_dfs, ignore_index=True)


def preprocess_air_pollution_data(df: pd.DataFrame, test_size: float = 0.2, random_state: int = 42):
    """
    Preprocess air pollution dataset for modeling
    
    Args:
        df: Input DataFrame
        test_size: Proportion of test set
        random_state: Random seed
    
    Returns:
        X_train, X_test, y_train, y_test, scaler
    """
    # Convert DateTime to datetime
    df['DateTime'] = pd.to_datetime(df['DateTime'])
    
    # Extract temporal features
    df['Hour'] = df['DateTime'].dt.hour
    df['DayOfWeek'] = df['DateTime'].dt.dayofweek
    df['Month'] = df['DateTime'].dt.month
    
    # Select features (exclude DateTime, Station_ID, and target)
    feature_cols = [
        'PM2.5', 'PM10', 'NO₂', 'SO₂', 'CO', 'O₃',
        'Temp_C', 'Humidity_%', 'Wind_Speed_mps', 
        'Wind_Direction_deg', 'Pressure_hPa', 'Rain_mm',
        'Hour', 'DayOfWeek', 'Month'
    ]
    
    # Handle missing values
    df[feature_cols] = df[feature_cols].fillna(df[feature_cols].mean())
    
    X = df[feature_cols]
    y = df['AQI_Target']
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state
    )
    
    # Scale features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    return X_train_scaled, X_test_scaled, y_train, y_test, scaler


def preprocess_health_data(df: pd.DataFrame, test_size: float = 0.2, random_state: int = 42, augment_data: bool = True):
    """
    Preprocess wearable sports health dataset for modeling
    
    Args:
        df: Input DataFrame
        test_size: Proportion of test set
        random_state: Random seed
    
    Returns:
        X_train, X_test, y_train, y_test, scaler, label_encoder
    """
    # Convert Timestamp to datetime and sort by timestamp for temporal analysis
    df['Timestamp'] = pd.to_datetime(df['Timestamp'])
    df = df.sort_values(['Athlete_ID', 'Timestamp']).reset_index(drop=True)
    
    # Extract temporal features
    df['Hour'] = df['Timestamp'].dt.hour
    df['DayOfWeek'] = df['Timestamp'].dt.dayofweek
    df['Minute'] = df['Timestamp'].dt.minute
    
    # TEMPORAL PATTERNS: Calculate time differences and activity duration
    df['Time_Diff'] = df.groupby('Athlete_ID')['Timestamp'].diff().dt.total_seconds() / 60  # minutes
    df['Time_Diff'] = df['Time_Diff'].fillna(5.0)  # Default 5 minutes if first record
    
    # Calculate rolling averages for temporal patterns (last 3 measurements)
    df['HR_Rolling_Mean'] = df.groupby('Athlete_ID')['Heart_Rate'].transform(lambda x: x.rolling(window=3, min_periods=1).mean())
    df['Steps_Rolling_Mean'] = df.groupby('Athlete_ID')['Step_Count'].transform(lambda x: x.rolling(window=3, min_periods=1).mean())
    df['HR_Change'] = df.groupby('Athlete_ID')['Heart_Rate'].diff().fillna(0)
    df['Steps_Change'] = df.groupby('Athlete_ID')['Step_Count'].diff().fillna(0)
    
    # GPS SPEED: Calculate speed from location changes (meters per minute)
    # Using Haversine formula approximation for distance
    df['Lat_Change'] = df.groupby('Athlete_ID')['Latitude'].diff().fillna(0)
    df['Lon_Change'] = df.groupby('Athlete_ID')['Longitude'].diff().fillna(0)
    # Approximate distance (degrees to meters: ~111,000 meters per degree)
    df['Distance_Moved'] = np.sqrt(df['Lat_Change']**2 + df['Lon_Change']**2) * 111000  # meters
    df['GPS_Speed'] = df['Distance_Moved'] / (df['Time_Diff'] + 0.1)  # meters per minute
    df['GPS_Speed'] = df['GPS_Speed'].fillna(0)
    
    # Activity duration proxy (time since last measurement)
    df['Activity_Duration'] = df['Time_Diff']
    
    # Parse Blood_Pressure (format: "systolic/diastolic")
    df[['BP_Systolic', 'BP_Diastolic']] = df['Blood_Pressure'].str.split('/', expand=True).astype(float)
    
    # Feature Engineering: Create interaction features and ratios
    df['HR_to_Steps_Ratio'] = df['Heart_Rate'] / (df['Step_Count'] + 1)  # Heart rate per step
    df['BP_Ratio'] = df['BP_Systolic'] / (df['BP_Diastolic'] + 1)  # BP ratio
    df['HR_Temp_Interaction'] = df['Heart_Rate'] * df['Body_Temperature']
    df['Steps_Oxygen_Interaction'] = df['Step_Count'] * df['Blood_Oxygen']
    df['HR_BP_Interaction'] = df['Heart_Rate'] * df['BP_Systolic']
    
    # More sophisticated feature engineering
    df['HR_Steps_Product'] = df['Heart_Rate'] * df['Step_Count']
    df['Oxygen_Temp_Ratio'] = df['Blood_Oxygen'] / (df['Body_Temperature'] + 1)
    df['BP_Pulse_Pressure'] = df['BP_Systolic'] - df['BP_Diastolic']
    
    # Create activity intensity indicator based on heart rate zones
    # Normal resting: 60-100, Light: 50-60% max (assume max ~200), Moderate: 60-70%, Vigorous: 70-85%
    df['HR_Zone'] = pd.cut(df['Heart_Rate'], 
                          bins=[0, 80, 120, 150, 200], 
                          labels=[0, 1, 2, 3]).astype(float)
    
    # Step count categories - more granular
    df['Step_Intensity'] = pd.cut(df['Step_Count'], 
                                 bins=[0, 400, 600, 750, 900, 1000], 
                                 labels=[0, 1, 2, 3, 4]).astype(float)
    
    # Heart rate variability proxy (using standard deviation of HR relative to mean)
    hr_mean = df['Heart_Rate'].mean()
    df['HR_Deviation'] = abs(df['Heart_Rate'] - hr_mean) / hr_mean
    
    # Combined intensity score
    df['Intensity_Score'] = (df['Heart_Rate'] / 200) * 0.5 + (df['Step_Count'] / 1000) * 0.5
    
    # DOMAIN KNOWLEDGE: Activity-specific rules and thresholds
    # Running: High HR, High Steps, High Speed
    df['Likely_Running'] = ((df['Heart_Rate'] > 130) & (df['Step_Count'] > 600) & (df['GPS_Speed'] > 10)).astype(int)
    
    # Walking: Moderate HR, Moderate Steps, Low-Moderate Speed
    df['Likely_Walking'] = ((df['Heart_Rate'] >= 80) & (df['Heart_Rate'] <= 120) & 
                            (df['Step_Count'] >= 400) & (df['Step_Count'] <= 800) & 
                            (df['GPS_Speed'] > 0) & (df['GPS_Speed'] < 50)).astype(int)
    
    # Cycling: High HR, Very High Steps, Very High Speed
    df['Likely_Cycling'] = ((df['Heart_Rate'] > 120) & (df['Step_Count'] > 650) & 
                            (df['GPS_Speed'] > 30)).astype(int)
    
    # Resting: Low HR, Low Steps, No/Low Speed
    df['Likely_Resting'] = ((df['Heart_Rate'] < 100) & (df['Step_Count'] < 500) & 
                           (df['GPS_Speed'] < 5)).astype(int)
    
    # Activity intensity based on domain knowledge
    df['Activity_Intensity'] = 0  # Default
    df.loc[(df['Heart_Rate'] < 100) & (df['Step_Count'] < 500), 'Activity_Intensity'] = 0  # Resting
    df.loc[(df['Heart_Rate'] >= 100) & (df['Heart_Rate'] < 130) & (df['Step_Count'] >= 500), 'Activity_Intensity'] = 1  # Light
    df.loc[(df['Heart_Rate'] >= 130) & (df['Heart_Rate'] < 160) & (df['Step_Count'] >= 600), 'Activity_Intensity'] = 2  # Moderate
    df.loc[(df['Heart_Rate'] >= 160) & (df['Step_Count'] >= 700), 'Activity_Intensity'] = 3  # Vigorous
    
    # Step rate (steps per minute) - important for activity classification
    df['Step_Rate'] = df['Step_Count'] / (df['Time_Diff'] + 0.1)
    df['Step_Rate'] = df['Step_Rate'].fillna(df['Step_Count'] / 5.0)  # Default 5 min window
    
    # Encode categorical features for target
    label_encoder = LabelEncoder()
    df['Activity_Status_Encoded'] = label_encoder.fit_transform(df['Activity_Status'])
    
    # Select features (excluding Activity_Status_Encoded to avoid data leakage)
    # Now includes temporal patterns, GPS speed, domain knowledge rules
    feature_cols = [
        # Base features
        'Heart_Rate', 'Step_Count', 'Body_Temperature', 'Blood_Oxygen',
        'Latitude', 'Longitude', 'BP_Systolic', 'BP_Diastolic',
        # Temporal patterns
        'Time_Diff', 'HR_Rolling_Mean', 'Steps_Rolling_Mean', 
        'HR_Change', 'Steps_Change', 'Activity_Duration',
        # GPS and movement
        'GPS_Speed', 'Distance_Moved', 'Step_Rate',
        # Domain knowledge rules
        'Likely_Running', 'Likely_Walking', 'Likely_Cycling', 'Likely_Resting',
        'Activity_Intensity',
        # Engineered features
        'HR_to_Steps_Ratio', 'BP_Ratio', 'BP_Pulse_Pressure',
        'HR_Temp_Interaction', 'HR_BP_Interaction',
        'HR_Zone', 'Step_Intensity', 'Intensity_Score',
        'Hour', 'Minute'
    ]
    
    # Handle missing values
    df[feature_cols] = df[feature_cols].fillna(df[feature_cols].mean())
    
    X = df[feature_cols]
    # Use Activity_Status as target (predicting activity from health metrics)
    y = df['Activity_Status_Encoded']
    
    # Split data FIRST (before augmentation to avoid data leakage)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state, stratify=y
    )
    
    # DATA AUGMENTATION: Only augment training data, not test data
    if augment_data and len(X_train) < 1000:
        print(f"Augmenting training data from {len(X_train)} to {len(X_train) * 3} samples...")
        train_df = pd.DataFrame(X_train, columns=feature_cols)
        train_df['Activity_Status_Encoded'] = y_train.values
        augmented_train = augment_health_data(train_df, augmentation_factor=3, random_state=random_state)
        X_train = augmented_train[feature_cols].values
        y_train = augmented_train['Activity_Status_Encoded'].values
        print(f"Augmented training data shape: {X_train.shape}")
    
    # Scale features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    return X_train_scaled, X_test_scaled, y_train, y_test, scaler, label_encoder


if __name__ == "__main__":
    from src.data_loader import load_air_pollution_data, load_health_data
    from pathlib import Path
    
    base_path = Path(__file__).parent.parent
    
    # Test air pollution preprocessing
    print("Testing Air Pollution Preprocessing...")
    air_data = load_air_pollution_data(
        str(base_path / "Data" / "UrbanAirPollutionDataset.csv"),
        sample_size=1000
    )
    X_train, X_test, y_train, y_test, scaler = preprocess_air_pollution_data(air_data)
    print(f"Air Pollution - Train: {X_train.shape}, Test: {X_test.shape}")
    
    # Test health data preprocessing
    print("\nTesting Health Data Preprocessing...")
    health_data = load_health_data(
        str(base_path / "Data" / "wearable_sports_health_dataset.csv"),
        sample_size=1000
    )
    X_train, X_test, y_train, y_test, scaler, le = preprocess_health_data(health_data)
    print(f"Health Data - Train: {X_train.shape}, Test: {X_test.shape}")

