from flask import render_template, redirect, url_for, flash, request
from app import app, db
from app.models import User, Job, Application
from app.forms import LoginForm, SignupForm, JobPostForm
from flask_login import login_user, logout_user, current_user, login_required
from datetime import datetime, timedelta


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.password == form.password.data:
            login_user(user)
            if user.user_type == 'user':
                return redirect(url_for('user_dashboard'))
            elif user.user_type == 'employer':
                return redirect(url_for('employer_dashboard'))
    return render_template('login.html', form=form)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        new_user = User(username=form.username.data, email=form.email.data, password=form.password.data, user_type=form.user_type.data)
        db.session.add(new_user)
        db.session.commit()
        flash('Account created successfully!')
        return redirect(url_for('login'))
    return render_template('signup.html', form=form)

@app.route('/user/dashboard')
@login_required
def user_dashboard():
    jobs = Job.query.filter(Job.posted_at <= datetime.utcnow() - timedelta(hours=24)).all() if not current_user.premium_status else Job.query.all()
    return render_template('user_dashboard.html', jobs=jobs)

@app.route('/employer/dashboard')
@login_required
def employer_dashboard():
    jobs = Job.query.filter_by(employer_id=current_user.id).all()
    return render_template('employer_dashboard.html', jobs=jobs)
