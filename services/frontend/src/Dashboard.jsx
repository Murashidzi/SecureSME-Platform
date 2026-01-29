import { useState, useEffect } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import { PieChart, Pie, Cell, Tooltip, Legend, ResponsiveContainer } from 'recharts';

const Dashboard = () => {
  const [file, setFile] = useState(null);
  const [message, setMessage] = useState('');
  const [username, setUsername] = useState('User');
  const [report, setReport] = useState(null);
  const [chartData, setChartData] = useState([]);
  const navigate = useNavigate();

  useEffect(() => {
    const token = localStorage.getItem('token');
    const savedName = localStorage.getItem('username');

    if (!token) {
      navigate('/');
      return;
    }
    if (savedName && savedName !== 'undefined') {
      setUsername(savedName);
    }
  }, [navigate]);

  const handleLogout = () => {
    localStorage.clear();
    navigate('/');
  };

  const processChartData = (analysis) => {
    const counts = { HIGH: 0, MEDIUM: 0, LOW: 0 };
    analysis.forEach(item => {
      if (counts[item.severity] !== undefined) {
        counts[item.severity]++;
      }
    });

    const data = [
      { name: 'High Severity', value: counts.HIGH, color: '#EF4444' }, // Red-500
      { name: 'Medium Severity', value: counts.MEDIUM, color: '#F59E0B' }, // Yellow-500
      { name: 'Low Severity', value: counts.LOW, color: '#3B82F6' } // Blue-500
    ];

    // Only show segments that have data > 0
    setChartData(data.filter(item => item.value > 0));
  };

  const handleUpload = async () => {
    if (!file) {
      setMessage('Please select a file first.');
      return;
    }

    const formData = new FormData();
    formData.append('file', file);

    try {
      const token = localStorage.getItem('token');

      const response = await axios.post('http://localhost:5000/files/upload', formData, {
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'multipart/form-data'
        }
      });

      setMessage(response.data.message);
      setReport(response.data.analysis);
      processChartData(response.data.analysis); // Generate Chart Data

    } catch (error) {
      console.error("Upload Error:", error);
      const errorMsg = error.response?.data?.message || error.message;
      setMessage(`Error: ${errorMsg}`);
    }
  };

  const getSeverityColor = (severity) => {
    if (severity === 'HIGH') return 'bg-red-100 text-red-800 border-red-200';
    if (severity === 'MEDIUM') return 'bg-yellow-100 text-yellow-800 border-yellow-200';
    return 'bg-blue-100 text-blue-800 border-blue-200';
  };

  return (
    <div className="min-h-screen bg-gray-100 p-8">
      <div className="max-w-6xl mx-auto bg-white rounded-lg shadow-md p-6">

        {/* Header */}
        <div className="flex justify-between items-center mb-8 border-b pb-4">
          <h1 className="text-3xl font-bold text-gray-800">SecureSME Dashboard</h1>
          <button onClick={handleLogout} className="bg-red-500 hover:bg-red-600 text-white px-4 py-2 rounded transition">
            Logout
          </button>
        </div>

        {/* Top Section: Upload & Chart */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8 mb-8">

          {/* Left: Upload Controls */}
          <div className="md:col-span-1 space-y-6">
            <div className="p-4 bg-blue-50 rounded-lg border border-blue-100">
              <h2 className="text-xl font-semibold text-blue-800">Welcome, {username}</h2>
              <p className="text-sm text-blue-600 mt-1">System Status: Active Monitoring</p>
            </div>

            <div className="p-6 border-2 border-dashed border-gray-300 rounded-lg bg-gray-50 text-center">
              <input
                type="file"
                onChange={(e) => setFile(e.target.files[0])}
                className="block w-full text-sm text-gray-500 mb-4 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100"
              />
              <button
                onClick={handleUpload}
                className="w-full bg-blue-600 hover:bg-blue-700 text-white font-bold py-2 px-6 rounded transition"
              >
                Analyze Log
              </button>
            </div>
            {message && (
              <div className={`p-3 rounded text-sm ${message.includes('Error') ? 'bg-red-100 text-red-700' : 'bg-green-100 text-green-700'}`}>
                {message}
              </div>
            )}
          </div>

          {/* Right: Visual Analytics (The Chart) */}
          <div className="md:col-span-2 flex flex-col justify-center items-center bg-gray-50 rounded-lg border border-gray-200 p-4">
            <h3 className="text-lg font-semibold mb-2 text-gray-700">Threat Severity Distribution</h3>
            {chartData.length > 0 ? (
              <div className="w-full h-64">
                <ResponsiveContainer width="100%" height="100%">
                  <PieChart>
                    <Pie
                      data={chartData}
                      cx="50%"
                      cy="50%"
                      innerRadius={60}
                      outerRadius={80}
                      paddingAngle={5}
                      dataKey="value"
                    >
                      {chartData.map((entry, index) => (
                        <Cell key={`cell-${index}`} fill={entry.color} />
                      ))}
                    </Pie>
                    <Tooltip />
                    <Legend verticalAlign="bottom" height={36}/>
                  </PieChart>
                </ResponsiveContainer>
              </div>
            ) : (
              <div className="text-gray-400 italic h-64 flex items-center">
                No data to visualize yet.
              </div>
            )}
          </div>
        </div>

        {/* Bottom Section: Detailed Table */}
        <div>
          <h3 className="text-lg font-semibold mb-4">Detailed Intelligence Report</h3>
          {!report ? (
            <div className="text-gray-500 italic p-8 border rounded-lg bg-gray-50 flex items-center justify-center">
              Waiting for analysis... Upload a log file to begin.
            </div>
          ) : (
            <div className="overflow-hidden border rounded-lg shadow-sm">
              <table className="min-w-full bg-white">
                <thead className="bg-gray-100">
                  <tr>
                    <th className="py-3 px-4 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Severity</th>
                    <th className="py-3 px-4 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Line</th>
                    <th className="py-3 px-4 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Threat Type</th>
                    <th className="py-3 px-4 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Content</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-gray-200">
                  {report.map((item, index) => (
                    <tr key={index} className="hover:bg-gray-50">
                      <td className="py-3 px-4 whitespace-nowrap">
                        <span className={`px-2 inline-flex text-xs leading-5 font-semibold rounded-full ${getSeverityColor(item.severity)}`}>
                          {item.severity}
                        </span>
                      </td>
                      <td className="py-3 px-4 text-sm text-gray-500">{item.line}</td>
                      <td className="py-3 px-4 text-sm font-medium text-gray-900">{item.description}</td>
                      <td className="py-3 px-4 text-sm text-gray-500 font-mono truncate max-w-xs" title={item.content}>
                        {item.content}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </div>

      </div>
    </div>
  );
};

export default Dashboard;
