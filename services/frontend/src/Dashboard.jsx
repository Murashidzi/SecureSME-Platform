import { useState, useEffect } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import { PieChart, Pie, Cell, Tooltip, Legend, ResponsiveContainer } from 'recharts';

const Dashboard = () => {
  const [file, setFile] = useState(null);
  const [message, setMessage] = useState('');
  const [username, setUsername] = useState('User');
  const [role, setRole] = useState('user'); // New State
  const [report, setReport] = useState(null);
  const [chartData, setChartData] = useState([]);
  const navigate = useNavigate();

  useEffect(() => {
    const token = localStorage.getItem('token');
    const savedName = localStorage.getItem('username');
    const savedRole = localStorage.getItem('role'); // Get Role

    if (!token) {
      navigate('/');
      return;
    }
    if (savedName) setUsername(savedName);
    if (savedRole) setRole(savedRole);
  }, [navigate]);

  const handleLogout = () => {
    localStorage.clear();
    navigate('/');
  };

  const processChartData = (analysis) => {
    const counts = { HIGH: 0, MEDIUM: 0, LOW: 0 };
    analysis.forEach(item => {
      if (counts[item.severity] !== undefined) counts[item.severity]++;
    });

    const data = [
      { name: 'High', value: counts.HIGH, color: '#EF4444' },
      { name: 'Medium', value: counts.MEDIUM, color: '#F59E0B' },
      { name: 'Low', value: counts.LOW, color: '#3B82F6' }
    ];
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
        headers: { 'Authorization': `Bearer ${token}`, 'Content-Type': 'multipart/form-data' }
      });
      setMessage(response.data.message);
      setReport(response.data.analysis);
      processChartData(response.data.analysis);
    } catch (error) {
      setMessage(`Error: ${error.message}`);
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
          <div>
            <h1 className="text-3xl font-bold text-gray-800">SecureSME Dashboard</h1>
            <span className={`text-xs font-bold uppercase px-2 py-1 rounded ml-1 ${role === 'admin' ? 'bg-purple-100 text-purple-800' : 'bg-gray-100 text-gray-800'}`}>
              {role} View
            </span>
          </div>
          <button onClick={handleLogout} className="bg-red-500 hover:bg-red-600 text-white px-4 py-2 rounded transition">Logout</button>
        </div>

        {/* Main Content */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8 mb-8">

          {/* Upload Section (Visible to ALL) */}
          <div className="md:col-span-1 space-y-6">
            <div className="p-4 bg-blue-50 rounded-lg border border-blue-100">
              <h2 className="text-xl font-semibold text-blue-800">Hello, {username}</h2>
              <p className="text-sm text-blue-600 mt-1">Status: Online</p>
            </div>
            <div className="p-6 border-2 border-dashed border-gray-300 rounded-lg bg-gray-50 text-center">
              <input type="file" onChange={(e) => setFile(e.target.files[0])} className="block w-full text-sm text-gray-500 mb-4"/>
              <button onClick={handleUpload} className="w-full bg-blue-600 hover:bg-blue-700 text-white font-bold py-2 px-6 rounded transition">Analyze Log</button>
            </div>
            {message && <div className="p-3 bg-green-100 text-green-700 rounded text-sm">{message}</div>}
          </div>

          {/* Admin Analytics (Visible ONLY to Admin) */}
          <div className="md:col-span-2 flex flex-col justify-center items-center bg-gray-50 rounded-lg border border-gray-200 p-4 relative">

            {role !== 'admin' && (
              <div className="absolute inset-0 bg-white bg-opacity-90 flex flex-col items-center justify-center z-10 rounded-lg">
                <svg className="w-12 h-12 text-gray-400 mb-2" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z"></path></svg>
                <p className="text-gray-500 font-semibold">Analytics Locked</p>
                <p className="text-xs text-gray-400">Admin privileges required</p>
              </div>
            )}

            <h3 className="text-lg font-semibold mb-2 text-gray-700">Global Threat Intelligence</h3>
            {chartData.length > 0 ? (
              <div className="w-full h-64">
                <ResponsiveContainer width="100%" height="100%">
                  <PieChart>
                    <Pie data={chartData} cx="50%" cy="50%" innerRadius={60} outerRadius={80} paddingAngle={5} dataKey="value">
                      {chartData.map((entry, index) => <Cell key={`cell-${index}`} fill={entry.color} />)}
                    </Pie>
                    <Tooltip />
                    <Legend verticalAlign="bottom"/>
                  </PieChart>
                </ResponsiveContainer>
              </div>
            ) : (
              <div className="text-gray-400 italic h-64 flex items-center">No data available</div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
