import { useState, useEffect } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

const Dashboard = () => {
  const [file, setFile] = useState(null);
  const [message, setMessage] = useState('');
  const [username, setUsername] = useState('User');
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

      setMessage('Success: ' + response.data.message);
    } catch (error) {
      console.error("Upload Error:", error);
      const errorMsg = error.response?.data?.message || error.message;
      // FIX: Use backticks for template literals
      setMessage(`Error: ${errorMsg}`);
    }
  };

  return (
    <div className="min-h-screen bg-gray-100 p-8">
      <div className="max-w-4xl mx-auto bg-white rounded-lg shadow-md p-6">
        <div className="flex justify-between items-center mb-8">
          <h1 className="text-3xl font-bold text-gray-800">SecureSME Dashboard</h1>
          <button
            onClick={handleLogout}
            className="bg-red-500 hover:bg-red-600 text-white px-4 py-2 rounded transition"
          >
            Logout
          </button>
        </div>

        <div className="mb-8 p-4 bg-blue-50 rounded-lg border border-blue-100">
          <h2 className="text-xl font-semibold text-blue-800">
            Welcome back, {username}!
          </h2>
          <p className="text-blue-600 mt-1">You are securely logged in.</p>
        </div>

        <div className="border-t pt-6">
          <h3 className="text-lg font-semibold mb-4">Evidence Upload</h3>

          <div className="flex gap-4 items-center">
            <input
              type="file"
              onChange={(e) => setFile(e.target.files[0])}
              className="block w-full text-sm text-gray-500
                file:mr-4 file:py-2 file:px-4
                file:rounded-full file:border-0
                file:text-sm file:font-semibold
                file:bg-blue-50 file:text-blue-700
                hover:file:bg-blue-100"
            />
            <button
              onClick={handleUpload}
              className="bg-green-600 hover:bg-green-700 text-white font-bold py-2 px-6 rounded transition"
            >
              Secure Upload
            </button>
          </div>

          {message && (
            <div className={`mt-4 p-3 rounded ${message.includes('Error') ? 'bg-red-100 text-red-700' : 'bg-green-100 text-green-700'}`}>
              {message}
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
