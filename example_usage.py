"""
Example usage script demonstrating the MLOps pipeline
"""
from pathlib import Path
from src.data_loader import load_air_pollution_data, load_health_data
from src.preprocessing import preprocess_air_pollution_data, preprocess_health_data
from src.train_models import train_air_pollution_model, train_health_model
import joblib
import numpy as np


def main():
    """Main example function"""
    base_path = Path(__file__).parent
    
    print("=" * 60)
    print("MLOps Project - Example Usage")
    print("=" * 60)
    
    # Example 1: Load and sample data
    print("\n1. Loading and sampling data...")
    air_data = load_air_pollution_data(
        str(base_path / "Data" / "UrbanAirPollutionDataset.csv"),
        sample_size=10000  # Increased to 10x for better model performance
    )
    health_data = load_health_data(
        str(base_path / "Data" / "wearable_sports_health_dataset.csv"),
        sample_size=500  # Using all available data
    )
    
    # Example 2: Preprocess data
    print("\n2. Preprocessing data...")
    X_train_air, X_test_air, y_train_air, y_test_air, scaler_air = preprocess_air_pollution_data(air_data)
    X_train_health, X_test_health, y_train_health, y_test_health, scaler_health, le_health = preprocess_health_data(health_data)
    
    print(f"   Air Pollution - Train: {X_train_air.shape}, Test: {X_test_air.shape}")
    print(f"   Health Data - Train: {X_train_health.shape}, Test: {X_test_health.shape}")
    
    # Example 3: Train models
    print("\n3. Training models...")
    train_air_pollution_model(sample_size=10000)  # Increased to 10x for better model performance
    train_health_model(sample_size=500)  # Using all available data
    
    # Example 4: Load and use trained models
    print("\n4. Loading trained models for prediction...")
    models_dir = base_path / "models"
    
    # Load air pollution model
    air_model = joblib.load(models_dir / "air_pollution_model.pkl")
    air_scaler = joblib.load(models_dir / "air_pollution_scaler.pkl")
    
    # Make a prediction on test data
    sample_pred = air_model.predict(X_test_air[:5])
    print(f"\n   Air Pollution Predictions (first 5 samples):")
    print(f"   Predicted AQI: {sample_pred}")
    print(f"   Actual AQI: {y_test_air.iloc[:5].values}")
    
    # Load health model
    health_model = joblib.load(models_dir / "health_activity_model.pkl")
    health_scaler = joblib.load(models_dir / "health_scaler.pkl")
    health_le = joblib.load(models_dir / "health_label_encoder.pkl")
    
    # Make a prediction on test data
    health_pred = health_model.predict(X_test_health[:5])
    print(f"\n   Health Activity Predictions (first 5 samples):")
    print(f"   Predicted Activity: {health_le.inverse_transform(health_pred)}")
    print(f"   Actual Activity: {health_le.inverse_transform(y_test_health.iloc[:5].values)}")
    
    print("\n" + "=" * 60)
    print("Example completed successfully!")
    print("=" * 60)


if __name__ == "__main__":
    main()

