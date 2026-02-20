from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
import os
from app.tasks import process_log_upload  # Import the new Celery task

api_bp = Blueprint('api', __name__)

UPLOAD_FOLDER = '/app/uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@api_bp.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if file:
        filename = secure_filename(file.filename)
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)

        # ASYNC MAGIC HAPPENS HERE
        # We use .delay() to send the task to Redis.
        # The API responds IMMEDIATELY, instead of waiting for parsing.
        task = process_log_upload.delay(filepath)

        return jsonify({
            "message": "File uploaded successfully. Processing started in background.",
            "task_id": task.id
        }), 202

from flask import request
import uuid

@api_bp.route('/ebpf-alert', methods=['POST'])
def receive_ebpf_alert():
    """
    Ingests high-fidelity kernel alerts directly from the eBPF Agent.
    """
    data = request.json
    if not data:
        return jsonify({"error": "Invalid payload"}), 400

    # Extract threats
    pid = data.get('pid')
    parent_comm = data.get('parent_comm')
    executed_cmd = data.get('executed_cmd')
    mitre_tactic = data.get('mitre_tactic', 'T1059')

    # Construct a raw log string that fits our existing LogEntry model
    # Format: "eBPF ALERT | PID: 123 | Parent:sh | Cmd:/usr/bin/wget"
    raw_log = f"eBPF ALERT | PID:{pid} | Parent:{parent_comm} | Cmd:{executed_cmd}"

    """
    For now, we reuse the existing process_log_upload worker logic
    by simulating a tiny log file, or we can just save it directly.
    To be fast, let's save it directly to the Db so it shows on the dashboard.
    """

    from app.models.log_entry import LogEntry
    from app.extensions import db
    from datetime import datetime

    new_alert = LogEntry(
        ip_address="Kernel-Agent", # It's a local system event
        timestamp=datetime.now().strftime("%b %d %H:%M:%S"),
        attack_type=f"Runtime Threat ({mitre_tactic})",
        raw_log=raw_log
    )

    try:
        db.session.add(new_alert)
        db.session.commit()

        # Trigger the town crier in the API log
        print(f" [API] Received Kernel Alert: {raw_log}", flush=True)

        return jsonify({"status": "success", "message": "Kernel alert ingested"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
