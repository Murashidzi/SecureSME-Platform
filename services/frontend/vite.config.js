import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vitejs.dev/config/
export default defineConfig({
	plugins: [react()],
	server: {
		proxy: {
			// any request starting with /auth will be sent to the backend
			'/auth': {
				target: 'http://localhost:5000',
				changeOrigin: true,
				secure: false,
			}
		}
	}
})
