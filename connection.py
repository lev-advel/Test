from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_utils import database_exists, create_database
import os

# Initialize SQLAlchemy instance
db = SQLAlchemy()


def init_db(app):
    # Get database URL from environment or use default
    db_url = os.getenv('DATABASE_URL', 'postgresql://postgres:postgres@localhost/forecast')

    # Check if database exists, create if it doesn't
    if not database_exists(db_url):
        create_database(db_url)
        print("Database created successfully!")

    # Connection string
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Bind SQLAlchemy instance to Flask application
    db.init_app(app)