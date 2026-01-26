from flask import Blueprint, request, jsonify
from app.models.user import User
from flask_jwt_extended import create_access_token, create_refresh_token
import traceback

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()

        # Validate Input
        if not data or not data.get('email') or not data.get('password'):
            return jsonify({'message': 'Missing email or password'}), 400

        # Find User
        user = User.query.filter_by(email=data['email']).first()

        # Check Password
        if user and user.check_password(data['password']):
            access_token = create_access_token(identity=str(user.id))

            # --- THE KITCHEN SINK RESPONSE ---
            # We send data in every format so the Frontend can't miss it.
            return jsonify({
                'message': 'Login successful',

                # 1. Flat Tokens
                'access_token': access_token,
                'token': access_token,

                # 2. Flat User Data
                'username': user.username,
                'user_id': user.username,
                'email': user.email,

                # 3. Nested User Object (Common in React)
                'user': {
                    'username': user.username,
                    'name': user.username,
                    'id': user.id,
                    'email': user.email,
                    'role': 'admin'
                }
            }), 200

        return jsonify({'message': 'Invalid credentials'}), 401

    except Exception as e:
        print(f"!!! LOGIN CRASH !!!: {str(e)}")
        traceback.print_exc()
        return jsonify({'message': 'Backend Crash', 'error': str(e)}), 500

@auth_bp.route('/me', methods=['GET'])
def me():
    return jsonify({'message': 'User endpoint working'}), 200
