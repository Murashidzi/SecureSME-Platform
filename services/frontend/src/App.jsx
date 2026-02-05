import React, { useState, useEffect } from 'react';
import Login from './Login';
import Dashboard from './Dashboard';

function App() {
  // 1. State to hold the user's login data
  // We check localStorage first so the user stays logged in if they refresh
  const [token, setToken] = useState(localStorage.getItem('token') || '');
  const [role, setRole] = useState(localStorage.getItem('role') || '');

  // 2. Effect: Whenever token/role changes, save it to the browser's storage
  useEffect(() => {
    if (token) {
      localStorage.setItem('token', token);
      localStorage.setItem('role', role);
    } else {
      localStorage.removeItem('token');
      localStorage.removeItem('role');
    }
  }, [token, role]);

  // 3. Logout function (wipes the state)
  const handleLogout = () => {
    setToken('');
    setRole('');
  };

  // 4. The Decision Logic
  // If we DON'T have a token, show the Login Screen.
  // CRITICAL FIX: We must pass 'setToken' and 'setRole' as props here!
  if (!token) {
    return <Login setToken={setToken} setRole={setRole} />;
  }

  // If we DO have a token, show the Dashboard.
  return <Dashboard token={token} role={role} onLogout={handleLogout} />;
}

export default App;
