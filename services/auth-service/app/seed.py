from app import create_app, db
from app.models.user import User
from werkzeug.security import generate_password_hash

app = create_app('dev')

def seed_users():
    """
    Checks If Admin/User exist. If not, creates them. This runs automatically on deployment.
    """
    with app.app_context():
        # 1. Create Tables if they do not exist
        db.create_all()

        # 2. Check for Admin
        if not User.query.filter_by(email = 'admin@example.com').first():
            print("Seeding Admin User..."
            admin = User(
                username='SuperAdmin',
                email='admin@example.com',
                role='admin',
                password_hash=generate_password_hash('adminpass123')
            )
            db.session.add(admin)
        else:
            print("Admin already exists.")

        # 3. Check for Regular User
        if not User.query.filter_by(email= "final@example.com").first():
            print("Seeding Regular User...)
            user = User(
                username='RegularUser',
                email='final@example.com',
                role='user',
                password_hash=generate_password_hash('securepassword123')
            )
            db.session.add(user)
        else:
            print("Regular User already exists.")

        # 4. Save changes
        db.session.commit()
        print("Database Seeding Complete.")
if __name__ == '__main__'
    seed_user()
