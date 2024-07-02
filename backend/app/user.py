from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from .config import Session
from .models import User
from .auth import token_required

user_bp = Blueprint('user', __name__)


@user_bp.route('/user', methods=['GET'])
@token_required()
def get_user(current_user):
    session = Session()
    user = session.query(User).filter_by(id=current_user.id).first()
    session.close()
    if not user:
        return jsonify({'message': 'User not found!'}), 404
    user_data = {
        'id': user.id,
        'name': user.name,
        'email': user.email,
        'bio': user.bio,
        'about_me': user.about_me,
        'role_ref_id': user.role_ref_id
    }
    return jsonify({'user': user_data})


@user_bp.route('/user', methods=['PUT'])
@token_required()
def update_user(current_user):
    data = request.get_json()
    session = Session()
    user = session.query(User).filter_by(id=current_user.id).first()
    if not user:
        session.close()
        return jsonify({'message': 'User not found!'}), 404
    user.name = data.get('name', user.name)
    user.email = data.get('email', user.email)
    user.bio = data.get('bio', user.bio)
    user.about_me = data.get('about_me', user.about_me)
    user.role_ref_id = data.get('role_ref_id', user.role_ref_id)
    if 'password' in data:
        user.password = generate_password_hash(data['password'], method='pbkdf2:sha256')
    session.commit()
    session.close()
    return jsonify({'message': 'User updated!'})


@user_bp.route('/user', methods=['DELETE'])
@token_required()
def delete_user(current_user):
    session = Session()
    user = session.query(User).filter_by(id=current_user.id).first()
    if not user:
        session.close()
        return jsonify({'message': 'User not found!'}), 404
    session.delete(user)
    session.commit()
    session.close()
    return jsonify({'message': 'User deleted!'})


@user_bp.route('/user/<int:id>', methods=['GET'])
@token_required(optional=True)
def get_user_by_id(current_user, id):
    session = Session()
    user = session.query(User).filter_by(id=id).first()
    session.close()
    if not user:
        return jsonify({'message': 'User not found!'}), 404
    user_data = {
        'id': user.id,
        'name': user.name,
        'email': user.email,
        'bio': user.bio,
        'about_me': user.about_me,
        'role_ref_id': user.role_ref_id
    }
    return jsonify({'user': user_data})


@user_bp.route('/users', methods=['GET'])
@token_required()
def get_all_users(current_user):
    session = Session()
    users = session.query(User).all()
    session.close()
    all_users = []
    for user in users:
        user_data = {
            'id': user.id,
            'name': user.name,
            'email': user.email,
            'bio': user.bio,
            'about_me': user.about_me,
            'role_ref_id': user.role_ref_id
        }
        all_users.append(user_data)
    return jsonify(all_users)
