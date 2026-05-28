import os
from flask import Flask, render_template, abort
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__, static_folder=os.path.join(BASE_DIR, "public"), static_url_path="", template_folder=os.path.join(BASE_DIR, "templates"))
app.config["SEND_FILE_MAX_AGE_DEFAULT"] = 31536000
PROJECTS = {"aws-call-transcription": {"slug": "aws-call-transcription", "category": "AWS + NLP", "title": "AWS Call Transcription", "summary": "Docker AWS Lambda pipeline.", "image": "img/output.jpg", "tags": ["AWS", "Lambda", "Docker"], "details": ["Event-driven", "Transcription", "Sentiment"]}, "ml-forecasting": {"slug": "ml-forecasting", "category": "ML", "title": "Time Series Forecasting", "summary": "LSTM networks.", "image": "img/output.jpg", "tags": ["Python", "TensorFlow"], "details": ["LSTM", "80%", "Real-time"]}, "data-pipeline": {"slug": "data-pipeline", "category": "Data", "title": "ETL Pipeline", "summary": "100GB+ daily.", "image": "img/output.jpg", "tags": ["Airflow", "SQL"], "details": ["DAG", "Quality", "Automated"]}}
EXPERIENCE = {"kotak": {"slug": "kotak-ai-internship", "role": "AI Intern", "company": "Kotak", "period": "Nov 2025", "location": "Mumbai", "summary": "AWS call pipeline.", "highlights": ["Transcription", "Lambda", "Compliance"]}}
@app.route("/")
def index():
    return render_template("index.html", profile={"name": "Jeet Shorey", "headline": "Data Science student.", "email": "shoreyjeet@gmail.com", "linkedin": "https://linkedin.com", "phone": "+91 9833232395", "location": "Mumbai"}, projects=list(PROJECTS.values()), experience=list(EXPERIENCE.values()), education=[{"year": "2022-2026", "degree": "B.Tech", "school": "NMIMS"}], skills=["Python", "ML", "AWS", "SQL", "Docker", "Flask", "JS", "TensorFlow", "Airflow"])
@app.route("/project/<slug>")
def project_detail(slug):
    project = PROJECTS.get(slug)
    if not project: abort(404)
    return render_template("project_detail.html", profile={"name": "Jeet Shorey", "email": "shoreyjeet@gmail.com"}, project=project)
@app.route("/experience/<slug>")
def experience_detail(slug):
    exp = EXPERIENCE.get(slug)
    if not exp: abort(404)
    return render_template("experience_detail.html", profile={"name": "Jeet Shorey", "email": "shoreyjeet@gmail.com"}, experience=exp)
@app.errorhandler(404)
def not_found(error):
    return render_template("404.html"), 404
if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5000)
