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
			const response = await axios.post('/auth/login', {
				email: email,
				password: password
			});
			localStorage.setItem('token', response.data.access_token);
			navigate('/dashboard');
		} catch (err) {
			setError('Invalid email or password.');
		}
	};

	return (
		<div className="min-h-screen bg-gray-100 flex items-center justify-center">
			<div className="max-w-md w-full bg-white rounded-lg shadow-xl p-8">

				{/*Header Section */}
				<div className="text-center mb-8">
					<h2 className="text-3xl font-bold text-gray-800">SecureSME</h2>
					<p className="text-gray-500 mt-2">Sign in to your account</p>
				</div>

				{/* Form Section */}
				<form onSubmit={handleLogin} className="space-y-6">

					{/* Email Input */}
					<div>
						<label className="block text-sm font-medium text-gray-700">
							Email Address
						</label>
						<input
							type="email"
							required
							className="mt-1 block w-full px-4 py-2 border border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500"
							placeholder="you@example.com"
							value={email}
							onChange={(e) => setEmail(e.target.value)}
						/>
					</div>

					{/* Password Input */}
					<div>
						<label className="block text-sm font-medium text-gray-700">
							Password
						</label>
						<input
							type="password"
							required
							className="mt-1 block w-full px-4 py-2 border border-gray-300 round-md shadow-sm focus:ring-blue-500 focus:border-blue-500"
							placeholder="........"
							value={password}
							onChange={(e) => setPassword(e.target.value)}
						/>
					</div>

					{/* Error message */}
					{error && (
						<div classname="bg-red-50 text-red-500 text-sm p-3 rounded-md text-center">
							{error}
						</div>
					)}

					{/* Submit Button */}
					<button
						type="submit"
						className="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 transition-colors"
					>
						Sign In
					</button>
				</form>
			</div>
		</div>
	);
}

export default Login;
