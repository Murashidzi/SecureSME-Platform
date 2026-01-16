import os
from flask.cli import FlaskGroup
from app import create_app, db
from app.models.user import User

# Get the environment from the FLASK_ENV environment variable, default to 'dev'
config_name = os.getenv('FLASK_ENV', 'dev')
app = create_app(config_name)

# Create a FlaskGroup instance to extend the Flask CLI
cli = FlaskGroup(app)

# Add shell context for easy access to db and models in 'flask shell'
@app.shell_context_processor
def make_shell_context():
    return dict(db=db, User=User)

if __name__ == '__main__':
    cli()
