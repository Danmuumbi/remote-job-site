# Remote Job Search Platform

The **Remote Job Search Platform** is designed to bridge the gap between job seekers looking for remote opportunities and employers seeking remote talent. The platform enables users to register, create profiles, browse remote job listings, and apply for jobs directly, while employers can post job opportunities, manage applications, and interact with potential candidates.

## Table of Contents

1. [Features](#features)
2. [Tech Stack](#tech-stack)
3. [Project Structure](#project-structure)
4. [Installation](#installation)
5. [Usage](#usage)
6. [Key Pages](#key-pages)
7. [Premium Features](#premium-features)
8. [Challenges and Solutions](#challenges-and-solutions)
9. [Future Enhancements](#future-enhancements)
10. [Contributing](#contributing)
11. [License](#license)
12. [Status](#status)

## Features

### For Job Seekers:
- **Profile Creation**: Users can create and update profiles with their skills, resumes, and job preferences.
- **Job Search**: Browse a curated list of remote job opportunities based on various filters such as location, company, and skillset.
- **Application Management**: Users can apply for jobs directly from their dashboard and track the status of their applications.
- **Notifications**: Receive email or in-app notifications for job application status changes or new job listings.

### For Employers:
- **Profile Creation**: Employers can create a company profile with information about their organization and job opportunities.
- **Job Posting**: Post job opportunities with detailed descriptions, requirements, and salary ranges.
- **Applicant Management**: View the list of applicants, manage their status (shortlisted, rejected, etc.), and communicate directly with candidates.
- **Premium Job Listings**: Employers can upgrade to premium to boost their job postings, making them more visible to job seekers.

### Premium Features:
- **Exclusive Job Listings**: Access to exclusive job opportunities available only to premium members.
- **Enhanced Search**: Use advanced filters like salary range, company size, and work hours.
- **Analytics**: Get insights into how many people viewed and applied to your job listing (for employers).

## Tech Stack

The project uses the following technologies:

- **Backend**: Flask (Python Framework)
- **Database**: SQLAlchemy with MySQL (or SQLite for development)
- **Frontend**: HTML5, CSS3, Bootstrap for responsive and modern UI
- **Authentication**: Flask-Login for user authentication
- **Forms**: WTForms for user registration, login, and job post forms
- **Deployment**: The project can be deployed on platforms such as **Heroku** or **AWS**
- **Version Control**: Git

## Project Structure




The project is organized into the following directories:

remote_job_search/
│
├── app/
│   ├── __init__.py                # Initializes the Flask app and configurations
│   ├── models.py                  # SQLAlchemy models for users, employers, jobs, and applications
│   ├── forms.py                   # WTForms for sign-up, login, job post, etc.
│   ├── routes.py                  # All the routes (user, employer, dashboard, jobs)
│   ├── templates/
│   │   ├── layout.html            # Base layout for pages
│   │   ├── index.html             # Landing page
│   │   ├── user_dashboard.html    # User dashboard page
│   │   ├── employer_dashboard.html # Employer dashboard page
│   │   ├── login.html             # Login page
│   │   ├── signup.html            # Sign-up page for both users and employers
│   │   ├── post_job.html          # Job posting form for employers
│   │   ├── jobs.html              # List of jobs available
│   │   ├── applicant_list.html    # Employer's view of applicants
│   ├── static/
│   │   ├── css/
│   │   │   └── styles.css         # Bootstrap CSS customization (optional)
│   │   └── js/
│       └── images/
├── migrations/                    # Alembic for DB migrations
├── config.py                      # Application configurations
├── run.py                         # Runs the Flask application
└── requirements.txt               # Python package dependencies




## Installation

### Prerequisites

- Python 3.7 or higher
- Flask
- MySQL or SQLite
- Git

### Setup Instructions

1. **Clone the repository:**

   ```bash
   git clone https://github.com/yourusername/remote-job-search.git
   cd remote-job-search



Create and activate a virtual environment:
python3 -m venv venv
source venv/bin/activate  # On Windows use venv\Scripts\activate



Install the required packages:
pip install -r requirements.txt

Set up the database:

For MySQL:

Set up your MySQL database and update config.py with your database URI.
Run the following commands to apply migrations:

flask db init
flask db migrate
flask db upgrade

Run the Flask app:
flask run/python3 run.py

The application will now be running on http://127.0.0.1:5000.


