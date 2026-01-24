import os
import uuid
from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required
from werkzeug.utils import secure_filename

file_bp = Blueprint('file', __name__)

# Allowed extentions for Digital Forensics (logs, captures, images)
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'pcap', 'log', 'evtx'}

def allowed_file(filename):
	return '.' in filename and \
		filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@file_bp.route('/upload', methods=['POST'])
@jwt_required()
def upload_file():
	# 1. Check if the request has the file part
	if 'file' not in request.files:
		return jsonify({'message': 'No file part in the request'}), 400

	file = request.files['file']

	# 2. Check if user selected a file
	if file.filename == '':
		return jsonify({'message': 'No file selected'}), 400

	# 3. Validate extension
	if file and allowed_file(file.filename):
		#  Sanitize filename (Prevention: Directory Traversal)
		original_filename = secure_filename(file.filename)

		# 5. Generate unique ID (Prevention: overwriting existing files)
		file_ext = original_filename.rsplit('.', 1)[1].lower()
		unique_filename = f"{uuid.uuid4().hex}.{file_ext}"

		# Use the config we just set
		save_path = os.path.join(current_app.config['UPLOAD_FOLDER'], unique_filename)

		# 6. Save the file
		try:
			# Ensure directory exists inside the container
			os.makedirs(current_app.config['UPLOAD_FOLDER'], exist_ok=True)
			file.save(save_path)

			return jsonify({
				'message': 'File uploaded successfully',
				'file_id': unique_filename,
				'original_name': original_filename
			}), 201
		except Exception as e:
			return jsonify({'message': 'Error saving file', 'error': str(e)}), 500

	return jsonify({'message': 'File type not allowed'}), 400
