from flask import Flask, render_template, request, redirect, url_for, session
from resume_parser import extract_text_from_pdf
from skill_matcher import extract_skills, match_jobs
from auth import register_user, login_user, logout_user, is_logged_in, get_current_user
import json
import os

app = Flask(__name__)
import os
app.secret_key = os.environ.get("SECRET_KEY", "fallback-dev-secret")
app.config['UPLOAD_FOLDER'] = 'uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Load job data
with open('jobs_data.json', 'r') as f:
    job_data = json.load(f)

# --- AUTH ROUTES ---

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        success, msg = register_user(name, email, password)
        if success:
            return redirect(url_for('login'))
        return render_template('register.html', error=msg)
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        success, msg = login_user(email, password)
        if success:
            return redirect(url_for('dashboard'))
        return render_template('login.html', error=msg)
    return render_template('login.html')

@app.route('/logout')
def logout():
    return logout_user()

# --- DASHBOARD / RESUME MATCHER ---

@app.route('/')
def home():
    return redirect(url_for('dashboard'))

@app.route('/dashboard')
def dashboard():
    if not is_logged_in():
        return redirect(url_for('login'))
    return render_template('index.html', user=get_current_user())

@app.route('/upload', methods=['POST'])
def upload_resume():
    if not is_logged_in():
        return redirect(url_for('login'))

    if 'resume' not in request.files:
        return "No file part"
    file = request.files['resume']
    if file.filename == '':
        return "No selected file"

    filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(filepath)

    resume_text = extract_text_from_pdf(filepath)
    extracted_skills = extract_skills(resume_text)
    matched_jobs = match_jobs(extracted_skills, job_data)

    return render_template('index.html',
                           skills=extracted_skills,
                           jobs=matched_jobs,
                           user=get_current_user())

if __name__ == '__main__':
    import os
    # Use Render's recommended host and port
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

