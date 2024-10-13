
# from app import app  # Import the app from the app package
# from flask_login import LoginManager

# login_manager = LoginManager()
# login_manager.init_app(app)

# # Specify the login view
# login_manager.login_view = 'login'  # 'login' should match your login route name


# if __name__ == '__main__':
#     app.run(debug=True)  # Run the application in debug mode


from app import app

if __name__ == '__main__':
    app.run(debug=True)
