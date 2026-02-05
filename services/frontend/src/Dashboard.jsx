import React, { useState, useEffect } from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, PieChart, Pie, Cell } from 'recharts';
import { Upload, Shield, AlertTriangle, FileText, Activity, CheckCircle, Lock } from 'lucide-react';
import axios from 'axios';

const Dashboard = ({ token, role, onLogout }) => {
  const [stats, setStats] = useState([]);
  const [pieData, setPieData] = useState([]);
  const [summary, setSummary] = useState({ total_incidents: 0, top_attacker: 'N/A' });
  const [loading, setLoading] = useState(true);
  const [uploadStatus, setUploadStatus] = useState('');

  const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:5000';

  // Fetch Data on Load
  const fetchStats = async () => {
    try {
      const response = await axios.get(`${apiUrl}/stats`, {
        headers: { 'Authorization': `Bearer ${token}` }
      });

      const data = response.data;
      if (data.chart_data) {
          setStats(data.chart_data);
          setPieData(data.pie_data);
          setSummary(data.summary);
      }
    } catch (err) {
      console.error("Failed to fetch stats", err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchStats();
  }, []);

  const handleFileUpload = async (e) => {
    const file = e.target.files[0];
    if (!file) return;

    setUploadStatus('Uploading & Analyzing...');
    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await axios.post(`${apiUrl}/upload`, formData, {
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'multipart/form-data'
        }
      });

      setUploadStatus('✅ Analysis Complete!');
      // Update charts immediately with the new data
      if (response.data.data) {
          setStats(response.data.data.chart_data);
          setPieData(response.data.data.pie_data);
          setSummary(response.data.data.summary);
      }

    } catch (err) {
      console.error("Upload failed", err);
      const reason = err.response?.data?.msg || err.message || 'Unknown Error';
      setUploadStatus(`❌ Failed: ${reason}`);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 font-sans text-gray-800">
      <nav className="bg-slate-900 text-white shadow-lg sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between h-16 items-center">
            <div className="flex items-center gap-2">
              <Shield className="h-8 w-8 text-blue-400" />
              <span className="text-xl font-bold tracking-tight">SecureSME <span className="text-blue-400">Intel</span></span>
            </div>
            <div className="flex items-center gap-6">
              <div className="hidden md:block text-right">
                <p className="text-xs text-slate-400 uppercase tracking-wider">Operator</p>
                <div className="flex items-center gap-2">
                  <span className={`h-2 w-2 rounded-full ${role === 'admin' ? 'bg-red-500' : 'bg-green-500'}`}></span>
                  <span className="font-semibold capitalize text-sm">{role}</span>
                </div>
              </div>
              <button onClick={onLogout} className="bg-slate-800 hover:bg-slate-700 text-slate-200 px-4 py-2 rounded-md text-sm font-medium transition border border-slate-700">
                Sign Out
              </button>
            </div>
          </div>
        </div>
      </nav>

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* --- KPI Cards --- */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          <div className="bg-white p-6 rounded-xl shadow-sm border border-slate-200">
            <div className="flex justify-between items-start">
              <div><p className="text-sm font-medium text-slate-500">Total Incidents</p><h3 className="text-3xl font-bold text-slate-800 mt-2">{summary.total_incidents}</h3></div>
              <div className="p-2 bg-red-50 rounded-lg"><AlertTriangle className="h-6 w-6 text-red-500" /></div>
            </div>
          </div>
          <div className="bg-white p-6 rounded-xl shadow-sm border border-slate-200">
             <div className="flex justify-between items-start">
              <div><p className="text-sm font-medium text-slate-500">Top Attacker IP</p><h3 className="text-xl font-bold text-slate-800 mt-2">{summary.top_attacker}</h3></div>
              <div className="p-2 bg-blue-50 rounded-lg"><FileText className="h-6 w-6 text-blue-500" /></div>
            </div>
          </div>
           <div className="bg-white p-6 rounded-xl shadow-sm border border-slate-200">
             <div className="flex justify-between items-start">
              <div><p className="text-sm font-medium text-slate-500">System Status</p><h3 className="text-3xl font-bold text-slate-800 mt-2">Active</h3></div>
              <div className="p-2 bg-green-50 rounded-lg"><CheckCircle className="h-6 w-6 text-green-500" /></div>
            </div>
          </div>
        </div>

        {/* --- Charts --- */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          <div className="lg:col-span-2 space-y-8">
            {/* Line Chart */}
            <div className="bg-white p-6 rounded-xl shadow-sm border border-slate-200">
              <h3 className="text-lg font-bold text-slate-800 mb-4">Threat Velocity (Hourly)</h3>
              <div className="h-72 w-full">
                {stats.length > 0 ? (
                  <ResponsiveContainer width="100%" height="100%">
                    <LineChart data={stats}>
                      <CartesianGrid strokeDasharray="3 3" stroke="#f1f5f9" />
                      <XAxis dataKey="name" stroke="#94a3b8" />
                      <YAxis stroke="#94a3b8" />
                      <Tooltip contentStyle={{ backgroundColor: '#1e293b', border: 'none', borderRadius: '8px', color: '#fff' }} itemStyle={{ color: '#fff' }} />
                      <Line type="monotone" dataKey="threats" stroke="#3b82f6" strokeWidth={3} dot={{r: 4, strokeWidth: 2}} activeDot={{r: 8}} />
                    </LineChart>
                  </ResponsiveContainer>
                ) : (
                  <div className="flex h-full items-center justify-center text-gray-400">No data available. Upload a log file.</div>
                )}
              </div>
            </div>

            {/* Pie Chart */}
             <div className="bg-white p-6 rounded-xl shadow-sm border border-slate-200">
              <h3 className="text-lg font-bold text-slate-800 mb-4">Attack Vectors</h3>
              <div className="h-64 w-full flex justify-center">
                 {pieData.length > 0 ? (
                   <ResponsiveContainer width="100%" height="100%">
                      <PieChart>
                        <Pie data={pieData} cx="50%" cy="50%" innerRadius={60} outerRadius={80} paddingAngle={5} dataKey="value">
                          {pieData.map((entry, index) => (<Cell key={`cell-${index}`} fill={entry.color} />))}
                        </Pie>
                        <Tooltip />
                      </PieChart>
                   </ResponsiveContainer>
                 ) : (
                    <div className="flex h-full items-center justify-center text-gray-400">No attack data found.</div>
                 )}
              </div>
              <div className="flex justify-center gap-6 mt-4">
                  {pieData.map((item) => (<div key={item.name} className="flex items-center text-sm text-slate-600"><span className="w-3 h-3 rounded-full mr-2" style={{backgroundColor: item.color}}></span>{item.name}</div>))}
              </div>
            </div>
          </div>

          <div className="space-y-8">
             <div className="bg-white p-6 rounded-xl shadow-sm border border-slate-200">
                <h3 className="text-lg font-bold text-slate-800 mb-4">Upload Evidence</h3>
                <div className="border-2 border-dashed border-slate-300 rounded-lg p-8 text-center hover:bg-slate-50 transition-colors relative">
                   <input type="file" onChange={handleFileUpload} className="absolute inset-0 w-full h-full opacity-0 cursor-pointer" />
                   <div className="flex flex-col items-center">
                      <div className="p-3 bg-blue-100 rounded-full mb-3"><Upload className="h-6 w-6 text-blue-600" /></div>
                      <p className="text-sm font-medium text-slate-700">Click to upload auth.log</p>
                      <p className="text-xs text-slate-500 mt-1">Supports .log, .txt (Max 5MB)</p>
                   </div>
                </div>
                {uploadStatus && (
                  <div className={`mt-4 p-3 rounded-md text-sm text-center font-medium ${uploadStatus.includes('✅') ? 'bg-green-100 text-green-700' : 'bg-blue-100 text-blue-700'}`}>
                    {uploadStatus}
                  </div>
                )}
             </div>
          </div>
        </div>
      </main>
    </div>
  );
};

export default Dashboard;
