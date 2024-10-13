from app import db, User  # Adjust the import according to your app structure
from werkzeug.security import generate_password_hash

# Create the admin user
admin_user = User(username='admin', email='admin@example.com', password=generate_password_hash('your_password'), user_type='admin')
db.session.add(admin_user)
db.session.commit()

print("Admin user created!")
