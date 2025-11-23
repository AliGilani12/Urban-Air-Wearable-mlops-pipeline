import { useQuery } from '@tanstack/react-query';
import Layout from '../components/Layout';
import StatsCard from '../components/StatsCard';
import AlertCard from '../components/Alerts/AlertCard';
import LineChart from '../components/Charts/LineChart';
import BarChart from '../components/Charts/BarChart';
import PieChart from '../components/Charts/PieChart';
import { getPersonalAlerts, getPersonalTrends } from '../services/api';

const CitizenDashboard = () => {
  // Fetch personal alerts
  const { data: alertsData, isLoading: alertsLoading } = useQuery({
    queryKey: ['personalAlerts'],
    queryFn: () => getPersonalAlerts(),
    refetchInterval: 30000, // Refetch every 30 seconds
  });

  // Fetch personal trends
  const { data: trendsData, isLoading: trendsLoading } = useQuery({
    queryKey: ['personalTrends'],
    queryFn: () => getPersonalTrends(null, 'all', 7),
    refetchInterval: 60000, // Refetch every minute
  });

  const alerts = alertsData?.alerts || [];
  const trends = trendsData?.trends || {};

  // Prepare chart data
  const heartRateData = trends.heart_rate?.dates?.map((date, index) => ({
    date: date.split(' ')[0],
    value: trends.heart_rate.values[index],
  })) || [];

  const stepCountData = trends.step_count?.dates?.map((date, index) => ({
    date: date.split(' ')[0],
    value: trends.step_count.values[index],
  })) || [];

  const temperatureData = trends.body_temperature?.dates?.map((date, index) => ({
    date: date.split(' ')[0],
    value: trends.body_temperature.values[index],
  })) || [];

  const activityDistribution = trends.activity_distribution || {};

  // Calculate statistics
  const avgHeartRate = trends.heart_rate?.average?.toFixed(1) || 'N/A';
  const avgSteps = trends.step_count?.average?.toFixed(0) || 'N/A';
  const avgTemp = trends.body_temperature?.average?.toFixed(1) || 'N/A';
  const totalAlerts = alerts.length;

  return (
    <Layout>
      <div className="space-y-6">
        {/* Header */}
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">
            Citizen Dashboard
          </h1>
          <p className="text-gray-600">
            Your personal health monitoring and insights
          </p>
        </div>

        {/* Statistics Cards */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          <StatsCard
            title="Average Heart Rate"
            value={`${avgHeartRate} bpm`}
            subtitle={trends.heart_rate?.trend ? `Trend: ${trends.heart_rate.trend}` : ''}
            icon="❤️"
            color="red"
          />
          <StatsCard
            title="Average Steps"
            value={avgSteps}
            subtitle={trends.step_count?.trend ? `Trend: ${trends.step_count.trend}` : ''}
            icon="🚶"
            color="blue"
          />
          <StatsCard
            title="Body Temperature"
            value={`${avgTemp}°C`}
            subtitle="Last 7 days"
            icon="🌡️"
            color="yellow"
          />
          <StatsCard
            title="Active Alerts"
            value={totalAlerts}
            subtitle="Requires attention"
            icon="⚠️"
            color={totalAlerts > 0 ? 'red' : 'green'}
          />
        </div>

        {/* Personal Alerts */}
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
          <h2 className="text-xl font-bold text-gray-900 mb-4">Personal Alerts</h2>
          {alertsLoading ? (
            <div className="text-center py-8 text-gray-500">Loading alerts...</div>
          ) : alerts.length === 0 ? (
            <div className="text-center py-8 text-gray-500">
              <p className="text-lg mb-2">✅ No active alerts</p>
              <p className="text-sm">Your health metrics are within normal ranges.</p>
            </div>
          ) : (
            <div className="space-y-4">
              {alerts.map((alert, index) => (
                <AlertCard key={alert.alert_id || index} alert={alert} />
              ))}
            </div>
          )}
        </div>

        {/* Health Trends Charts */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Heart Rate Trend */}
          <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
            <h2 className="text-xl font-bold text-gray-900 mb-4">Heart Rate Trend</h2>
            {trendsLoading ? (
              <div className="text-center py-8 text-gray-500">Loading data...</div>
            ) : heartRateData.length > 0 ? (
              <LineChart
                data={heartRateData}
                dataKey="value"
                name="Heart Rate (bpm)"
                color="#ef4444"
              />
            ) : (
              <div className="text-center py-8 text-gray-500">No data available</div>
            )}
          </div>

          {/* Step Count Trend */}
          <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
            <h2 className="text-xl font-bold text-gray-900 mb-4">Step Count Trend</h2>
            {trendsLoading ? (
              <div className="text-center py-8 text-gray-500">Loading data...</div>
            ) : stepCountData.length > 0 ? (
              <LineChart
                data={stepCountData}
                dataKey="value"
                name="Steps"
                color="#3b82f6"
              />
            ) : (
              <div className="text-center py-8 text-gray-500">No data available</div>
            )}
          </div>
        </div>

        {/* Temperature and Activity Distribution */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Body Temperature Trend */}
          <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
            <h2 className="text-xl font-bold text-gray-900 mb-4">Body Temperature Trend</h2>
            {trendsLoading ? (
              <div className="text-center py-8 text-gray-500">Loading data...</div>
            ) : temperatureData.length > 0 ? (
              <LineChart
                data={temperatureData}
                dataKey="value"
                name="Temperature (°C)"
                color="#f59e0b"
              />
            ) : (
              <div className="text-center py-8 text-gray-500">No data available</div>
            )}
          </div>

          {/* Activity Distribution */}
          <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
            <h2 className="text-xl font-bold text-gray-900 mb-4">Activity Distribution</h2>
            {trendsLoading ? (
              <div className="text-center py-8 text-gray-500">Loading data...</div>
            ) : Object.keys(activityDistribution).length > 0 ? (
              <PieChart data={activityDistribution} />
            ) : (
              <div className="text-center py-8 text-gray-500">No data available</div>
            )}
          </div>
        </div>

        {/* Recent Statistics Summary */}
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
          <h2 className="text-xl font-bold text-gray-900 mb-4">Recent Health Statistics</h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div className="p-4 bg-blue-50 rounded-lg">
              <p className="text-sm text-gray-600">Heart Rate Trend</p>
              <p className="text-lg font-semibold text-gray-900">
                {trends.heart_rate?.trend || 'Stable'}
              </p>
            </div>
            <div className="p-4 bg-green-50 rounded-lg">
              <p className="text-sm text-gray-600">Step Count Trend</p>
              <p className="text-lg font-semibold text-gray-900">
                {trends.step_count?.trend || 'Stable'}
              </p>
            </div>
            <div className="p-4 bg-yellow-50 rounded-lg">
              <p className="text-sm text-gray-600">Period</p>
              <p className="text-lg font-semibold text-gray-900">
                Last {trendsData?.period_days || 7} days
              </p>
            </div>
          </div>
        </div>
      </div>
    </Layout>
  );
};

export default CitizenDashboard;

