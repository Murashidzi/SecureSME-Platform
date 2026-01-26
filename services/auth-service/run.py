import os
from app import create_app, db
from flask_migrate import Migrate

# Force 'dev' environment
app = create_app('dev')
migrate = Migrate(app, db)

if __name__ == '__main__':
	# Get debug status from environment variable (Defaults to False for security)
	debug_mode = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'

	# FORCE DEBUG MODE ON - This will print the error!
	# Run the app
	# nosec B104: We bind to 0.0.0.0 because this is running inside a Docker container.
	app.run(host='0.0.0.0', port=5000, debug=debug_mode) # nosec
