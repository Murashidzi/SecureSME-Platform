from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


db = SQLAlchemy() # Initialize SQLAlchemy
migrate = Migrate() # Initialize Flask-Migrate