from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager

db = SQLAlchemy() # Initialize SQLAlchemy
migrate = Migrate() # Initialize Flask-Migrate
jwt = JWTManager()