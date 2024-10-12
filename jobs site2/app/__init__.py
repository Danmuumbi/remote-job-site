from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yoursecretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://username:password@localhost/remote_job_search'
db = SQLAlchemy(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login'

from app import routes
