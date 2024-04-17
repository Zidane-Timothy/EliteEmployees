from flask import Blueprint, render_template, jsonify, request, flash, redirect, url_for
from flask_jwt_extended import jwt_required, current_user, unset_jwt_cookies, set_access_cookies
from sqlalchemy.exc import IntegrityError

from App.models.user import db, User

from App.controllers import (
    login
    
)

auth_views = Blueprint('auth_views', __name__, template_folder='../templates')


'''
Page/Action Routes
'''    
@auth_views.route('/users', methods=['GET']) #works
def get_user_page():
    if 'username' not in session:
        return redirect(url_for('auth_views.login_view'))
    users = get_all_users()
    return render_template('users.html', users=users)
    
@auth_views.route('/identify', methods=['GET'])
@jwt_required()
def identify_page():
    return render_template('message.html', title="Identify", message=f"You are logged in as {current_user.id} - {current_user.username}")

@auth_views.route('/login', methods=['GET', 'POST']) #works
def login_view():
    if request.method == 'POST':
        data = request.form
        token = login(data['username'], data['password'])
        if token:
            flash('Login Successful')
            response = redirect(url_for('index_views.index_page'))
            set_access_cookies(response, token)
            return response
        else:
            flash('Bad username or password given', 'error')
    return render_template('login.html')

@auth_views.route('/logout', methods=['GET']) #works
def logout_action():
    response = redirect(request.referrer) 
    flash("Logged Out!")
    unset_jwt_cookies(response)
    return response

@auth_views.route('/signup', methods=['GET', 'POST'])
def signup_user_view():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        try:
            new_user = User(username=username, password=password)
            db.session.add(new_user)
            db.session.commit()
            flash(f"User {username} created!")
            # Log in the user and set access cookies
            token = login(username, password)
            response = redirect(url_for('index_views.index_page'))
            set_access_cookies(response, token)
            return response
        except IntegrityError:
            db.session.rollback()
            flash('Username already exists', 'error')
            return redirect(url_for('auth_views.signup_user_view'))
    return render_template('signup.html')


'''
API Routes
'''

@auth_views.route('/api/login', methods=['POST'])
def user_login_api():
  data = request.json
  token = login(data['username'], data['password'])
  if not token:
    return jsonify(message='bad username or password given'), 401
  response = jsonify(access_token=token) 
  set_access_cookies(response, token)
  return response

@auth_views.route('/api/identify', methods=['GET'])
@jwt_required()
def identify_user():
    return jsonify({'message': f"username: {current_user.username}, id : {current_user.id}"})

@auth_views.route('/api/logout', methods=['GET'])
def logout_api():
    response = jsonify(message="Logged Out!")
    unset_jwt_cookies(response)
    return response