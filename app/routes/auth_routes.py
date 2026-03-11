from flask import Blueprint, request, jsonify, render_template, redirect, url_for, make_response, flash
from flask_jwt_extended import create_access_token, set_access_cookies, unset_jwt_cookies
from ..models import User
from ..extensions import db
import datetime

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('auth/register.html')
    
    data = request.form if request.form else request.get_json()
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')
    role = data.get('role', 'student')

    if User.query.filter_by(email=email).first():
        flash('Email already registered', 'danger')
        return render_template('auth/register.html')

    new_user = User(name=name, email=email, role=role)
    new_user.set_password(password)
    db.session.add(new_user)
    db.session.commit()

    flash('Registration successful! Please login.', 'success')
    return redirect(url_for('auth.login'))

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('auth/login.html')
    
    data = request.form if request.form else request.get_json()
    email = data.get('email')
    password = data.get('password')

    user = User.query.filter_by(email=email).first()
    if user and user.check_password(password):
        access_token = create_access_token(identity=str(user.id), additional_claims={"role": user.role})
        resp = make_response(redirect(url_for('user.dashboard')))
        set_access_cookies(resp, access_token)
        flash(f'Welcome back, {user.name}!', 'success')
        return resp
    
    flash('Invalid email or password', 'danger')
    return render_template('auth/login.html')

@auth_bp.route('/logout')
def logout():
    resp = make_response(redirect(url_for('auth.login')))
    unset_jwt_cookies(resp)
    flash('Successfully logged out', 'info')
    return resp
