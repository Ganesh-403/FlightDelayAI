# backend/app/__init__.py
from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bcrypt import Bcrypt

from .core.config import settings
from .models.base import db
from .models.user import User

bcrypt = Bcrypt()
migrate = Migrate()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object(settings)
    app.config['SQLALCHEMY_DATABASE_URI'] = settings.SQLALCHEMY_DATABASE_URI
    app.config['SECRET_KEY'] = settings.SECRET_KEY

    # Initialize Extensions
    db.init_app(app)
    bcrypt.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    CORS(app)  # Enable CORS for React/Vite frontend

    login_manager.login_view = "auth.login"

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Register Blueprints
    from .api.v1.auth import auth_bp
    from .api.v1.predict import predict_bp
    
    app.register_blueprint(auth_bp, url_prefix=f"{settings.API_V1_STR}/auth")
    app.register_blueprint(predict_bp, url_prefix=f"{settings.API_V1_STR}/predict")

    @app.route("/health")
    def health_check():
        return {"status": "healthy", "service": "flight-delay-api"}, 200

    return app
