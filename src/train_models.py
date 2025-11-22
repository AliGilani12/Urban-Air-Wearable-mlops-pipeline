"""
Model training scripts
"""
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier, GradientBoostingClassifier, VotingClassifier
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import mean_squared_error, r2_score, accuracy_score, classification_report
from sklearn.model_selection import cross_val_score
import joblib
try:
    from xgboost import XGBClassifier
    XGBOOST_AVAILABLE = True
except ImportError:
    XGBOOST_AVAILABLE = False
    print("XGBoost not available, using GradientBoostingClassifier instead")
from pathlib import Path
from src.data_loader import load_air_pollution_data, load_health_data
from src.preprocessing import preprocess_air_pollution_data, preprocess_health_data


def train_air_pollution_model(sample_size: int = 1000, random_state: int = 42):
    """
    Train a model to predict AQI from air pollution features
    
    Args:
        sample_size: Number of samples to use
        random_state: Random seed
    """
    print("=" * 50)
    print("Training Air Pollution Model")
    print("=" * 50)
    
    # Load and preprocess data
    base_path = Path(__file__).parent.parent
    df = load_air_pollution_data(
        str(base_path / "Data" / "UrbanAirPollutionDataset.csv"),
        sample_size=sample_size,
        random_state=random_state
    )
    
    X_train, X_test, y_train, y_test, scaler = preprocess_air_pollution_data(
        df, random_state=random_state
    )
    
    # Train model
    model = RandomForestRegressor(n_estimators=100, random_state=random_state, n_jobs=-1)
    model.fit(X_train, y_train)
    
    # Cross-validation for better performance estimate
    cv_scores = cross_val_score(model, X_train, y_train, cv=5, scoring='r2')
    print(f"\nCross-Validation R² Score (5-fold): {cv_scores.mean():.4f} (+/- {cv_scores.std() * 2:.4f})")
    
    # Evaluate on test set
    y_pred = model.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    
    print(f"\nTest Set Performance:")
    print(f"MSE: {mse:.4f}")
    print(f"R² Score: {r2:.4f}")
    print(f"RMSE: {np.sqrt(mse):.4f}")
    
    # Save model and scaler
    models_dir = base_path / "models"
    models_dir.mkdir(exist_ok=True)
    
    joblib.dump(model, models_dir / "air_pollution_model.pkl")
    joblib.dump(scaler, models_dir / "air_pollution_scaler.pkl")
    
    print(f"\nModel saved to {models_dir / 'air_pollution_model.pkl'}")
    print(f"Scaler saved to {models_dir / 'air_pollution_scaler.pkl'}")
    
    return model, scaler


def train_health_model(sample_size: int = 1000, random_state: int = 42):
    """
    Train a model to predict activity status from health metrics
    
    Args:
        sample_size: Number of samples to use
        random_state: Random seed
    """
    print("\n" + "=" * 50)
    print("Training Health Activity Model")
    print("=" * 50)
    
    # Load and preprocess data
    base_path = Path(__file__).parent.parent
    df = load_health_data(
        str(base_path / "Data" / "wearable_sports_health_dataset.csv"),
        sample_size=sample_size,
        random_state=random_state
    )
    
    X_train, X_test, y_train, y_test, scaler, label_encoder = preprocess_health_data(
        df, test_size=0.2, random_state=random_state
    )
    
    # Use XGBoost with optimized hyperparameters for maximum accuracy
    # Location features (Latitude/Longitude) are critical for good performance
    # Note: The dataset has limited discriminative power due to similar feature distributions
    # across activities, which limits achievable accuracy
    if XGBOOST_AVAILABLE:
        model = XGBClassifier(
            n_estimators=2000,
            max_depth=15,
            learning_rate=0.01,
            subsample=0.9,
            colsample_bytree=0.9,
            min_child_weight=1,
            gamma=0.0,
            reg_alpha=0.0,
            reg_lambda=0.5,
            scale_pos_weight=1,
            random_state=random_state,
            n_jobs=-1,
            eval_metric='mlogloss'
        )
        model.fit(X_train, y_train)
    else:
        # Use RandomForest with extensive tuning as fallback
        model = RandomForestClassifier(
            n_estimators=2000,
            max_depth=30,
            min_samples_split=2,
            min_samples_leaf=1,
            max_features='sqrt',
            bootstrap=True,
            random_state=random_state,
            n_jobs=-1
        )
        model.fit(X_train, y_train)
    
    model.fit(X_train, y_train)
    
    # Cross-validation for better performance estimate
    cv_scores = cross_val_score(model, X_train, y_train, cv=5, scoring='accuracy')
    print(f"\nCross-Validation Accuracy (5-fold): {cv_scores.mean():.4f} (+/- {cv_scores.std() * 2:.4f})")
    
    # Evaluate on test set
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    
    print(f"\nTest Set Performance:")
    print(f"Accuracy: {accuracy:.4f}")
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred, 
                                target_names=label_encoder.classes_))
    
    # Save model, scaler, and label encoder
    models_dir = base_path / "models"
    models_dir.mkdir(exist_ok=True)
    
    joblib.dump(model, models_dir / "health_activity_model.pkl")
    joblib.dump(scaler, models_dir / "health_scaler.pkl")
    joblib.dump(label_encoder, models_dir / "health_label_encoder.pkl")
    
    print(f"\nModel saved to {models_dir / 'health_activity_model.pkl'}")
    print(f"Scaler saved to {models_dir / 'health_scaler.pkl'}")
    print(f"Label Encoder saved to {models_dir / 'health_label_encoder.pkl'}")
    
    return model, scaler, label_encoder


if __name__ == "__main__":
    # Train both models with increased sample sizes (10x for air pollution)
    train_air_pollution_model(sample_size=10000)
    train_health_model(sample_size=500)  # Use all available data

