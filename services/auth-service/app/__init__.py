from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from app.config import Config

db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()

def create_app(config_name='dev'):
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    CORS(app)

    @jwt.invalid_token_loader
    def invalid_token_callback(error_string):
        print(f"JWT INVALID ERROR: {error_string}")
        return jsonify({"msg": f"Invalid Token: {error_string}"}), 422

    @jwt.unauthorized_loader
    def missing_token_callback(error_string):
        print(f"JWT MISSING ERROR: {error_string}")
        return jsonify({"msg": "Missing Authorization Header"}), 401

    from app.models.user import User
    from app.models.report import Report

    from app.auth import auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    from app.api import api_bp
    app.register_blueprint(api_bp)

    return app
