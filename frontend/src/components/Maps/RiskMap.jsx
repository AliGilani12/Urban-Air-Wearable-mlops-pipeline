import { MapContainer, TileLayer, CircleMarker, Popup } from 'react-leaflet';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';

// Fix for Leaflet default icon issue with React
delete L.Icon.Default.prototype._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/images/marker-icon-2x.png',
  iconUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/images/marker-icon.png',
  shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/images/marker-shadow.png',
});

const RiskMap = ({ data = [] }) => {
  const getColor = (riskLevel) => {
    switch (riskLevel) {
      case 'Low': return 'green';
      case 'Moderate': return 'yellow';
      case 'Unhealthy for Sensitive': return 'orange';
      case 'Unhealthy': return 'red';
      default: return 'gray';
    }
  };

  const getRadius = (aqi) => {
    if (aqi < 50) return 8;
    if (aqi < 100) return 12;
    if (aqi < 150) return 16;
    return 20;
  };

  // Calculate center from data or use default
  const center = data.length > 0
    ? [data[0].latitude || 12.9716, data[0].longitude || 77.5946]
    : [12.9716, 77.5946]; // Default to a central location

  return (
    <div className="w-full h-[500px] rounded-lg overflow-hidden border border-gray-300">
      <MapContainer
        center={center}
        zoom={11}
        style={{ height: '100%', width: '100%' }}
      >
        <TileLayer
          attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />
        {data.map((station, index) => (
          <CircleMarker
            key={station.station_id || index}
            center={[station.latitude, station.longitude]}
            radius={getRadius(station.aqi)}
            pathOptions={{
              color: getColor(station.risk_level),
              fillColor: getColor(station.risk_level),
              fillOpacity: 0.6,
            }}
          >
            <Popup>
              <div className="p-2">
                <h3 className="font-semibold text-sm">Station {station.station_id}</h3>
                <p className="text-xs mt-1">
                  <strong>AQI:</strong> {station.aqi?.toFixed(1) || 'N/A'}
                </p>
                <p className="text-xs">
                  <strong>Risk:</strong> {station.risk_level || 'Unknown'}
                </p>
                <p className="text-xs">
                  <strong>PM2.5:</strong> {station.pm25?.toFixed(1) || 'N/A'}
                </p>
                <p className="text-xs">
                  <strong>PM10:</strong> {station.pm10?.toFixed(1) || 'N/A'}
                </p>
              </div>
            </Popup>
          </CircleMarker>
        ))}
      </MapContainer>
    </div>
  );
};

export default RiskMap;

