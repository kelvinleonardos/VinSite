from flask import Flask
from .config import engine, Base
from .auth import auth_bp, token_bp
from .user import user_bp
from flask_cors import CORS


def create_app():
    app = Flask(__name__)
    app.secret_key = 'supersecretkey'
    CORS(app)

    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(token_bp, url_prefix='/token')
    app.register_blueprint(user_bp, url_prefix='/user')

    Base.metadata.create_all(engine)

    return app
