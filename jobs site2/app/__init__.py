

# from flask import Flask
# from flask_sqlalchemy import SQLAlchemy
# from flask_migrate import Migrate
# from flask_login import LoginManager



# app = Flask(__name__)
# app.config.from_object('config.Config')  # Load configuration from config.py

# # Initialize database and migration
# db = SQLAlchemy(app)
# migrate = Migrate(app, db)

# from app import routes, models  # Import routes and models to avoid circular import issues



from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

app = Flask(__name__)
app.config.from_object('config.Config')  # Load configuration from config.py

# Initialize database and migration
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Initialize LoginManager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'  # This specifies the login route to redirect unauthorized users

# Import routes and models to avoid circular import issues
from app import routes, models

# Define the user loader callback
@login_manager.user_loader
def load_user(user_id):
    return models.User.query.get(int(user_id))  # Make sure this refers to the User model
