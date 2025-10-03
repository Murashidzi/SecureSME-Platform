import os
from . import create_app

# Get the environment from the FLASK_ENV evironment variable, default to 'dev'
config_name = os.getenv('FLASK_ENV', 'dev')
app = create_app(config_name)

if __name__ == '__main__':
	app.run()