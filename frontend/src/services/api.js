import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// ==================== HEALTH AUTHORITY ENDPOINTS ====================

/**
 * Get public health risk map data
 * @param {string} region - Optional region filter
 * @returns {Promise} Risk map data with stations and AQI
 */
export const getRiskMap = async (region = null) => {
  const params = region ? { region } : {};
  const response = await api.get('/api/health-authorities/risk-map', { params });
  return response.data;
};

/**
 * Get public health alerts
 * @param {string} severity - Optional severity filter (High, Medium, Low)
 * @param {number} limit - Maximum number of alerts (default: 50)
 * @returns {Promise} List of health alerts
 */
export const getHealthAlerts = async (severity = null, limit = 50) => {
  const params = {};
  if (severity) params.severity = severity;
  if (limit) params.limit = limit;
  const response = await api.get('/api/health-authorities/alerts', { params });
  return response.data;
};

/**
 * Get overall health statistics
 * @returns {Promise} Health statistics including air quality and health metrics
 */
export const getHealthStats = async () => {
  const response = await api.get('/api/health-authorities/stats');
  return response.data;
};

// ==================== CITIZEN ENDPOINTS ====================

/**
 * Get personal health alerts
 * @param {string} user_id - Optional user ID filter
 * @returns {Promise} Personal health alerts
 */
export const getPersonalAlerts = async (user_id = null) => {
  const params = user_id ? { user_id } : {};
  const response = await api.get('/api/citizens/personal-alerts', { params });
  return response.data;
};

/**
 * Get personal health trends
 * @param {string} user_id - Optional user ID
 * @param {string} metric - Metric to get trends for (default: "all")
 * @param {number} days - Number of days to look back (default: 7)
 * @returns {Promise} Personal health trends data
 */
export const getPersonalTrends = async (user_id = null, metric = 'all', days = 7) => {
  const params = {};
  if (user_id) params.user_id = user_id;
  if (metric) params.metric = metric;
  if (days) params.days = days;
  const response = await api.get('/api/citizens/trends', { params });
  return response.data;
};

/**
 * Predict activity from health metrics
 * @param {Object} metrics - Health metrics object
 * @param {number} metrics.Heart_Rate
 * @param {number} metrics.Body_Temperature
 * @param {number} metrics.Blood_Oxygen
 * @param {number} metrics.Step_Count
 * @param {number} metrics.BP_Systolic
 * @param {number} metrics.BP_Diastolic
 * @param {number} metrics.Latitude
 * @param {number} metrics.Longitude
 * @param {string} metrics.Timestamp
 * @returns {Promise} Predicted activity with confidence
 */
export const predictActivity = async (metrics) => {
  const response = await api.post('/api/citizens/predict-activity', metrics);
  return response.data;
};

// ==================== PREDICTION ENDPOINTS ====================

/**
 * Predict Air Quality Index
 * @param {Object} data - Air quality data
 * @param {number} data.PM25
 * @param {number} data.PM10
 * @param {number} data.NO2
 * @param {number} data.SO2
 * @param {number} data.CO
 * @param {number} data.O3
 * @param {number} data.Temp_C
 * @param {number} data.Humidity
 * @param {number} data.Wind_Speed
 * @param {number} data.Wind_Direction
 * @param {number} data.Pressure
 * @param {number} data.Rain
 * @returns {Promise} Predicted AQI with category
 */
export const predictAirQuality = async (data) => {
  const response = await api.post('/api/predict/air-quality', data);
  return response.data;
};

// ==================== ROOT ENDPOINT ====================

/**
 * Get API information and available endpoints
 * @returns {Promise} API information
 */
export const getApiInfo = async () => {
  const response = await api.get('/');
  return response.data;
};

export default api;

