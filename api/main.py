"""
FastAPI application for Health and Air Quality Dashboards
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import pandas as pd
import numpy as np
import joblib
from pathlib import Path
from datetime import datetime, timedelta
import json

app = FastAPI(title="Health & Air Quality Dashboard API", version="1.0.0")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load models
BASE_PATH = Path(__file__).parent.parent
MODELS_DIR = BASE_PATH / "models"
DATA_DIR = BASE_PATH / "Data"

# Load models (with error handling)
try:
    air_model = joblib.load(MODELS_DIR / "air_pollution_model.pkl")
    air_scaler = joblib.load(MODELS_DIR / "air_pollution_scaler.pkl")
    health_model = joblib.load(MODELS_DIR / "health_activity_model.pkl")
    health_scaler = joblib.load(MODELS_DIR / "health_scaler.pkl")
    health_label_encoder = joblib.load(MODELS_DIR / "health_label_encoder.pkl")
    MODELS_LOADED = True
except Exception as e:
    print(f"Warning: Could not load models: {e}")
    MODELS_LOADED = False

# Load data for dashboards
try:
    air_data = pd.read_csv(DATA_DIR / "UrbanAirPollutionDataset.csv")
    health_data = pd.read_csv(DATA_DIR / "wearable_sports_health_dataset.csv")
    DATA_LOADED = True
except Exception as e:
    print(f"Warning: Could not load data: {e}")
    DATA_LOADED = False


# Pydantic models for request/response
class AirQualityPrediction(BaseModel):
    PM25: float
    PM10: float
    NO2: float
    SO2: float
    CO: float
    O3: float
    Temp_C: float
    Humidity: float
    Wind_Speed: float
    Wind_Direction: float
    Pressure: float
    Rain: float


class HealthMetrics(BaseModel):
    Heart_Rate: float
    Body_Temperature: float
    Blood_Oxygen: float
    Step_Count: float
    BP_Systolic: float
    BP_Diastolic: float
    Latitude: float
    Longitude: float
    Timestamp: str


class AlertRequest(BaseModel):
    location: Optional[str] = None
    date_from: Optional[str] = None
    date_to: Optional[str] = None


@app.get("/")
async def root():
    """Root endpoint with API information and documentation links"""
    return {
        "message": "Health & Air Quality Dashboard API",
        "version": "1.0.0",
        "documentation": {
            "swagger_ui": "/docs",
            "redoc": "/redoc",
            "openapi_schema": "/openapi.json"
        },
        "endpoints": {
            "health_authorities": {
                "risk_map": {
                    "url": "/api/health-authorities/risk-map",
                    "method": "GET",
                    "description": "Get public health risk map data"
                },
                "alerts": {
                    "url": "/api/health-authorities/alerts",
                    "method": "GET",
                    "description": "Get public health alerts",
                    "query_params": ["severity", "limit"]
                },
                "stats": {
                    "url": "/api/health-authorities/stats",
                    "method": "GET",
                    "description": "Get overall health statistics"
                }
            },
            "citizens": {
                "personal_alerts": {
                    "url": "/api/citizens/personal-alerts",
                    "method": "GET",
                    "description": "Get personal health alerts",
                    "query_params": ["user_id"]
                },
                "trends": {
                    "url": "/api/citizens/trends",
                    "method": "GET",
                    "description": "Get personal health trends",
                    "query_params": ["user_id", "metric", "days"]
                },
                "predict_activity": {
                    "url": "/api/citizens/predict-activity",
                    "method": "POST",
                    "description": "Predict activity from health metrics"
                }
            },
            "predictions": {
                "air_quality": {
                    "url": "/api/predict/air-quality",
                    "method": "POST",
                    "description": "Predict Air Quality Index"
                },
                "activity": {
                    "url": "/api/predict/activity",
                    "method": "POST",
                    "description": "Predict activity status"
                }
            }
        },
        "quick_start": "Visit /docs for interactive API documentation"
    }


# ==================== HEALTH AUTHORITY ENDPOINTS ====================

@app.get("/api/health-authorities/risk-map")
async def get_risk_map(region: Optional[str] = None):
    """
    Get public health risk map data for health authorities
    Shows air quality risks by location
    """
    if not DATA_LOADED:
        raise HTTPException(status_code=503, detail="Data not available")
    
    try:
        # Sample data for risk map (using air pollution data)
        sample_data = air_data.sample(min(1000, len(air_data)))
        
        risk_map_data = []
        for _, row in sample_data.iterrows():
            aqi = row.get('AQI_Target', 50)
            
            # Categorize risk level
            if aqi < 50:
                risk_level = "Low"
                color = "green"
            elif aqi < 100:
                risk_level = "Moderate"
                color = "yellow"
            elif aqi < 150:
                risk_level = "Unhealthy for Sensitive"
                color = "orange"
            else:
                risk_level = "Unhealthy"
                color = "red"
            
            risk_map_data.append({
                "station_id": str(row.get('Station_ID', 'Unknown')),
                "latitude": 12.9 + np.random.random() * 0.1,  # Simulated coordinates
                "longitude": 80.1 + np.random.random() * 0.1,
                "aqi": float(aqi),
                "risk_level": risk_level,
                "color": color,
                "pm25": float(row.get('PM2.5', 0)),
                "pm10": float(row.get('PM10', 0)),
                "timestamp": str(row.get('DateTime', datetime.now()))
            })
        
        return {
            "status": "success",
            "data": risk_map_data,
            "total_stations": len(risk_map_data),
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating risk map: {str(e)}")


@app.get("/api/health-authorities/alerts")
async def get_health_alerts(severity: Optional[str] = None, limit: int = 50):
    """
    Get public health alerts for health authorities
    """
    if not DATA_LOADED:
        raise HTTPException(status_code=503, detail="Data not available")
    
    try:
        alerts = []
        
        # Generate alerts from air quality data
        high_aqi_data = air_data[air_data['AQI_Target'] > 100].head(limit)
        
        for _, row in high_aqi_data.iterrows():
            aqi = row.get('AQI_Target', 0)
            
            if aqi > 150:
                alert_severity = "High"
                alert_type = "Air Quality Warning"
                message = f"Unhealthy air quality detected (AQI: {aqi:.1f})"
            elif aqi > 100:
                alert_severity = "Medium"
                alert_type = "Air Quality Advisory"
                message = f"Moderate air quality concern (AQI: {aqi:.1f})"
            else:
                continue
            
            alerts.append({
                "alert_id": f"AQ-{row.get('Station_ID', 'Unknown')}-{hash(str(row.get('DateTime', ''))) % 10000}",
                "type": alert_type,
                "severity": alert_severity,
                "message": message,
                "location": f"Station {row.get('Station_ID', 'Unknown')}",
                "aqi": float(aqi),
                "pm25": float(row.get('PM2.5', 0)),
                "pm10": float(row.get('PM10', 0)),
                "timestamp": str(row.get('DateTime', datetime.now())),
                "recommendation": "Limit outdoor activities for sensitive groups" if aqi > 100 else "Monitor air quality"
            })
        
        # Filter by severity if requested
        if severity:
            alerts = [a for a in alerts if a['severity'].lower() == severity.lower()]
        
        return {
            "status": "success",
            "alerts": alerts,
            "total_alerts": len(alerts),
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching alerts: {str(e)}")


@app.get("/api/health-authorities/stats")
async def get_health_stats():
    """
    Get overall health statistics for health authorities dashboard
    """
    if not DATA_LOADED:
        raise HTTPException(status_code=503, detail="Data not available")
    
    try:
        # Air quality statistics
        avg_aqi = air_data['AQI_Target'].mean()
        max_aqi = air_data['AQI_Target'].max()
        high_risk_stations = len(air_data[air_data['AQI_Target'] > 100])
        total_stations = len(air_data['Station_ID'].unique())
        
        # Health activity statistics
        activity_dist = health_data['Activity_Status'].value_counts().to_dict()
        avg_heart_rate = health_data['Heart_Rate'].mean()
        avg_steps = health_data['Step_Count'].mean()
        
        return {
            "status": "success",
            "air_quality": {
                "average_aqi": float(avg_aqi),
                "max_aqi": float(max_aqi),
                "high_risk_stations": int(high_risk_stations),
                "total_stations": int(total_stations),
                "risk_percentage": float((high_risk_stations / total_stations) * 100) if total_stations > 0 else 0
            },
            "health_metrics": {
                "activity_distribution": activity_dist,
                "average_heart_rate": float(avg_heart_rate),
                "average_steps": float(avg_steps),
                "total_records": int(len(health_data))
            },
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching stats: {str(e)}")


# ==================== CITIZEN ENDPOINTS ====================

@app.get("/api/citizens/personal-alerts")
async def get_personal_alerts(user_id: Optional[str] = None):
    """
    Get personal health alerts for citizens
    """
    if not DATA_LOADED:
        raise HTTPException(status_code=503, detail="Data not available")
    
    try:
        # Filter health data for specific user if provided
        user_data = health_data
        if user_id:
            user_data = health_data[health_data['Athlete_ID'] == user_id]
        
        if len(user_data) == 0:
            user_data = health_data.sample(min(10, len(health_data)))
        
        alerts = []
        
        for _, row in user_data.iterrows():
            hr = row.get('Heart_Rate', 0)
            steps = row.get('Step_Count', 0)
            temp = row.get('Body_Temperature', 0)
            oxygen = row.get('Blood_Oxygen', 0)
            
            # Generate personal alerts
            if hr > 160:
                alerts.append({
                    "alert_id": f"HR-{row.get('Record_ID', 'Unknown')}",
                    "type": "High Heart Rate",
                    "severity": "Medium",
                    "message": f"Your heart rate is elevated ({hr} bpm). Consider resting.",
                    "timestamp": str(row.get('Timestamp', datetime.now())),
                    "recommendation": "Take a break and monitor your heart rate"
                })
            
            if temp > 37.5:
                alerts.append({
                    "alert_id": f"TEMP-{row.get('Record_ID', 'Unknown')}",
                    "type": "Elevated Body Temperature",
                    "severity": "High",
                    "message": f"Your body temperature is elevated ({temp}°C).",
                    "timestamp": str(row.get('Timestamp', datetime.now())),
                    "recommendation": "Stay hydrated and rest. Consult a doctor if it persists."
                })
            
            if oxygen < 95:
                alerts.append({
                    "alert_id": f"O2-{row.get('Record_ID', 'Unknown')}",
                    "type": "Low Blood Oxygen",
                    "severity": "High",
                    "message": f"Your blood oxygen level is low ({oxygen}%).",
                    "timestamp": str(row.get('Timestamp', datetime.now())),
                    "recommendation": "Seek medical attention if symptoms persist"
                })
            
            if steps < 300 and hr > 100:
                alerts.append({
                    "alert_id": f"ACT-{row.get('Record_ID', 'Unknown')}",
                    "type": "Activity Mismatch",
                    "severity": "Low",
                    "message": "High heart rate with low step count detected.",
                    "timestamp": str(row.get('Timestamp', datetime.now())),
                    "recommendation": "This might indicate stress. Consider relaxation techniques."
                })
        
        return {
            "status": "success",
            "user_id": user_id or "sample",
            "alerts": alerts[:20],  # Limit to 20 most recent
            "total_alerts": len(alerts),
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching personal alerts: {str(e)}")


@app.get("/api/citizens/trends")
async def get_personal_trends(
    user_id: Optional[str] = None,
    metric: str = "all",
    days: int = 7
):
    """
    Get personal health trends for citizens
    """
    if not DATA_LOADED:
        raise HTTPException(status_code=503, detail="Data not available")
    
    try:
        # Filter data for user
        user_data = health_data.copy()
        if user_id:
            user_data = health_data[health_data['Athlete_ID'] == user_id]
        
        if len(user_data) == 0:
            user_data = health_data.sample(min(50, len(health_data))).copy()
        
        # Convert timestamp
        user_data['Timestamp'] = pd.to_datetime(user_data['Timestamp'])
        user_data = user_data.sort_values('Timestamp')
        
        # Get last N days
        cutoff_date = datetime.now() - timedelta(days=days)
        user_data = user_data[user_data['Timestamp'] >= cutoff_date]
        
        trends = {
            "heart_rate": {
                "values": user_data['Heart_Rate'].tolist(),
                "dates": user_data['Timestamp'].dt.strftime('%Y-%m-%d %H:%M').tolist(),
                "average": float(user_data['Heart_Rate'].mean()),
                "trend": "increasing" if user_data['Heart_Rate'].iloc[-1] > user_data['Heart_Rate'].iloc[0] else "decreasing"
            },
            "step_count": {
                "values": user_data['Step_Count'].tolist(),
                "dates": user_data['Timestamp'].dt.strftime('%Y-%m-%d %H:%M').tolist(),
                "average": float(user_data['Step_Count'].mean()),
                "trend": "increasing" if user_data['Step_Count'].iloc[-1] > user_data['Step_Count'].iloc[0] else "decreasing"
            },
            "body_temperature": {
                "values": user_data['Body_Temperature'].tolist(),
                "dates": user_data['Timestamp'].dt.strftime('%Y-%m-%d %H:%M').tolist(),
                "average": float(user_data['Body_Temperature'].mean()),
                "trend": "stable"
            },
            "activity_distribution": user_data['Activity_Status'].value_counts().to_dict()
        }
        
        # Filter by metric if requested
        if metric != "all":
            trends = {metric: trends.get(metric, {})}
        
        return {
            "status": "success",
            "user_id": user_id or "sample",
            "period_days": days,
            "trends": trends,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching trends: {str(e)}")


@app.post("/api/citizens/predict-activity")
async def predict_activity(metrics: HealthMetrics):
    """
    Predict activity status from health metrics for citizens
    Note: This is a simplified prediction. For production, use full preprocessing pipeline.
    """
    if not MODELS_LOADED:
        raise HTTPException(status_code=503, detail="Models not available")
    
    try:
        # Calculate derived features (simplified version)
        hr_to_steps = metrics.Heart_Rate / (metrics.Step_Count + 1)
        bp_ratio = metrics.BP_Systolic / (metrics.BP_Diastolic + 1)
        bp_pulse = metrics.BP_Systolic - metrics.BP_Diastolic
        hr_temp_interaction = metrics.Heart_Rate * metrics.Body_Temperature
        hr_bp_interaction = metrics.Heart_Rate * metrics.BP_Systolic
        intensity_score = (metrics.Heart_Rate / 200) * 0.5 + (metrics.Step_Count / 1000) * 0.5
        
        # Parse timestamp for temporal features
        try:
            ts = pd.to_datetime(metrics.Timestamp)
            hour = ts.hour
            minute = ts.minute
        except:
            hour = datetime.now().hour
            minute = datetime.now().minute
        
        # Create feature array matching preprocessing (32 features)
        # Base features + temporal + GPS + domain rules + engineered
        features = np.array([[
            metrics.Heart_Rate, metrics.Step_Count, metrics.Body_Temperature, metrics.Blood_Oxygen,
            metrics.Latitude, metrics.Longitude, metrics.BP_Systolic, metrics.BP_Diastolic,
            # Temporal patterns (simplified - using defaults)
            5.0,  # Time_Diff (default 5 min)
            metrics.Heart_Rate,  # HR_Rolling_Mean (using current)
            metrics.Step_Count,  # Steps_Rolling_Mean (using current)
            0.0,  # HR_Change
            0.0,  # Steps_Change
            5.0,  # Activity_Duration
            # GPS and movement (simplified)
            0.0,  # GPS_Speed
            0.0,  # Distance_Moved
            metrics.Step_Count / 5.0,  # Step_Rate
            # Domain knowledge rules
            1 if (metrics.Heart_Rate > 130 and metrics.Step_Count > 600) else 0,  # Likely_Running
            1 if (80 <= metrics.Heart_Rate <= 120 and 400 <= metrics.Step_Count <= 800) else 0,  # Likely_Walking
            1 if (metrics.Heart_Rate > 120 and metrics.Step_Count > 650) else 0,  # Likely_Cycling
            1 if (metrics.Heart_Rate < 100 and metrics.Step_Count < 500) else 0,  # Likely_Resting
            2 if metrics.Heart_Rate >= 130 else 1,  # Activity_Intensity
            # Engineered features
            hr_to_steps, bp_ratio, bp_pulse,
            hr_temp_interaction, hr_bp_interaction,
            2.0,  # HR_Zone (simplified)
            2.0,  # Step_Intensity (simplified)
            intensity_score,
            hour, minute
        ]])
        
        # Scale and predict
        features_scaled = health_scaler.transform(features)
        prediction = health_model.predict(features_scaled)[0]
        probabilities = health_model.predict_proba(features_scaled)[0]
        
        activity = health_label_encoder.inverse_transform([prediction])[0]
        
        return {
            "status": "success",
            "predicted_activity": activity,
            "confidence": float(max(probabilities)),
            "probabilities": {
                health_label_encoder.inverse_transform([i])[0]: float(prob) 
                for i, prob in enumerate(probabilities)
            },
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error predicting activity: {str(e)}")


# ==================== PREDICTION ENDPOINTS ====================

@app.post("/api/predict/air-quality")
async def predict_air_quality(data: AirQualityPrediction):
    """
    Predict Air Quality Index from pollution metrics
    """
    if not MODELS_LOADED:
        raise HTTPException(status_code=503, detail="Models not available")
    
    try:
        # Prepare features
        features = np.array([[
            data.PM25, data.PM10, data.NO2, data.SO2, data.CO, data.O3,
            data.Temp_C, data.Humidity, data.Wind_Speed, data.Wind_Direction,
            data.Pressure, data.Rain,
            0, 0, 0  # Placeholder for temporal features
        ]])
        
        # Scale and predict
        features_scaled = air_scaler.transform(features)
        aqi = air_model.predict(features_scaled)[0]
        
        # Categorize AQI
        if aqi < 50:
            category = "Good"
            health_concern = "None"
        elif aqi < 100:
            category = "Moderate"
            health_concern = "Unusually sensitive people may experience symptoms"
        elif aqi < 150:
            category = "Unhealthy for Sensitive Groups"
            health_concern = "Children, elderly, and people with heart/lung disease should limit outdoor activity"
        else:
            category = "Unhealthy"
            health_concern = "Everyone should limit outdoor activity"
        
        return {
            "status": "success",
            "predicted_aqi": float(aqi),
            "category": category,
            "health_concern": health_concern,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error predicting air quality: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

