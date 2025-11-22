"""
Data loading and sampling utilities
"""
import pandas as pd
import numpy as np
from pathlib import Path


def load_air_pollution_data(data_path: str, sample_size: int = 1000, random_state: int = 42):
    """
    Load and sample air pollution dataset
    
    Args:
        data_path: Path to the CSV file
        sample_size: Number of samples to take (default: 1000)
        random_state: Random seed for reproducibility
    
    Returns:
        DataFrame with sampled data
    """
    df = pd.read_csv(data_path)
    
    # Take a sample if dataset is larger than sample_size
    if len(df) > sample_size:
        df = df.sample(n=sample_size, random_state=random_state).reset_index(drop=True)
    
    print(f"Loaded {len(df)} samples from air pollution dataset")
    return df


def load_health_data(data_path: str, sample_size: int = 1000, random_state: int = 42):
    """
    Load and sample wearable sports health dataset
    
    Args:
        data_path: Path to the CSV file
        sample_size: Number of samples to take (default: 1000)
        random_state: Random seed for reproducibility
    
    Returns:
        DataFrame with sampled data
    """
    df = pd.read_csv(data_path)
    
    # Take a sample if dataset is larger than sample_size
    if len(df) > sample_size:
        df = df.sample(n=sample_size, random_state=random_state).reset_index(drop=True)
    
    print(f"Loaded {len(df)} samples from health dataset")
    return df


if __name__ == "__main__":
    # Example usage
    base_path = Path(__file__).parent.parent
    
    # Load air pollution data (using 10x samples for better model performance)
    air_data = load_air_pollution_data(
        str(base_path / "Data" / "UrbanAirPollutionDataset.csv"),
        sample_size=10000
    )
    print(f"Air Pollution Data Shape: {air_data.shape}")
    print(f"Air Pollution Data Columns: {air_data.columns.tolist()}")
    
    # Load health data (using all available data)
    health_data = load_health_data(
        str(base_path / "Data" / "wearable_sports_health_dataset.csv"),
        sample_size=500
    )
    print(f"\nHealth Data Shape: {health_data.shape}")
    print(f"Health Data Columns: {health_data.columns.tolist()}")

