const AlertCard = ({ alert }) => {
  const getSeverityColor = (severity) => {
    switch (severity?.toLowerCase()) {
      case 'high':
        return 'bg-red-100 border-red-500 text-red-800';
      case 'medium':
        return 'bg-yellow-100 border-yellow-500 text-yellow-800';
      case 'low':
        return 'bg-blue-100 border-blue-500 text-blue-800';
      default:
        return 'bg-gray-100 border-gray-500 text-gray-800';
    }
  };

  const getSeverityIcon = (severity) => {
    switch (severity?.toLowerCase()) {
      case 'high':
        return '⚠️';
      case 'medium':
        return '⚡';
      case 'low':
        return 'ℹ️';
      default:
        return '📢';
    }
  };

  return (
    <div className={`border-l-4 rounded-lg p-4 ${getSeverityColor(alert.severity)}`}>
      <div className="flex items-start justify-between">
        <div className="flex-1">
          <div className="flex items-center space-x-2 mb-2">
            <span className="text-xl">{getSeverityIcon(alert.severity)}</span>
            <h3 className="font-semibold text-sm">{alert.type || 'Alert'}</h3>
            <span className="text-xs px-2 py-1 rounded-full bg-white/50">
              {alert.severity || 'Unknown'}
            </span>
          </div>
          <p className="text-sm mb-2">{alert.message}</p>
          {alert.location && (
            <p className="text-xs opacity-75 mb-1">
              <strong>Location:</strong> {alert.location}
            </p>
          )}
          {alert.recommendation && (
            <p className="text-xs mt-2 italic">{alert.recommendation}</p>
          )}
          {alert.timestamp && (
            <p className="text-xs mt-2 opacity-60">
              {new Date(alert.timestamp).toLocaleString()}
            </p>
          )}
        </div>
      </div>
    </div>
  );
};

export default AlertCard;

