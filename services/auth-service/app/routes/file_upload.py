import os
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from werkzeug.utils import secure_filename

# Import our new Brain!
from app.utils.log_parser import analyze_log

file_bp = Blueprint('file_upload', __name__)

@file_bp.route('/upload', methods=['POST'])
@jwt_required()
def upload_file():
    try:
        # 1. Basic Validation
        if 'file' not in request.files:
            return jsonify({'message': 'No file part'}), 400

        file = request.files['file']
        if file.filename == '':
            return jsonify({'message': 'No selected file'}), 400

        # 2. Save the file
        upload_folder = '/app/uploads'
        if not os.path.exists(upload_folder):
            os.makedirs(upload_folder)

        filename = secure_filename(file.filename)
        file_path = os.path.join(upload_folder, filename)
        file.save(file_path)

        # 3. TRIGGER THE ANALYSIS
        # We pass the path of the saved file to our parser
        analysis_report = analyze_log(file_path)

        # 4. Return the report to the Frontend
        return jsonify({
            'message': 'File uploaded and analyzed successfully',
            'path': file_path,
            'analysis': analysis_report # sending the results back!
        }), 200

    except Exception as e:
        print(f"!!! UPLOAD ERROR !!!: {str(e)}")
        return jsonify({'message': 'Upload failed', 'error': str(e)}), 500
