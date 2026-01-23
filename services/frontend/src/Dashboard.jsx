import { useEffect, useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

function Dashboard() {
  const [message, setMessage] = useState('Loading...');
  const navigate = useNavigate();

  useEffect(() => {
    // 1. Get the token from storage
    const token = localStorage.getItem('token');

    if (!token) {
      navigate('/'); // Kick them out if no token
      return;
    }

    // 2. Ask the backend for data, showing the token as ID
    axios.get('/auth/dashboard', {
      headers: {
        Authorization: `Bearer ${token}`
      }
    })
    .then(response => {
      setMessage(response.data.message);
    })
    .catch(error => {
      setMessage('Access Denied');
      localStorage.removeItem('token'); // Delete invalid token
      setTimeout(() => navigate('/'), 2000);
    });
  }, [navigate]);

  return (
    <div style={{ padding: '50px' }}>
      <h1>Dashboard</h1>
      <div style={{ padding: '20px', border: '1px solid #ccc', borderRadius: '8px' }}>
        <h3>Status: {message}</h3>
      </div>
      <button 
        onClick={() => {
          localStorage.removeItem('token');
          navigate('/');
        }}
        style={{ marginTop: '20px', padding: '10px' }}
      >
        Log Out
      </button>
    </div>
  );
}

export default Dashboard;
