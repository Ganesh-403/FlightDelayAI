from flask import Blueprint, render_template, request, redirect, flash, url_for
from flask_bcrypt import Bcrypt
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user
from models import db, User, Prediction

setup_admin_bp = Blueprint('setup_admin', __name__)
bcrypt = Bcrypt()

# 🔹 Admin Panel Setup
admin = Admin(name="Admin Panel", template_mode="bootstrap3")

class AdminModelView(ModelView):
    """Restricts admin panel access to logged-in users."""
    def is_accessible(self):
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('login'))  # Redirect to login page if not authenticated

# 🔹 Register the admin panel models
def init_admin(app):
    """Registers Flask-Admin with the app."""
    admin.init_app(app)
    admin.add_view(AdminModelView(Prediction, db.session))

@setup_admin_bp.route('/setup-admin', methods=['GET', 'POST'])
def setup_admin():
    """Creates an admin user."""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash("Admin already exists!", "danger")
            return redirect(url_for('setup_admin.setup_admin'))

        # ✅ Fix Variable Name
        new_admin = User(username=username, password=hashed_password)  # ✅ Don't use 'admin' here
        db.session.add(new_admin)
        db.session.commit()

        flash("Admin created successfully!", "success")
        return redirect(url_for('setup_admin.setup_admin'))

    return render_template("admin_setup.html")
