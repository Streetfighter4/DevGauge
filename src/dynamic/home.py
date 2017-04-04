from flask import Flask
from flask import render_template_string
from flask_sqlalchemy import SQLAlchemy
from flask_user import UserManager, UserMixin, SQLAlchemyAdapter

from dynamic.config.config_class import ConfigClass
from dynamic.controlers import settings
from dynamic.web_hooks import jira_webhook, git_webhook, sentry_webhook


def create_app():
    config = ConfigClass
    app = Flask(__name__)
    app.config.from_object(config)
    app.config['TEMPLATES_AUTO_RELOAD']=True
    app.register_blueprint(jira_webhook.hook)
    app.register_blueprint(git_webhook.hook)
    app.register_blueprint(sentry_webhook.hook)
    app.register_blueprint(settings.settings_blue_print)

    # Initialize Flask extensions
    db = SQLAlchemy(app)  # Initialize Flask-SQLAlchemy

    # Define the User data model. Make sure to add flask_user UserMixin !!!
    class User(db.Model, UserMixin):
        id = db.Column(db.Integer, primary_key=True)

        # User authentication information
        username = db.Column(db.String(50), nullable=False, unique=True)
        password = db.Column(db.String(255), nullable=False, server_default='')

        # User email information
        email = db.Column(db.String(255), nullable=False, unique=True)
        confirmed_at = db.Column(db.DateTime())

        # User information
        active = db.Column('is_active', db.Boolean(), nullable=False, server_default='0')
        first_name = db.Column(db.String(100), nullable=False, server_default='')
        last_name = db.Column(db.String(100), nullable=False, server_default='')

    # Create all database tables
    db.create_all()

    # Setup Flask-User
    db_adapter = SQLAlchemyAdapter(db, User)  # Register the User model
    user_manager = UserManager(db_adapter, app)  # Initialize Flask-User

    # The Home page is accessible to anyone
    @app.route('/')
    def home_page():
        return render_template_string("""
               {% extends "base.html" %}
               {% block content %}
                   <h2>Home page</h2>
                   <p>This page can be accessed by anyone.</p><br/>
                   <p><a href={{ url_for('home_page') }}>Home page</a> (anyone)</p>
                   <p><a href={{ url_for('settings.setup_project') }}>Set up project</a> (login required)</p>
               {% endblock %}
               """)


    return app


if __name__ == "__main__":
    app = create_app()
    app.run(host='192.168.1.100', debug=True)