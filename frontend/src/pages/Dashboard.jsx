import { Link } from 'react-router-dom';
import Layout from '../components/Layout';

const Dashboard = () => {
  return (
    <Layout>
      <div className="max-w-4xl mx-auto">
        <div className="text-center mb-12">
          <h1 className="text-4xl font-bold text-gray-900 mb-4">
            Health & Air Quality Dashboard
          </h1>
          <p className="text-xl text-gray-600">
            Monitor your health and air quality data
          </p>
        </div>

        <div className="grid md:grid-cols-2 gap-6">
          {/* Citizen Dashboard Card */}
          <Link
            to="/citizen"
            className="block bg-white rounded-lg shadow-lg hover:shadow-xl transition-shadow p-8 border-2 border-transparent hover:border-blue-500"
          >
            <div className="text-center">
              <div className="w-20 h-20 bg-blue-100 rounded-full flex items-center justify-center mx-auto mb-4">
                <span className="text-4xl">👤</span>
              </div>
              <h2 className="text-2xl font-bold text-gray-900 mb-2">
                Citizen View
              </h2>
              <p className="text-gray-600 mb-4">
                Access your personal health alerts, trends, and predictions
              </p>
              <div className="text-sm text-gray-500 space-y-1">
                <p>✓ Personal health alerts</p>
                <p>✓ Health trends & analytics</p>
                <p>✓ Activity predictions</p>
                <p>✓ Recent statistics</p>
              </div>
              <div className="mt-6">
                <span className="inline-block bg-blue-600 text-white px-6 py-2 rounded-md font-medium">
                  View Dashboard →
                </span>
              </div>
            </div>
          </Link>

          {/* Health Authority Dashboard Card */}
          <Link
            to="/authority"
            className="block bg-white rounded-lg shadow-lg hover:shadow-xl transition-shadow p-8 border-2 border-transparent hover:border-green-500"
          >
            <div className="text-center">
              <div className="w-20 h-20 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-4">
                <span className="text-4xl">🏥</span>
              </div>
              <h2 className="text-2xl font-bold text-gray-900 mb-2">
                Health Authority View
              </h2>
              <p className="text-gray-600 mb-4">
                Monitor public health risks, alerts, and system-wide analytics
              </p>
              <div className="text-sm text-gray-500 space-y-1">
                <p>✓ Public health risk maps</p>
                <p>✓ System-wide alerts</p>
                <p>✓ Community-level predictions</p>
                <p>✓ Advanced monitoring</p>
              </div>
              <div className="mt-6">
                <span className="inline-block bg-green-600 text-white px-6 py-2 rounded-md font-medium">
                  View Dashboard →
                </span>
              </div>
              <p className="text-xs text-gray-400 mt-2">
                Login required
              </p>
            </div>
          </Link>
        </div>

        <div className="mt-12 bg-blue-50 rounded-lg p-6 border border-blue-200">
          <h3 className="text-lg font-semibold text-blue-900 mb-2">
            About This Dashboard
          </h3>
          <p className="text-blue-800 text-sm">
            This dashboard provides real-time monitoring of health metrics and air quality data.
            Citizens can track their personal health trends, while health authorities can monitor
            public health risks and system-wide patterns. All data is sourced from the MLOps API
            and updated in real-time.
          </p>
        </div>
      </div>
    </Layout>
  );
};

export default Dashboard;

