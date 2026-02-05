from flask import Blueprint, request, jsonify
from app.models.user import User
from app import db
from werkzeug.security import check_password_hash
from flask_jwt_extended import create_access_token
import datetime

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({"msg": "Missing email or password"}), 400

    user = User.query.filter_by(email=email).first()

    if user and check_password_hash(user.password_hash, password):
        # Create token (expires in 1 day)
        access_token = create_access_token(identity=str(user.id), expires_delta=datetime.timedelta(days=1))

        return jsonify({
            "msg": "Login Successful",
            "access_token": access_token,
            "role": user.role
        }), 200

    return jsonify({"msg": "Invalid credentials"}), 401
