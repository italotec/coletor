import os
from flask import Flask
from .extensions import db, login_manager
from .models import User
from config import Config

def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(Config)

    os.makedirs(app.instance_path, exist_ok=True)

    db.init_app(app)
    login_manager.init_app(app)

    from .auth.routes import auth_bp
    from .accounts.routes import accounts_bp
    from .admin.routes import admin_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(accounts_bp)
    app.register_blueprint(admin_bp)

    with app.app_context():
        db.create_all()
        _ensure_default_admin()

    return app


def _ensure_default_admin():
    """
    Creates a default admin if there are no users yet.

    IMPORTANT:
    - username is a separate field from id.
    - id is auto-generated integer (usually 1 on a fresh DB).
    - default credentials:
        username: df
        password: df
    """
    if User.query.count() == 0:
        admin = User(username="df", is_admin=True, is_banned=False)
        admin.set_password("df")
        db.session.add(admin)
        db.session.commit()
