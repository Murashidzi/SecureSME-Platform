import React, { useState } from 'react';
import axios from 'axios';

const Login = ({ setToken, setRole }) => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      // In production, use the relative path (proxy) or env var
      const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:5000';
      const response = await axios.post(`${apiUrl}/auth/login`, {
        email,
        password
      });
      setToken(response.data.access_token);
      setRole(response.data.role);
    } catch (err) {
      setError('Invalid credentials');
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-100">
      <div className="max-w-md w-full bg-white p-8 rounded shadow-md">
        <h2 className="text-2xl font-bold mb-6 text-center text-gray-800">SecureSME Login</h2>

        {error && <div className="mb-4 text-red-500 text-center">{error}</div>}

        <form onSubmit={handleSubmit}>
          <div className="mb-4">
            <label className="block text-gray-700 text-sm font-bold mb-2">Email</label>
            <input
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              className="w-full p-2 border rounded focus:outline-none focus:ring-2 focus:ring-blue-500"
              required
            />
          </div>
          <div className="mb-6">
            <label className="block text-gray-700 text-sm font-bold mb-2">Password</label>
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="w-full p-2 border rounded focus:outline-none focus:ring-2 focus:ring-blue-500"
              required
            />
          </div>
          <button
            type="submit"
            className="w-full bg-blue-600 text-white p-2 rounded hover:bg-blue-700 transition duration-200"
          >
            Sign In
          </button>
        </form>

        {/* Demo Credentials Box */}
        <div className="mt-6 p-4 bg-blue-50 border border-blue-200 rounded text-sm text-gray-700">
          <p className="font-bold mb-2">👀 Recruiter / Demo Access:</p>
          <div className="mb-2">
            <span className="font-semibold">Admin (View Charts):</span><br/>
            <code>admin@example.com</code> / <code>adminpass123</code>
          </div>
          <div>
            <span className="font-semibold">Analyst (Upload Only):</span><br/>
            <code>final@example.com</code> / <code>securepassword123</code>
          </div>
        </div>

      </div>
    </div>
  );
};

export default Login;
