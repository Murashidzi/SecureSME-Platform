import os

class Config:
    SECRET_KEY =  'dev-key-please-change-to-something-secure'
    JWT_SECRET_KEY = 'this-is-a-very-strong-and-long-secret-key-for-jwt-security'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'postgresql://postgres:password@securesme_db:5432/securesme'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
