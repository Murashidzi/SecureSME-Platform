from app import create_app
from app.extensions import db
from app.models.log_entry import LogEntry

app = create_app('dev')

with app.app_context():
    print("⏳ Creating database tables...")
    db.create_all()
    print("✅ Tables created successfully.")
