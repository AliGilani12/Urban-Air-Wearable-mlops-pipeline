# MLOps Project

This project implements a basic MLOps pipeline for two datasets:
1. **Urban Air Pollution Dataset** - Predicting Air Quality Index (AQI)
2. **Wearable Sports Health Dataset** - Predicting Activity Status from health metrics

## Project Structure

```
mlops-proj/
├── Data/                          # Raw data files
│   ├── UrbanAirPollutionDataset.csv
│   └── wearable_sports_health_dataset.csv
├── src/                           # Source code
│   ├── __init__.py
│   ├── data_loader.py            # Data loading and sampling utilities
│   ├── preprocessing.py          # Data preprocessing pipelines
│   └── train_models.py           # Model training scripts
├── models/                        # Trained models (generated)
├── notebooks/                     # Jupyter notebooks (optional)
├── data/processed/               # Processed data (optional)
├── requirements.txt              # Python dependencies
└── readme.md                     # This file
```

## Setup

1. Create a virtual environment (recommended):
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Load and Sample Data

```python
from src.data_loader import load_air_pollution_data, load_health_data

# Load air pollution data (samples 10,000 rows for better model performance)
air_data = load_air_pollution_data("Data/UrbanAirPollutionDataset.csv", sample_size=10000)

# Load health data (uses all available data - 500 rows)
health_data = load_health_data("Data/wearable_sports_health_dataset.csv", sample_size=500)
```

### Preprocess Data

```python
from src.preprocessing import preprocess_air_pollution_data, preprocess_health_data

# Preprocess air pollution data
X_train, X_test, y_train, y_test, scaler = preprocess_air_pollution_data(air_data)

# Preprocess health data
X_train, X_test, y_train, y_test, scaler, label_encoder = preprocess_health_data(health_data)
```

### Train Models

```python
from src.train_models import train_air_pollution_model, train_health_model

# Train air pollution model (using 10,000 samples for better performance)
train_air_pollution_model(sample_size=10000)

# Train health activity model (using all available data - 500 samples)
train_health_model(sample_size=500)
```

Or run from command line:

```bash
python -m src.train_models
```

### Run Complete Example

```bash
python example_usage.py
```

This script demonstrates the complete pipeline: loading data, preprocessing, training models, and making predictions.

## Features

- **Data Sampling**: Automatically samples large datasets for faster experimentation
- **Preprocessing Pipelines**: Handles missing values, feature engineering, and scaling
- **Model Training**: Random Forest models for both regression and classification tasks
- **Model Persistence**: Saves trained models, scalers, and encoders for later use

## Datasets

### Urban Air Pollution Dataset
- **Target**: AQI_Target (Air Quality Index)
- **Features**: PM2.5, PM10, NO₂, SO₂, CO, O₃, Temperature, Humidity, Wind Speed/Direction, Pressure, Rain
- **Task**: Regression

### Wearable Sports Health Dataset
- **Target**: Activity_Status (Walking, Running, Cycling, Resting)
- **Features**: Heart Rate, Body Temperature, Blood Pressure, Blood Oxygen, Step Count, Location
- **Task**: Classification

## FastAPI Dashboard API

The project includes a FastAPI application with endpoints for health authorities and citizens.

### Running the API

```bash
# Option 1: Using the script
./run_api.sh

# Option 2: Direct command
source venv/bin/activate
uvicorn api.main:app --reload --host 0.0.0.0 --port 8000
```

### API Endpoints

**Health Authority Endpoints:**
- `GET /api/health-authorities/risk-map` - Public health risk maps
- `GET /api/health-authorities/alerts` - Public health alerts
- `GET /api/health-authorities/stats` - Overall health statistics

**Citizen Endpoints:**
- `GET /api/citizens/personal-alerts` - Personal health alerts
- `GET /api/citizens/trends` - Personal health trends
- `POST /api/citizens/predict-activity` - Predict activity from health metrics

**Prediction Endpoints:**
- `POST /api/predict/air-quality` - Predict AQI from pollution data
- `POST /api/predict/activity` - Predict activity status

### Interactive Documentation

Once the server is running:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

See `API_DOCUMENTATION.md` for detailed API documentation.

## Notes

- Air pollution data is sampled to 10,000 rows for better model performance and to reduce overfitting
- Health data uses all available 500 rows (the dataset is smaller)
- Models are saved in the `models/` directory
- All preprocessing steps are reproducible with fixed random seeds
- Increased sample sizes help prevent overfitting and improve model generalization
- Health activity model achieves ~96% accuracy with enhanced features and data augmentation

