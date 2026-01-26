import os
from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.utils import secure_filename

file_bp = Blueprint('file_upload', __name__)

@file_bp.route('/upload', methods=['POST'])
@jwt_required()
def upload_file():
    try:
        # 1. Check if file is present
        if 'file' not in request.files:
            return jsonify({'message': 'No file part'}), 400

        file = request.files['file']
        if file.filename == '':
            return jsonify({'message': 'No selected file'}), 400

        # 2. Create Upload Folder (if it doesn't exist)
        # We save it in the main 'auth-service' directory
        upload_folder = '/app/uploads'
        if not os.path.exists(upload_folder):
            os.makedirs(upload_folder)

        # 3. Save File
        filename = secure_filename(file.filename)
        file_path = os.path.join(upload_folder, filename)
        file.save(file_path)

        return jsonify({'message': 'File uploaded successfully', 'path': file_path}), 200

    except Exception as e:
        print(f"!!! UPLOAD ERROR !!!: {str(e)}")
        return jsonify({'message': 'Upload failed', 'error': str(e)}), 500
