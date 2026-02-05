import os
import json
from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.log_parser import parse_auth_log
from app.models.report import Report
from app.models.user import User
from app import db

api_bp = Blueprint('api', __name__)

ALLOWED_EXTENSIONS = {'log', 'txt'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@api_bp.route('/upload', methods=['POST'])
@jwt_required()
def upload_file():
    if 'file' not in request.files:
        return jsonify({"msg": "No file part"}), 400

    file = request.files['file']

    if file.filename == '' or not allowed_file(file.filename):
        return jsonify({"msg": "Invalid file"}), 400

    filename = secure_filename(file.filename)

    # Save File
    upload_folder = '/app/uploads'
    if not os.path.exists(upload_folder):
        os.makedirs(upload_folder)

    filepath = os.path.join(upload_folder, filename)
    file.save(filepath)

    # --- TRIGGER THE ANALYSIS ENGINE ---
    print(f"🕵️‍♂️ Analyzing {filename}...")
    analysis_results = parse_auth_log(filepath)

    if not analysis_results:
        return jsonify({"msg": "Failed to parse log file"}), 500

    # FIX IS HERE: Get the user ID from the token!
    current_user_id = get_jwt_identity()

    new_report = Report(
        filename=filename,
        user_id=int(current_user_id),
        status='completed',
        findings=analysis_results
    )

    db.session.add(new_report)
    db.session.commit()

    return jsonify({
        "msg": "Analysis Complete",
        "data": analysis_results
    }), 200

@api_bp.route('/stats', methods=['GET'])
@jwt_required()
def get_stats():
    # Fetch the LATEST report for the current user
    current_user_id = get_jwt_identity()

    latest_report = Report.query.filter_by(user_id=int(current_user_id))\
        .order_by(Report.upload_date.desc())\
        .first()

    if latest_report:
        return jsonify(latest_report.findings), 200
    else:
        return jsonify({
            "summary": {"total_incidents": 0, "top_attacker": "None"},
            "chart_data": [],
            "pie_data": []
        }), 200
