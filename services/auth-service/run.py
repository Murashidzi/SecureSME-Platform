import sys
import time
from sqlalchemy.exc import OperationalError
from app import create_app, db

# Create the application
application = create_app('dev')

if __name__ == '__main__':
    # DEBUG: Print the type to prove it is a Flask object
    print(f"DEBUG: 'application' type is: {type(application)}", flush=True)

    if not hasattr(application, 'app_context'):
        print("❌ CRITICAL ERROR: 'application' is not a Flask object!", flush=True)
        sys.exit(1)

    print("🚀 API Container Starting...", flush=True)

    with application.app_context():
        print("⏳ Checking Database Connection...", flush=True)
        connected = False
        for i in range(15):
            try:
                db.engine.connect()
                print("✅ Database is ready!", flush=True)
                connected = True
                break
            except OperationalError:
                print(f"⚠️ Waiting for DB (Attempt {i+1}/15)...", flush=True)
                time.sleep(2)
            except Exception as e:
                print(f"❌ Unexpected Error: {e}", flush=True)
                time.sleep(2)

    # Start the Server
    application.run(host='0.0.0.0', port=5000)  # nosec B104
