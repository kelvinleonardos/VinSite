from flask import Flask, Blueprint, request, jsonify, session as flask_session
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime
from functools import wraps
from .config import Session
from .models import User

auth_bp = Blueprint('auth', __name__)
token_bp = Blueprint('token', __name__)

SECRET_KEY = "supersecret"

token_time_delta = datetime.timedelta(minutes=5)


def token_required(optional=False):
    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            token = None
            if 'x-access-token' in request.headers:
                token = request.headers['x-access-token']
            if not token and not optional:
                return jsonify({'message': 'Token is missing!'}), 401
            try:
                data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
                session = Session()
                current_user = session.query(User).filter_by(id=data['user_id']).first()
                session.close()
            except jwt.ExpiredSignatureError:
                return jsonify({'message': 'Token is expired!'}), 401
            except jwt.InvalidTokenError:
                if not optional:
                    return jsonify({'message': 'Invalid token!'}), 401
                current_user = None
            return f(current_user, *args, **kwargs)

        return decorated

    return decorator


@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    hashed_password = generate_password_hash(data['password'], method='pbkdf2:sha256')
    session = Session()
    new_user = User(
        name=data['name'],
        email=data['email'],
        password=hashed_password,
        bio=data.get('bio', ''),
        about_me=data.get('about_me', ''),
        role_ref_id=data['role_ref_id']
    )
    try:
        session.add(new_user)
        session.commit()
        session.close()
        return jsonify({'message': 'New user created!'})
    except Exception as e:
        session.rollback()
        return jsonify({'message': f'Error: {str(e)}'}), 500
    finally:
        session.close()


@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    session = Session()
    user = session.query(User).filter_by(email=data['email']).first()
    if not user or not check_password_hash(user.password, data['password']):
        session.close()
        return jsonify({'message': 'Login failed!'}), 401
    token = jwt.encode({'user_id': user.id, 'exp': datetime.datetime.utcnow() + token_time_delta},
                       SECRET_KEY, algorithm="HS256")
    session.close()
    try:
        return jsonify({'token': token})
    except:
        return jsonify({'token': token.decode('utf-8')})


@auth_bp.route('/logout', methods=['POST'])
@token_required()
def logout(current_user):
    flask_session.pop('user_id', None)
    return jsonify({'message': 'Successfully logged out.'}), 200


@token_bp.route('/refresh', methods=['POST'])
def refresh_token():
    token = None
    if 'x-access-token' in request.headers:
        token = request.headers['x-access-token']
    if not token:
        return jsonify({'message': 'Token is missing!'}), 401
    try:
        data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"], options={"verify_exp": False})
        new_token = jwt.encode(
            {'user_id': data['user_id'], 'exp': datetime.datetime.utcnow() + token_time_delta},
            SECRET_KEY, algorithm="HS256")
        return jsonify({'token': new_token})
    except jwt.InvalidTokenError:
        return jsonify({'message': 'Invalid token!'}), 401
