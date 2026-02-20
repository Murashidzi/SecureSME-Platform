from flask import Flask
from flask_cors import CORS
from app.config import Config
from app.extensions import db, migrate, celery

def create_app(config_name='default'):
    # We rename the variable to 'server' to avoid any 'app' naming confusion
    server = Flask(__name__)
    server.config.from_object(Config)

    # 1. Initialize Extensions
    db.init_app(server)
    migrate.init_app(server, db)
    CORS(server)

    # 2. Initialize Celery
    celery.conf.update(server.config)
    celery.conf.broker_url = server.config.get('CELERY_BROKER_URL', 'redis://redis:6379/0')
    celery.conf.result_backend = server.config.get('CELERY_RESULT_BACKEND', 'redis://redis:6379/0')

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with server.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask

    # 3. Register Blueprints
    from app.routes.api import api_bp
    server.register_blueprint(api_bp, url_prefix='/api')

    from app.routes.auth import auth_bp
    server.register_blueprint(auth_bp, url_prefix='/auth')

    # 4. Import Tasks
    with server.app_context():
        import app.tasks

    return server
