from flask import session, redirect, url_for, flash

# Temporary in-memory user store
# Format: {'email@example.com': {'name': 'Shahid', 'password': '1234'}}
users_db = {}

def register_user(name, email, password):
    if email in users_db:
        return False, "User already exists"
    users_db[email] = {'name': name, 'password': password}
    return True, "Registration successful"

def login_user(email, password):
    user = users_db.get(email)
    if not user:
        return False, "User not found"
    if user['password'] != password:
        return False, "Incorrect password"
    session['user'] = {'name': user['name'], 'email': email}
    return True, "Login successful"

def logout_user():
    session.pop('user', None)
    return redirect(url_for('login'))

def is_logged_in():
    return 'user' in session

def get_current_user():
    return session.get('user')
