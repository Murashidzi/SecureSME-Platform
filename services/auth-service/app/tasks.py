import time
import os
from app.extensions import celery, db  # <--- FIXED: Import from extensions
from app.log_parser import parse_log_file
from app.models.log_entry import LogEntry

@celery.task(bind=True)
def process_log_upload(self, filepath):
    print(f"🔧 [Worker] Starting processing for: {filepath}")

    # Simulate processing time
    time.sleep(2)

    try:
        if not os.path.exists(filepath):
            print(f"❌ [Worker] File not found: {filepath}")
            return {"status": "error", "message": "File missing"}

        parsed_data = parse_log_file(filepath)

        entries = []
        for row in parsed_data:
            entry = LogEntry(
                ip_address=row['ip'],
                timestamp=row['timestamp'],
                attack_type=row['attack_type'],
                raw_log=row['raw']
            )
            entries.append(entry)

        db.session.bulk_save_objects(entries)
        db.session.commit()

        # Alerting Logic
        high_risk_count = sum(1 for r in parsed_data if r['attack_type'] == 'Root Access Attempt')
        total_attacks = len(parsed_data)

        alert_status = "No Alerts"
        if high_risk_count > 0 or total_attacks > 50:
            alert_status = trigger_alert(total_attacks, high_risk_count)

        print(f"✅ [Worker] Finished. Processed {total_attacks} lines. Status: {alert_status}")
        return {"status": "completed", "attacks": total_attacks, "alert": alert_status}

    except Exception as e:
        print(f"❌ [Worker] Error: {str(e)}")
        return {"status": "failed", "error": str(e)}

def trigger_alert(total, high_risk):
    alert_msg = f"🚨 SECURITY ALERT: Detected {total} attacks ({high_risk} CRITICAL root attempts)."
    print("\n" + "="*50)
    print(alert_msg)
    print("📧 Sending notification to admin@securesme.com...")
    print("="*50 + "\n")
    return "Alert Sent"
