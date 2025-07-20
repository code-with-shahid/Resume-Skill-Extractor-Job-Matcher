from flask import Flask, render_template, request
from resume_parser import extract_text_from_pdf
from skill_matcher import extract_skills, match_jobs
import json
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Load job data from JSON
with open('jobs_data.json', 'r') as f:
    job_data = json.load(f)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_resume():
    if 'resume' not in request.files:
        return "No file part"
    file = request.files['resume']
    if file.filename == '':
        return "No selected file"
    
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(filepath)

    # Extract text from PDF
    resume_text = extract_text_from_pdf(filepath)

    # Extract skills
    extracted_skills = extract_skills(resume_text)

    # Match with jobs
    matched_jobs = match_jobs(extracted_skills, job_data)

    return render_template('index.html', skills=extracted_skills, jobs=matched_jobs)

if __name__ == '__main__':
    app.run(debug=True)
