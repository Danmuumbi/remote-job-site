from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from .forms import LoginForm, SignupForm, PostJobForm
from .models import User, Job, Application
from . import app, db
from datetime import datetime,timedelta

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        # Check if the email is already registered
        existing_user = User.query.filter_by(email=form.email.data).first()
        if existing_user:
            flash('Email is already registered. Please use a different email.', 'danger')
            return redirect(url_for('signup'))

        # Create a new user with form data
        new_user = User(
            username=form.username.data,
            email=form.email.data,
            password=generate_password_hash(form.password.data),
            user_type=form.user_type.data  # 'user' or 'employer'
        )
        db.session.add(new_user)
        db.session.commit()

        flash('Account created successfully! Please log in.', 'success')
        return redirect(url_for('login'))

    return render_template('signup.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            flash('Login successful!', 'success')
            if user.user_type == 'user':
                return redirect(url_for('user_dashboard'))
            elif user.user_type == 'employer':
                return redirect(url_for('employer_dashboard'))
        else:
            flash('Login failed. Check your email and password.', 'danger')
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('index'))


@app.route('/user_dashboard')
@login_required
def user_dashboard():
    if current_user.user_type != 'user':
        flash('Access denied.', 'danger')
        return redirect(url_for('index'))

    # Define cutoff time as 30 minutes ago
    cutoff_time = datetime.utcnow() - timedelta(minutes=50)
    
    # Query jobs posted more than 30 minutes ago
    jobs = Job.query.filter(Job.posted_at <= cutoff_time).all()

    return render_template('user_dashboard.html', jobs=jobs)




@app.route('/employer_dashboard')
@login_required
def employer_dashboard():
    if current_user.user_type != 'employer':
        flash('Access denied.', 'danger')
        return redirect(url_for('index'))

    # Fetch jobs posted by the current employer
    jobs_posted = Job.query.filter_by(employer_id=current_user.id).all()
    
    return render_template('employer_dashboard.html', jobs=jobs_posted)



@app.route('/edit_job/<int:job_id>', methods=['GET', 'POST'])
@login_required
def edit_job(job_id):
    job = Job.query.get_or_404(job_id)

    if job.employer_id != current_user.id:
        flash('You do not have permission to edit this job.', 'danger')
        return redirect(url_for('employer_dashboard'))

    if request.method == 'POST':
        job.title = request.form['title']
        job.job_type = request.form['job_type']
        job.description = request.form['description']

        db.session.commit()
        flash('Job updated successfully.', 'success')
        return redirect(url_for('employer_dashboard'))

    return render_template('edit_job.html', job=job)







@app.route('/view_applicants/<int:job_id>')
@login_required
def view_applicants(job_id):
    # Ensure the user is an employer
    if current_user.user_type != 'employer':
        flash('Access denied.', 'danger')
        return redirect(url_for('index'))

    # Get the job and its applicants
    job = Job.query.get_or_404(job_id)
    
    # Retrieve all applicants for the job, joining with the user table to get applicant details
    applicants = Application.query.filter_by(job_id=job_id).join(User).all()

    return render_template('view_applicants.html', job=job, applicants=applicants)

@app.route('/view_application/<int:application_id>')
@login_required
def view_application_details(application_id):
    # Retrieve the application by ID
    application = Application.query.get_or_404(application_id)

    # Ensure the current user is allowed to view this information
    if current_user.user_type != 'employer':
        flash('Access denied.', 'danger')
        return redirect(url_for('index'))

    return render_template('application_details.html', application=application)





@app.route('/remove_job/<int:job_id>', methods=['POST'])
@login_required
def remove_job(job_id):
    job = Job.query.get(job_id)
    if job and job.employer_id == current_user.id:
        # First, delete all applications related to the job
        Application.query.filter_by(job_id=job.id).delete()
        db.session.delete(job)
        db.session.commit()
        flash('Job and related applications removed successfully.', 'success')
    else:
        flash('Job not found or access denied.', 'danger')
    return redirect(url_for('employer_dashboard'))




@app.route('/post_job', methods=['GET', 'POST'])
@login_required
def post_job():
    if request.method == 'POST':
        # Remove the premium status check
        # Get job details from the form
        job_title = request.form.get('job_title')
        job_description = request.form.get('job_description')
        job_type = request.form.get('job_type')

        # Log the received data
        app.logger.debug(f"Job Title: {job_title}, Job Description: {job_description}, Job Type: {job_type}")

        # Logic to handle job posting
        new_job = Job(title=job_title, description=job_description, job_type=job_type, employer_id=current_user.id)
        db.session.add(new_job)
        db.session.commit()

        flash('Job posted successfully!', 'success')
        return redirect(url_for('employer_dashboard'))

    return render_template('post_job.html')  # Render the job posting form



# @app.route('/premium', methods=['GET', 'POST'])
# @login_required
# def premium():
#     if current_user.user_type != 'user':
#         flash('Access denied.', 'danger')
#         return redirect(url_for('index'))
    
#     if request.method == 'POST':
#         passkey = request.form.get('passkey')
#         correct_passkey = 'PREMIUM123'  # Replace with your correct logic
        
#         if passkey == correct_passkey:
#             flash('Access granted to premium content!', 'success')
#             return redirect(url_for('premium_content'))
#         else:
#             flash('Incorrect passkey, please try again.', 'danger')
#             return render_template('premium.html')  # Reload passkey entry page
    
#     # GET request - Render the premium access page where the user can enter passkey
#     return render_template('premium.html')



from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user

@app.route('/premium', methods=['GET', 'POST'])
@login_required
def premium():
    if current_user.user_type != 'user':
        flash('Access denied.', 'danger')
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        passkey = request.form.get('passkey')
        correct_passkey = 'PREMIUM123'  # Replace with your correct logic
        
        if passkey == correct_passkey:
            flash('Access granted to premium content!', 'success')
            return redirect(url_for('premium_content'))
        else:
            flash('Incorrect passkey. Learn more about the benefits of upgrading to premium.', 'danger')
            return redirect(url_for('premium_info'))  # Redirect to premium info page
    
    # GET request - Render the premium access page where the user can enter passkey
    return render_template('premium.html')

# Route for premium info page
@app.route('/premium_info')
@login_required
def premium_info():
    return render_template('premium_info.html')



@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/submit_contact_form', methods=['POST'])
def submit_contact_form():
    # You can handle form submission here (e.g., send an email, save to a database)
    name = request.form['name']
    email = request.form['email']
    subject = request.form['subject']
    message = request.form['message']
    flash('Your message has been sent successfully!', 'success')
    return redirect('/contact')








@app.route('/upgrade')
def upgrade():
    return render_template('upgrade.html')

@app.route('/process_payment/<plan>')
def process_payment(plan):
    # Logic for payment processing
    # This is just a placeholder. In reality, you would call a payment API like Stripe or PayPal
    if plan == "basic":
        # Handle payment for Basic plan
        return redirect(url_for('payment_confirmation', plan="Basic Plan"))
    elif plan == "standard":
        # Handle payment for Standard plan
        return redirect(url_for('payment_confirmation', plan="Standard Plan"))
    elif plan == "premium":
        # Handle payment for Premium plan
        return redirect(url_for('payment_confirmation', plan="Premium Plan"))
    else:
        return redirect(url_for('upgrade'))

@app.route('/payment_confirmation/<plan>')
def payment_confirmation(plan):
    return f"Payment successful for {plan}! Thank you for upgrading."

if __name__ == '__main__':
    app.run(debug=True)





@app.route('/premium_content')
@login_required
def premium_content():
    if current_user.user_type != 'user' or not current_user.premium_status:
        flash('You must be a premium member to view this page.', 'danger')
        return redirect(url_for('premium'))
    
    # Fetch all jobs (since this is premium content)
    all_jobs = Job.query.all()  # Assuming 'Job' is your jobs model
    
    return render_template('premium_content.html', jobs=all_jobs)



@app.route('/job/<int:job_id>')
@login_required
def job_details(job_id):
    job = Job.query.get(job_id)
    if job:
        return render_template('job_details.html', job=job)
    else:
        flash('Job not found.', 'danger')
        return redirect(url_for('premium_content'))


@app.route('/jobs')
@login_required
def jobs():
    # Filter jobs to only show those posted more than 24 hours ago
    # cutoff_time = datetime.utcnow() - timedelta(hours=24)
    cutoff_time = datetime.utcnow() - timedelta(hours=0.5)
    jobs = Job.query.filter(Job.posted_at <= cutoff_time).all()
    
    return render_template('jobs.html', jobs=jobs)


# Route to apply for a job
@app.route('/apply/<int:job_id>', methods=['GET'])
@login_required
def apply_job(job_id):
    job = Job.query.get_or_404(job_id)
    return render_template('apply_job.html', job=job)


from flask import request, redirect, url_for, flash

@app.route('/submit_application/<int:job_id>', methods=['POST'])
@login_required
def submit_application(job_id):
    # Retrieve the job by its ID
    job = Job.query.get_or_404(job_id)

    # Get form data
    email = request.form.get('email')
    cv_text = request.form.get('cv_text')

    # Validate that the email and CV text are provided
    if not email or not cv_text:
        flash('Email and CV content are required.', 'danger')
        return redirect(url_for('apply_job', job_id=job_id))

    # Check if the user has already applied for this job
    existing_application = Application.query.filter_by(job_id=job_id, applicant_id=current_user.id).first()
    if existing_application:
        flash('You have already applied for this job.', 'warning')
        return redirect(url_for('user_dashboard'))  # Redirect to the dashboard if already applied

    # Create a new Application object
    application = Application(
        job_id=job_id,
        applicant_id=current_user.id,
        cv_text=cv_text
    )

    # Add the new application to the database
    try:
        db.session.add(application)
        db.session.commit()
        flash('Your application has been submitted successfully.', 'success')
    except Exception as e:
        db.session.rollback()
        flash('An error occurred while submitting your application.', 'danger')
        return redirect(url_for('apply_job', job_id=job_id))  # Stay on the form if there's an error

    # Redirect to the dashboard after successful submission
    return redirect(url_for('user_dashboard'))




#admin
# from flask import render_template, redirect, url_for, flash
# from flask_login import login_required, current_user

# @app.route('/admin')
# # @login_required
# def admin_panel():
#     # Ensure the current user is an administrator
#     if current_user.user_type != 'admin':
#         flash('Access denied. Admins only.', 'danger')
#         return redirect(url_for('index'))

#     # Get all users, jobs, and applications
#     users = User.query.all()
#     jobs = Job.query.all()
#     applications = Application.query.all()

#     return render_template('admin.html', users=users, jobs=jobs, applications=applications)

# # Route to delete a user
# @app.route('/delete_user/<int:user_id>')
# @login_required
# def delete_user(user_id):
#     # Ensure the current user is an administrator
#     if current_user.user_type != 'admin':
#         flash('Access denied. Admins only.', 'danger')
#         return redirect(url_for('index'))

#     user = User.query.get_or_404(user_id)
#     db.session.delete(user)
#     db.session.commit()
#     flash('User deleted successfully.', 'success')
#     return redirect(url_for('admin_panel'))

# # Route to delete a job
# @app.route('/delete_job/<int:job_id>')
# @login_required
# def delete_job(job_id):
#     # Ensure the current user is an administrator
#     if current_user.user_type != 'admin':
#         flash('Access denied. Admins only.', 'danger')
#         return redirect(url_for('index'))

#     job = Job.query.get_or_404(job_id)
#     db.session.delete(job)
#     db.session.commit()
#     flash('Job deleted successfully.', 'success')
#     return redirect(url_for('admin_panel'))

# # Route to delete an application
# @app.route('/delete_application/<int:application_id>')
# @login_required
# def delete_application(application_id):
#     # Ensure the current user is an administrator
#     if current_user.user_type != 'admin':
#         flash('Access denied. Admins only.', 'danger')
#         return redirect(url_for('index'))

#     application = Application.query.get_or_404(application_id)
#     db.session.delete(application)
#     db.session.commit()
#     flash('Application deleted successfully.', 'success')
#     return redirect(url_for('admin_panel'))



from flask import render_template, redirect, url_for, flash
from flask_login import current_user

@app.route('/admin')
# @login_required  # Commented out for easy access
def admin_panel():
    # You can remove the admin check temporarily for easy access
    # if current_user.user_type != 'admin':
    #     flash('Access denied. Admins only.', 'danger')
    #     return redirect(url_for('index'))

    # Get all users, jobs, and applications
    users = User.query.all()
    jobs = Job.query.all()
    applications = Application.query.all()

    return render_template('admin.html', users=users, jobs=jobs, applications=applications)

# Route to delete a user
@app.route('/delete_user/<int:user_id>')
# @login_required  # Commented out for easy access
def delete_user(user_id):
    # You can remove the admin check temporarily for easy access
    # if current_user.user_type != 'admin':
    #     flash('Access denied. Admins only.', 'danger')
    #     return redirect(url_for('index'))

    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    flash('User deleted successfully.', 'success')
    return redirect(url_for('admin_panel'))

# Route to delete a job
@app.route('/delete_job/<int:job_id>')
# @login_required  # Commented out for easy access
def delete_job(job_id):
    # You can remove the admin check temporarily for easy access
    # if current_user.user_type != 'admin':
    #     flash('Access denied. Admins only.', 'danger')
    #     return redirect(url_for('index'))

    job = Job.query.get_or_404(job_id)
    db.session.delete(job)
    db.session.commit()
    flash('Job deleted successfully.', 'success')
    return redirect(url_for('admin_panel'))

# Route to delete an application
@app.route('/delete_application/<int:application_id>')
# @login_required  # Commented out for easy access
def delete_application(application_id):
    # You can remove the admin check temporarily for easy access
    # if current_user.user_type != 'admin':
    #     flash('Access denied. Admins only.', 'danger')
    #     return redirect(url_for('index'))

    application = Application.query.get_or_404(application_id)
    db.session.delete(application)
    db.session.commit()
    flash('Application deleted successfully.', 'success')
    return redirect(url_for('admin_panel'))



from flask import request, flash

@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')

        # Ensure valid input
        if not username or not email:
            flash('Username and Email are required.', 'danger')
            return redirect(url_for('edit_profile'))

        # Update the current user's profile
        current_user.username = username
        current_user.email = email
        db.session.commit()

        flash('Profile updated successfully.', 'success')
        return redirect(url_for('user_dashboard'))

    return render_template('edit_profile.html', user=current_user)
