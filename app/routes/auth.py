from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required
from app.models.user import User, Role
from app.forms import LoginForm
from app.extensions import db

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    
    # Get all roles and their users for the dropdown
    roles = Role.query.all()
    users_by_role = {}
    for role in roles:
        users = User.query.filter_by(role_id=role.id, is_active=True).all()
        if users:  # Only add roles that have users
            users_by_role[role.name] = [(user.username, f"{user.username} ({role.name})") for user in users]
    
    # Prepare choices for the dropdown
    choices = [('', 'Select Username')]
    for role_name, users in users_by_role.items():
        choices.extend(users)
    
    form.username.choices = choices
    
    if request.method == 'POST' and form.validate():
        user = User.query.filter_by(username=form.username.data).first()
        
        if user and user.check_password(form.password.data):
            login_user(user)
            flash('Logged in successfully.', 'success')
            return redirect(url_for('main.dashboard'))
        else:
            flash('Invalid username or password.', 'error')
    
    return render_template('auth/login.html', form=form)

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out successfully.', 'success')
    return redirect(url_for('auth.login')) 