from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from celery import Celery

# Define the extensions here, but don't initialize them yet
db = SQLAlchemy()
migrate = Migrate()
celery = Celery()
