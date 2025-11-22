# FastAPI Dashboard API Documentation

## Overview
FastAPI endpoints for Health Authorities and Citizens dashboards with real-time health and air quality monitoring.

## Base URL
```
http://localhost:8000
```

## Running the API

### Option 1: Using the script
```bash
./run_api.sh
```

### Option 2: Direct command
```bash
source venv/bin/activate
uvicorn api.main:app --reload --host 0.0.0.0 --port 8000
```

### Option 3: Python module
```bash
source venv/bin/activate
python -m uvicorn api.main:app --reload
```

## API Endpoints

### Root
- **GET** `/` - API information and available endpoints

### Health Authority Endpoints

#### 1. Risk Map
- **GET** `/api/health-authorities/risk-map`
- **Description**: Get public health risk map data showing air quality risks by location
- **Query Parameters**:
  - `region` (optional): Filter by region
- **Response**: List of stations with AQI, risk levels, and coordinates

**Example:**
```bash
curl http://localhost:8000/api/health-authorities/risk-map
```

#### 2. Health Alerts
- **GET** `/api/health-authorities/alerts`
- **Description**: Get public health alerts for health authorities
- **Query Parameters**:
  - `severity` (optional): Filter by severity (High, Medium, Low)
  - `limit` (optional, default=50): Maximum number of alerts to return
- **Response**: List of alerts with severity, location, and recommendations

**Example:**
```bash
curl "http://localhost:8000/api/health-authorities/alerts?severity=High&limit=20"
```

#### 3. Health Statistics
- **GET** `/api/health-authorities/stats`
- **Description**: Get overall health statistics for dashboard
- **Response**: Air quality stats, health metrics, activity distribution

**Example:**
```bash
curl http://localhost:8000/api/health-authorities/stats
```

### Citizen Endpoints

#### 1. Personal Alerts
- **GET** `/api/citizens/personal-alerts`
- **Description**: Get personal health alerts for citizens
- **Query Parameters**:
  - `user_id` (optional): Filter alerts for specific user
- **Response**: Personal health alerts based on metrics

**Example:**
```bash
curl "http://localhost:8000/api/citizens/personal-alerts?user_id=ATH001"
```

#### 2. Personal Trends
- **GET** `/api/citizens/trends`
- **Description**: Get personal health trends over time
- **Query Parameters**:
  - `user_id` (optional): User ID to get trends for
  - `metric` (optional, default="all"): Specific metric (heart_rate, step_count, body_temperature)
  - `days` (optional, default=7): Number of days to look back
- **Response**: Trend data with values, dates, averages, and trend direction

**Example:**
```bash
curl "http://localhost:8000/api/citizens/trends?user_id=ATH001&metric=heart_rate&days=14"
```

#### 3. Predict Activity
- **POST** `/api/citizens/predict-activity`
- **Description**: Predict activity status from health metrics
- **Request Body** (JSON):
```json
{
  "Heart_Rate": 120,
  "Body_Temperature": 37.0,
  "Blood_Oxygen": 98,
  "Step_Count": 750,
  "BP_Systolic": 120,
  "BP_Diastolic": 80,
  "Latitude": 12.927,
  "Longitude": 80.116,
  "Timestamp": "2025-04-10 10:00:00"
}
```
- **Response**: Predicted activity with confidence scores

**Example:**
```bash
curl -X POST http://localhost:8000/api/citizens/predict-activity \
  -H "Content-Type: application/json" \
  -d '{
    "Heart_Rate": 120,
    "Body_Temperature": 37.0,
    "Blood_Oxygen": 98,
    "Step_Count": 750,
    "BP_Systolic": 120,
    "BP_Diastolic": 80,
    "Latitude": 12.927,
    "Longitude": 80.116,
    "Timestamp": "2025-04-10 10:00:00"
  }'
```

### Prediction Endpoints

#### 1. Predict Air Quality
- **POST** `/api/predict/air-quality`
- **Description**: Predict Air Quality Index from pollution metrics
- **Request Body** (JSON):
```json
{
  "PM25": 50.0,
  "PM10": 70.0,
  "NO2": 25.0,
  "SO2": 10.0,
  "CO": 0.6,
  "O3": 35.0,
  "Temp_C": 28.0,
  "Humidity": 65.0,
  "Wind_Speed": 3.0,
  "Wind_Direction": 180.0,
  "Pressure": 1013.0,
  "Rain": 0.0
}
```
- **Response**: Predicted AQI with category and health recommendations

**Example:**
```bash
curl -X POST http://localhost:8000/api/predict/air-quality \
  -H "Content-Type: application/json" \
  -d '{
    "PM25": 50.0,
    "PM10": 70.0,
    "NO2": 25.0,
    "SO2": 10.0,
    "CO": 0.6,
    "O3": 35.0,
    "Temp_C": 28.0,
    "Humidity": 65.0,
    "Wind_Speed": 3.0,
    "Wind_Direction": 180.0,
    "Pressure": 1013.0,
    "Rain": 0.0
  }'
```

## Interactive API Documentation

Once the server is running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Response Format

All endpoints return JSON responses with the following structure:

**Success:**
```json
{
  "status": "success",
  "data": {...},
  "timestamp": "2025-04-10T10:00:00"
}
```

**Error:**
```json
{
  "detail": "Error message"
}
```

## Notes

- All timestamps are in ISO 8601 format
- Coordinates are in decimal degrees (latitude, longitude)
- AQI values range from 0-500
- Health metrics use standard units (bpm, °C, %, etc.)
- The API includes CORS middleware for frontend integration

