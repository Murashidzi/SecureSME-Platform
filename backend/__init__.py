from flask import Flask
from .config import config_by_name
from .extensions import db, migrate
from .models import user


def create_app(config_name='dev'):
	"""
    Flask application factory function.
    Initializes the app and loads configuration based on the environment name.
    """
	app = Flask(__name__)
	# Load the configuration from the config.py file
	app.config.from_object(config_by_name[config_name])
	
	db.init_app(app) # Initialize db with the app
	migrate.init_app(app, db) # Initialize migrate with the app and db


	# -< We will Register Blueprints here later >-
	
	# Simple test route to confirm the app is running
	@app.route('/')
	def hello_world():
		return f"Hello from the {config_name.upper()} environment!"
		
	return app
