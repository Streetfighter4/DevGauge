# Initialize Flask extensions
from flask_sqlalchemy import SQLAlchemy
from flask_user import UserManager, SQLAlchemyAdapter

from dynamic.home import app
from dynamic.models.user import User

db = SQLAlchemy(app)  # Initialize Flask-SQLAlchemy
# Create all database tables
db.create_all()

# Setup Flask-User
db_adapter = SQLAlchemyAdapter(db, User)  # Register the User model
user_manager = UserManager(db_adapter, app)  # Initialize Flask-User
