from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Fake data for jobs and applicants for demonstration
jobs = [
    {"id": 1, "title": "Frontend Developer", "type": "Full-time", "description": "Work on creating and maintaining web frontends."},
    {"id": 2, "title": "Backend Developer", "type": "Contract", "description": "Develop server-side applications and maintain databases."},
    {"id": 3, "title": "Data Analyst", "type": "Part-time", "description": "Analyze data trends and create reports."}
]

applicants = [
    {"name": "John Doe", "skills": "Python, Flask, JavaScript", "email": "johndoe@example.com"},
    {"name": "Jane Smith", "skills": "React, Node.js, MongoDB", "email": "janesmith@example.com"}
]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Handle login logic here
        return redirect(url_for('user_dashboard'))
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        # Handle sign-up logic here
        return redirect(url_for('user_dashboard'))
    return render_template('signup.html')

@app.route('/user_dashboard')
def user_dashboard():
    return render_template('user_dashboard.html', jobs=jobs)

@app.route('/employer_dashboard')
def employer_dashboard():
    return render_template('employer_dashboard.html', jobs=jobs)

@app.route('/jobs')
def list_jobs():
    return render_template('jobs.html', jobs=jobs)

@app.route('/post_job', methods=['GET', 'POST'])
def post_job():
    if request.method == 'POST':
        # Handle job posting logic here
        title = request.form.get('job_title')
        job_type = request.form.get('job_type')
        description = request.form.get('job_description')
        jobs.append({"title": title, "type": job_type, "description": description})
        return redirect(url_for('employer_dashboard'))
    return render_template('post_job.html')

@app.route('/applicant_list')
def applicant_list():
    return render_template('applicant_list.html', applicants=applicants)

@app.route('/logout')
def logout():
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
