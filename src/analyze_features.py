"""
Analyze feature importance and model performance
"""
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import accuracy_score

# Load data
df = pd.read_csv('Data/wearable_sports_health_dataset.csv')
df['Timestamp'] = pd.to_datetime(df['Timestamp'])
df['Hour'] = df['Timestamp'].dt.hour
df[['BP_Systolic', 'BP_Diastolic']] = df['Blood_Pressure'].str.split('/', expand=True).astype(float)

le = LabelEncoder()
y = le.fit_transform(df['Activity_Status'])

# Test different feature combinations
feature_sets = {
    'Basic': ['Heart_Rate', 'Body_Temperature', 'Blood_Oxygen', 'Step_Count'],
    'With BP': ['Heart_Rate', 'Body_Temperature', 'Blood_Oxygen', 'Step_Count', 'BP_Systolic', 'BP_Diastolic'],
    'All': ['Heart_Rate', 'Body_Temperature', 'Blood_Oxygen', 'Step_Count', 'BP_Systolic', 'BP_Diastolic', 'Hour']
}

for name, features in feature_sets.items():
    X = df[features]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    model = RandomForestClassifier(n_estimators=200, max_depth=15, min_samples_split=3, random_state=42, n_jobs=-1)
    model.fit(X_train_scaled, y_train)
    
    y_pred = model.predict(X_test_scaled)
    acc = accuracy_score(y_test, y_pred)
    
    print(f"\n{name} Features:")
    print(f"  Accuracy: {acc:.4f}")
    print(f"  Features: {features}")
    if name == 'All':
        print(f"  Feature Importances:")
        for i, feat in enumerate(features):
            print(f"    {feat}: {model.feature_importances_[i]:.4f}")

