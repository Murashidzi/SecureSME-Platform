from app.extensions import db

class LogEntry(db.Model):
    __tablename__ = 'log_entries'

    id = db.Column(db.Integer, primary_key=True)
    ip_address = db.Column(db.String(50), nullable=False)
    timestamp = db.Column(db.String(50), nullable=False)
    attack_type = db.Column(db.String(50), nullable=False)
    raw_log = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    def __repr__(self):
        return f'<LogEntry {self.ip_address} - {self.attack_type}>'
