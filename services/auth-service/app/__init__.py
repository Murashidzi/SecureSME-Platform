from flask import Flask
from .extensions import db, migrate, jwt
from config import config_by_name

def create_app(config_name):
	app = Flask(__name__)
	app.config.from_object(config_by_name[config_name])

	# Initializing extensions
	db.init_app(app)
	migrate.init_app(app, db)
	jwt.init_app(app)

	#Registering blueprints
	from .routes.auth import auth_bp
	app.register_blueprint(auth_bp, url_prefix='/auth')

	return app

