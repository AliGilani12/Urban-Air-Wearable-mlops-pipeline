import { useQuery } from '@tanstack/react-query';
import Layout from '../components/Layout';
import StatsCard from '../components/StatsCard';
import AlertCard from '../components/Alerts/AlertCard';
import RiskMap from '../components/Maps/RiskMap';
import BarChart from '../components/Charts/BarChart';
import PieChart from '../components/Charts/PieChart';
import { getRiskMap, getHealthAlerts, getHealthStats } from '../services/api';

const AuthorityDashboard = () => {
  // Fetch risk map data
  const { data: riskMapData, isLoading: mapLoading } = useQuery({
    queryKey: ['riskMap'],
    queryFn: () => getRiskMap(),
    refetchInterval: 60000, // Refetch every minute
  });

  // Fetch health alerts
  const { data: alertsData, isLoading: alertsLoading } = useQuery({
    queryKey: ['healthAlerts'],
    queryFn: () => getHealthAlerts(null, 50),
    refetchInterval: 30000, // Refetch every 30 seconds
  });

  // Fetch health statistics
  const { data: statsData, isLoading: statsLoading } = useQuery({
    queryKey: ['healthStats'],
    queryFn: () => getHealthStats(),
    refetchInterval: 60000, // Refetch every minute
  });

  const riskMapStations = riskMapData?.data || [];
  const alerts = alertsData?.alerts || [];
  const stats = statsData || {};

  // Prepare alert severity distribution
  const severityDistribution = alerts.reduce((acc, alert) => {
    const severity = alert.severity || 'Unknown';
    acc[severity] = (acc[severity] || 0) + 1;
    return acc;
  }, {});

  // Prepare alert type distribution
  const alertTypeDistribution = alerts.reduce((acc, alert) => {
    const type = alert.type || 'Unknown';
    acc[type] = (acc[type] || 0) + 1;
    return acc;
  }, {});

  // Prepare risk level distribution
  const riskLevelDistribution = riskMapStations.reduce((acc, station) => {
    const risk = station.risk_level || 'Unknown';
    acc[risk] = (acc[risk] || 0) + 1;
    return acc;
  }, {});

  // High priority alerts (High severity)
  const highPriorityAlerts = alerts.filter(a => a.severity?.toLowerCase() === 'high');

  return (
    <Layout>
      <div className="space-y-6">
        {/* Header */}
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">
            Health Authority Dashboard
          </h1>
          <p className="text-gray-600">
            System-wide health monitoring and public health risk management
          </p>
        </div>

        {/* Statistics Cards */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          <StatsCard
            title="Average AQI"
            value={stats.air_quality?.average_aqi?.toFixed(1) || 'N/A'}
            subtitle="Air Quality Index"
            icon="🌬️"
            color="blue"
          />
          <StatsCard
            title="High Risk Stations"
            value={stats.air_quality?.high_risk_stations || 0}
            subtitle={`${stats.air_quality?.risk_percentage?.toFixed(1) || 0}% of total`}
            icon="⚠️"
            color="red"
          />
          <StatsCard
            title="Total Alerts"
            value={alerts.length}
            subtitle={`${highPriorityAlerts.length} high priority`}
            icon="🚨"
            color={highPriorityAlerts.length > 0 ? 'red' : 'yellow'}
          />
          <StatsCard
            title="Total Stations"
            value={stats.air_quality?.total_stations || 0}
            subtitle="Monitoring stations"
            icon="📍"
            color="green"
          />
        </div>

        {/* Risk Map */}
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
          <h2 className="text-xl font-bold text-gray-900 mb-4">Public Health Risk Map</h2>
          {mapLoading ? (
            <div className="text-center py-8 text-gray-500">Loading map data...</div>
          ) : riskMapStations.length > 0 ? (
            <>
              <RiskMap data={riskMapStations} />
              <div className="mt-4 flex flex-wrap gap-4 text-sm">
                <div className="flex items-center">
                  <div className="w-4 h-4 bg-green-500 rounded-full mr-2"></div>
                  <span>Low Risk</span>
                </div>
                <div className="flex items-center">
                  <div className="w-4 h-4 bg-yellow-500 rounded-full mr-2"></div>
                  <span>Moderate Risk</span>
                </div>
                <div className="flex items-center">
                  <div className="w-4 h-4 bg-orange-500 rounded-full mr-2"></div>
                  <span>Unhealthy for Sensitive</span>
                </div>
                <div className="flex items-center">
                  <div className="w-4 h-4 bg-red-500 rounded-full mr-2"></div>
                  <span>Unhealthy</span>
                </div>
              </div>
            </>
          ) : (
            <div className="text-center py-8 text-gray-500">No map data available</div>
          )}
        </div>

        {/* System-wide Alerts */}
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
          <div className="flex justify-between items-center mb-4">
            <h2 className="text-xl font-bold text-gray-900">System-wide Outbreak Alerts</h2>
            <span className="text-sm text-gray-500">
              {alerts.length} total alerts
            </span>
          </div>
          {alertsLoading ? (
            <div className="text-center py-8 text-gray-500">Loading alerts...</div>
          ) : alerts.length === 0 ? (
            <div className="text-center py-8 text-gray-500">
              <p className="text-lg mb-2">✅ No active alerts</p>
              <p className="text-sm">All systems operating normally.</p>
            </div>
          ) : (
            <div className="space-y-4 max-h-96 overflow-y-auto">
              {alerts.slice(0, 10).map((alert, index) => (
                <AlertCard key={alert.alert_id || index} alert={alert} />
              ))}
            </div>
          )}
        </div>

        {/* Analytics Charts */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Alert Severity Distribution */}
          <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
            <h2 className="text-xl font-bold text-gray-900 mb-4">Alert Severity Distribution</h2>
            {Object.keys(severityDistribution).length > 0 ? (
              <PieChart data={severityDistribution} />
            ) : (
              <div className="text-center py-8 text-gray-500">No data available</div>
            )}
          </div>

          {/* Risk Level Distribution */}
          <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
            <h2 className="text-xl font-bold text-gray-900 mb-4">Risk Level Distribution</h2>
            {Object.keys(riskLevelDistribution).length > 0 ? (
              <PieChart data={riskLevelDistribution} />
            ) : (
              <div className="text-center py-8 text-gray-500">No data available</div>
            )}
          </div>
        </div>

        {/* Additional Statistics */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Health Metrics Summary */}
          <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
            <h2 className="text-xl font-bold text-gray-900 mb-4">Health Metrics Summary</h2>
            {statsLoading ? (
              <div className="text-center py-8 text-gray-500">Loading statistics...</div>
            ) : stats.health_metrics ? (
              <div className="space-y-4">
                <div className="flex justify-between items-center p-3 bg-blue-50 rounded">
                  <span className="text-gray-700">Average Heart Rate</span>
                  <span className="font-semibold text-gray-900">
                    {stats.health_metrics.average_heart_rate?.toFixed(1) || 'N/A'} bpm
                  </span>
                </div>
                <div className="flex justify-between items-center p-3 bg-green-50 rounded">
                  <span className="text-gray-700">Average Steps</span>
                  <span className="font-semibold text-gray-900">
                    {stats.health_metrics.average_steps?.toFixed(0) || 'N/A'} steps
                  </span>
                </div>
                <div className="flex justify-between items-center p-3 bg-yellow-50 rounded">
                  <span className="text-gray-700">Total Records</span>
                  <span className="font-semibold text-gray-900">
                    {stats.health_metrics.total_records || 0}
                  </span>
                </div>
                {stats.health_metrics.activity_distribution && (
                  <div className="mt-4">
                    <h3 className="text-sm font-semibold text-gray-700 mb-2">Activity Distribution</h3>
                    <div className="space-y-2">
                      {Object.entries(stats.health_metrics.activity_distribution).map(([activity, count]) => (
                        <div key={activity} className="flex justify-between items-center text-sm">
                          <span className="text-gray-600">{activity}</span>
                          <span className="font-medium text-gray-900">{count}</span>
                        </div>
                      ))}
                    </div>
                  </div>
                )}
              </div>
            ) : (
              <div className="text-center py-8 text-gray-500">No data available</div>
            )}
          </div>

          {/* Air Quality Summary */}
          <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
            <h2 className="text-xl font-bold text-gray-900 mb-4">Air Quality Summary</h2>
            {statsLoading ? (
              <div className="text-center py-8 text-gray-500">Loading statistics...</div>
            ) : stats.air_quality ? (
              <div className="space-y-4">
                <div className="flex justify-between items-center p-3 bg-blue-50 rounded">
                  <span className="text-gray-700">Average AQI</span>
                  <span className="font-semibold text-gray-900">
                    {stats.air_quality.average_aqi?.toFixed(1) || 'N/A'}
                  </span>
                </div>
                <div className="flex justify-between items-center p-3 bg-red-50 rounded">
                  <span className="text-gray-700">Max AQI</span>
                  <span className="font-semibold text-gray-900">
                    {stats.air_quality.max_aqi?.toFixed(1) || 'N/A'}
                  </span>
                </div>
                <div className="flex justify-between items-center p-3 bg-yellow-50 rounded">
                  <span className="text-gray-700">High Risk Stations</span>
                  <span className="font-semibold text-gray-900">
                    {stats.air_quality.high_risk_stations || 0} / {stats.air_quality.total_stations || 0}
                  </span>
                </div>
                <div className="flex justify-between items-center p-3 bg-green-50 rounded">
                  <span className="text-gray-700">Risk Percentage</span>
                  <span className="font-semibold text-gray-900">
                    {stats.air_quality.risk_percentage?.toFixed(1) || 0}%
                  </span>
                </div>
              </div>
            ) : (
              <div className="text-center py-8 text-gray-500">No data available</div>
            )}
          </div>
        </div>
      </div>
    </Layout>
  );
};

export default AuthorityDashboard;

