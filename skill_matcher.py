import spacy
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Load English NLP model from spaCy
nlp = spacy.load("en_core_web_sm")

# Simple sample list of known skills (you can expand this)
known_skills = [
    "python", "java", "machine learning", "deep learning", "nlp",
    "sql", "html", "css", "javascript", "react", "node.js",
    "data analysis", "pandas", "numpy", "flask", "django", "git", "linux"
]

def extract_skills(resume_text):
    doc = nlp(resume_text.lower())
    extracted = set()

    for token in doc:
        if token.text in known_skills:
            extracted.add(token.text)

    return list(extracted)

def match_jobs(resume_skills, job_data):
    job_scores = []

    for job in job_data:
        job_text = job['description'].lower()
        resume_text = ' '.join(resume_skills).lower()

        vectorizer = TfidfVectorizer()
        vectors = vectorizer.fit_transform([resume_text, job_text])
        similarity = cosine_similarity(vectors[0], vectors[1])[0][0]

        job_scores.append({
            'title': job['title'],
            'company': job['company'],
            'match_score': round(similarity * 100, 2),
            'description': job['description']
        })

    # Sort by best match first
    job_scores.sort(key=lambda x: x['match_score'], reverse=True)

    return job_scores
