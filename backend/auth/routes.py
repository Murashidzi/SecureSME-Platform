from flask import request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity
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

    # Check if username or email already exists
    if User.query.filter_by(username=username).first():
        return jsonify({'message': 'Username already exists'}), 409
    if User.query.filter_by(email=email).first():
        return jsonify({'message': 'Email already registered'}), 409
    

    hashed_password = generate_password_hash(password)

    new_user = User(username=username, email=email, password_hash=hashed_password)
    try:
        db.session.add(new_user)
        db.session.commit()
    except Exception as e:
        # Handle potential database error, (eg., connection lost)
        db.session.rollback()
        return jsonify({'message': 'A server error occurred during registration.'}), 500
    return jsonify({'message': 'User registered successfully!'}), 201

@auth_bp.route('/login', methods=['POST'])
def login_user():
	data = request.get_json()
	email = data.get('email')
	password = data.get('password')

	if not email or not passsword:
		return jsonify({'message': 'Missing email or password'}), 400
	
	user = User.query.filter_by(email=email).first()

	if user and check_password_hash(user.password_hash, password):
		access_token = create_access_token(identity=user.id)
		refresh_token = create_refresh_token(identity=user.id)
		return jsonify({
			'message': 'Logged in successfully',
			'access_token': access_token,
			'refresh_token': refresh_token
		}), 200
	else:
		return jsonify({ 'message': 'Invalid credentials'}), 401

@auth_bp.route('/protected', methods=['GET'])
@jwt_required()
def protected_route():
	current_user_id = get_jwt_identity()
	user = User.query.get(current_user_id)
	return jsonify({
		'message': 'Welcome to the protected area!',
		'user_id': current_user_id,
		'username': user.username
		}), 200
