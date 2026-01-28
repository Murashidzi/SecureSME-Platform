import { useState, useEffect } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

const Dashboard = () => {
  const [file, setFile] = useState(null);
  const [message, setMessage] = useState('');
  const [username, setUsername] = useState('User');
  const [report, setReport] = useState(null);
  const navigate = useNavigate();

  useEffect(() => {
    // 1. Get Data from Storage
    const token = localStorage.getItem('token');
    const savedName = localStorage.getItem('username');

    // 2. Security Check
    if (!token) {
      navigate('/');
      return;
    }

    // 3. Set State
    if (savedName && savedName !== 'undefined') {
      setUsername(savedName);
    }
  }, [navigate]);

  const handleLogout = () => {
    localStorage.clear();
    navigate('/');
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
    } catch (error) {
      console.error("Upload Error:", error);
      const errorMsg = error.response?.data?.message || error.message;
      setMessage(`Error: ${errorMsg}`);
    }
  };

  // Helper function to color-code threats
  const getSeverityColor = (severity) => {
    if (severity == 'HIGH') return 'bg-red-100 text-red-800 border-red-200';
    if (severity == 'MEDIUM') return 'bg-yellow-100 text-yellow-800 border-yellow-200';
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

        {/* Welcome Section */}
        <div className="mb-8 p-4 bg-blue-50 rounded-lg border border-blue-100">
          <h2 className="text-xl font-semibold text-blue-800">Welcome back, {username}!</h2>
          <p className="text-blue-600 mt-1">System Status: Secure</p>
        </div>

        {/* Upload Section */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          <div className="md:col-span-1">
            <h3 className="text-lg font-semibold mb-4">Upload Evidence</h3>
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
                Analyze File
              </button>
            </div>
            {message && (
              <div className={`mt-4 p-3 rounded text-sm ${message.includes('Error') ? 'bg-red-100 text-red-700' : 'bg-green-100 text-green-700'}`}>
                {message}
              </div>
            )}
          </div>

          {/* RESULTS SECTION (The New Part) */}
          <div className="md:col-span-2">
            <h3 className="text-lg font-semibold mb-4">Threat Intelligence Report</h3>

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
    </div>
  );
};

export default Dashboard;
