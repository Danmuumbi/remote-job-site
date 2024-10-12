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
