import os
from datetime import timedelta

# Use a base directory to make file paths more robust
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
	# -< App Security Settings >-
	# This key is used by flask and its extensions to keep the client-side sessions secure.
	# It should be a long, random string. We will load it from an environment viriable.

	SECRET_KEY = os.environ.get("SECRET_KEY") or "a_very_secret_key_that_should_be_changed_in_production"

	# -< Database Settings >-
	# Disable modification tracking as it's deprecated and adds overhead
	SQLALCHEMY_TRACK_MODIFICATIONS = False


	# -< JSON Web Token (JWT) Settings for Authentication >-
	# Set the secret key for signing JWTs. HAS to be different from SECRET_KEY

	JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'a different-super-secret-jwt-key'
	# Set how long the access tokens are valid for.
	JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
	# Set how long refresh tokens are valid for (because we will implement them later).


class DevelopmentConfig(Config):
	DEBUG = True
	# Connect to the dockerized PostgreSQL database
	SQLALCHEMY_DATABASE_URI = os.environ.get("DEV_DATABASE_URL") or \
	'postgresql://murashidzi:vamurashidzi@localhost:5432/securesme_dev'
	SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-for-testing'
	JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'dev-jwt-secret-key-for-testing'

class TestingConfig(Config):
	TESTING = True
	# Use an in-memory SQLite database for fast tests
	SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
	# Use a different secret key for testing to ensure isolation
	SECRET_KEY = 'test-secret-key'
	JWT_SECRET_KEY = 'test-jwt-secret-key'


class ProductionConfig(Config):
	# -< App Security Settings >-
	# DEBUG must be False in production for security and perfomance.
	DEBUG = False
	# TESTING must be False in production.
	TESTING = False

	# -< Database Settings >-
	# In production, we MUST use a robust database like PostgreSQL.
	# The connection string will be loaded from an environment variable.
	# Example: postgresql://user:password@host:port/dbname
	SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
	if SQLALCHEMY_DATABASE_URI and SQLALCHEMY_DATABASE_URI.startswith('sqlite'):
		raise RuntimeError("Production configuration cannot use a SQLite database.")

	# -<Security Headers & Session Cookie Settings >-
	# Enforce secure cookies (sent only over HTTPS)
	SESSION_COOKIE_SECURE = True
	# Protect against cross-site request forgery (CSRF) on session cookies
	SESSION_COOKIE_HTTPONLY = True
	SESSION_COOKIE_SAMESITE = 'Lax'

	# -< Logging Settings >-
	''' In production, we will configure logging to a file or a logging  servive to ensure we capture errors and important events without cluttering stdout... To be implemented at a later stage '''

	# Dictionary to map environment names to configuration classes
config_by_name = dict (
	dev=DevelopmentConfig,
	test=TestingConfig,
	prod=ProductionConfig
)















