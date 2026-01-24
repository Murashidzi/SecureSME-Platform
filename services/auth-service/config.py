import os

class Config:
	# load from Environment, fail is not set (strict security)
	# or use a safe default only for development
	SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-key-please-change')
	JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'dev-jwt-key-please-change')

	SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'postgresql://user:password@db:5432/securesme_db')
	SQLALCHEMY_TRACK_MODIFICATIONS = False

	# File Upload Config
	UPLOAD_FOLDER = '/app/uploads'
	MAX_CONTENT_LENGTH = 16 * 1024 * 1024 # Limit to 16MB per file
class DevelopmentConfig(Config):
	DEBUG = True

class TestConfig(Config):
	TESTING = True
	SQLACHEMY_DATABASE_URI = 'sqlite:///:memory:'

	# It is okay to hardcode in TestConfig IF it overrides the main Config
	SECRET_KEY = 'test-secret-key' # nosec
	JWT_SECRET_KEY = 'test-jwt-secret-key' #nosec
config_by_name = {
	'dev': DevelopmentConfig,
	'test': TestConfig,
	'prod': Config
}
