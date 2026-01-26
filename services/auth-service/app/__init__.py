from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from config import config_by_name
from .extensions import db, migrate

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config_by_name[config_name])

    # Initialize Plugins
    db.init_app(app)
    migrate.init_app(app, db)
    JWTManager(app)  # <--- THIS WAS MISSING!

    # Enable CORS
    CORS(app, resources={r"/*": {"origins": "*"}})

    from .routes.auth import auth_bp
    from .routes.file_upload import file_bp

    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(file_bp, url_prefix='/files')

    return app
