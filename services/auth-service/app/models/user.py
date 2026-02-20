from app.extensions import db

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)

    # Commented out to fix the "Report not found" error until we build the Report model
    # reports = db.relationship('Report', backref='user', lazy=True)

    def __repr__(self):
        return f'<User {self.username}>'
