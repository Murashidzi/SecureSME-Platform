from app import create_app
from app.extensions import celery

# Create the app instance for the worker
app = create_app('dev')
