from app import db
from datetime import datetime
from sqlalchemy.dialects.postgresql import JSON

class Report(db.Model):
    __tablename__ = 'reports'

    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False)
    upload_date = db.Column(db.DateTime, default=datetime.utcnow)

    # We store the user_id so we know WHO uploaded it
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    # We store the analysis findings as a JSON object (Perfect for lists of threasts)
    findings = db.Column(JSON, nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'filename': self.filename,
            'upload_date': self.upload_date.isoformat(),
            'findings': self.findings
        }
