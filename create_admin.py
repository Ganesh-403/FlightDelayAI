# create_admin.py
from app import app, db, bcrypt
from models import User

def create_admin():
    with app.app_context():
        # Check if user already exists
        existing_user = User.query.filter_by(username='admin').first()
        if existing_user:
            print("Admin user already exists.")
            return

        # Create new admin user
        hashed_pw = bcrypt.generate_password_hash('admin123').decode('utf-8')
        admin = User(username='admin', password=hashed_pw, is_admin=True)
        db.session.add(admin)
        db.session.commit()
        print("Admin user created successfully!")
        print("Username: admin")
        print("Password: admin123")

if __name__ == '__main__':
    create_admin()
