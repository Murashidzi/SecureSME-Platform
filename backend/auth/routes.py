from flask import request, jsonify
from werkzeug.security import generate_password_hash
from .__init__ import auth_bp # Import the blueprint
from ..extensions import db 
from ..models.user import User

@auth_bp.route('/register', methods=['POST'])
def register_user():
	data = request.get_json()

	username = data.get('username')
	email = data.get('email')
	password = data.get('password')

	# Basic input validation
	if not username or not email or not password:
		return jsonify({'message': 'Missing username, email or password'}), 400
	if len(password) < 8:
		return jsonify({'message': 'Password must be at least 8 characters long'}), 400

	# Check if username of password already exists
	if User.query.filter_by(email=email).first():
		return jsonify({'message': 'Email already registered'}), 400
	

	hashed_password = generate_password_hash(password)

	new_user = User(username=username, email=email, password_hash=hashed_password)
	db.session.add(new_user)
	db.session.commit()

	return jsonify({'message': 'User registered successfully!'})