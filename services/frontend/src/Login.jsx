import { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

function Login() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const handleLogin = async (e) => {
    e.preventDefault();
    try {
      // We send the request to /auth/login.
      // The Vite Proxy forwards this to http://localhost:5000/auth/login
      const response = await axios.post('/auth/login', {
        email: email,
        password: password
      });

      // 1. Success! Save the token in the browser's memory
      localStorage.setItem('token', response.data.access_token);
      
      // 2. Move the user to the dashboard
      navigate('/dashboard');
      
    } catch (err) {
      setError('Login failed. Check your password.');
      console.error(err);
    }
  };

  return (
    <div style={{ padding: '50px' }}>
      <h2>SecureSME Login</h2>
      <form onSubmit={handleLogin}>
        <div>
          <input 
            type="email" 
            placeholder="Email" 
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required 
            style={{ padding: '10px', margin: '10px 0', width: '100%' }}
          />
        </div>
        <div>
          <input 
            type="password" 
            placeholder="Password" 
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required 
            style={{ padding: '10px', margin: '10px 0', width: '100%' }}
          />
        </div>
        <button type="submit" style={{ padding: '10px 20px', cursor: 'pointer' }}>
          Log In
        </button>
      </form>
      {error && <p style={{ color: 'red' }}>{error}</p>}
    </div>
  );
}

export default Login;
