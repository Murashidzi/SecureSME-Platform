import { useState } from 'react';
import axios from 'axios';
import {useNavigate } from 'react-router-dom';

const Upload = () => {
	const [file, setFile] = useState(null);
	const [status, setStatus] = useState('');
	const [isUploading, setIsUploading] = useState(false);
	const navigate = useNavigate();

	// 1. Handle file selection
	const handleFileChange = (e) => {
		if (e.target.files) {
			setFile(e.target.files[0]);
			setStatus('');
		}
	};

	// 2. Handle the Upload logic
	const handleUpload = async () => {
		if (!file) {
			setStatus('Please select a file first.');
			return;
		}

		setIsUploading(true);
		setStatus('Uploading...');

	// 3. Prepare the Data payload
	const formData = new FormData();
	formData.append('file', file);

	// 4. Retrieve the token (Authentication)
	const token = localStorage.getItem('token');

	if (!token) {
		setStatus('Error: You are not logged in.');
		setIsUploading(false);
		return;
	}

	try {
		// 5. Send to Backend
		const response = await axios.post('http://localhost:5000/files/upload', formData, {
			headers: {
				'Authorization': 'Bearer ${token"', // Secure Passkey
				'Content-Type': 'multipart/form-data',
			},
		});

		setStatus('Success: ${response.data.message} (ID: ${response.data.file.filed_id})');
		} catch (error) {
			console.error(error);
			const errorMsg = error.response?.data?.message || 'Upload failed.';
			setStatus('Error: ${errorMsg}');
		 } finally {
			setIsUploading(false);
		 }
	};

   return (
    <div className="min-h-screen flex items-center justify-center bg-gray-900">
      <div className="bg-gray-800 p-8 rounded-lg shadow-lg w-full max-w-md border border-gray-700">
        <h2 className="text-2xl font-bold text-white mb-6 text-center">Upload Evidence</h2>

        {/* File Input Area */}
        <div className="mb-6">
          <label className="block mb-2 text-sm font-medium text-gray-300">Select File</label>
          <input
            type="file"
            onChange={handleFileChange}
            className="block w-full text-sm text-gray-400
              file:mr-4 file:py-2 file:px-4
              file:rounded-full file:border-0
              file:text-sm file:font-semibold
              file:bg-blue-600 file:text-white
              hover:file:bg-blue-700
              cursor-pointer bg-gray-700 rounded-lg border border-gray-600"
          />
        </div>

        {/* Upload Button */}
        <button
          onClick={handleUpload}
          disabled={isUploading}
          className={`w-full py-2 px-4 rounded-lg font-semibold text-white transition duration-200
            ${isUploading
              ? 'bg-gray-600 cursor-not-allowed'
              : 'bg-green-600 hover:bg-green-700'}`}
        >
          {isUploading ? 'Uploading...' : 'Secure Upload'}
        </button>

        {/* Status Message */}
        {status && (
          <div className={`mt-4 p-3 rounded text-sm text-center ${
            status.startsWith('Success') ? 'bg-green-900 text-green-200' : 'bg-red-900 text-red-200'
          }`}>
            {status}
          </div>
        )}

        <button
            onClick={() => navigate('/dashboard')}
            className="mt-4 w-full text-sm text-gray-400 hover:text-white"
        >
            &larr; Back to Dashboard
        </button>
      </div>
    </div>
  );
};

export default Upload;
