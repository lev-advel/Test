from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_utils import database_exists, create_database

# Database connection URL (change only here for all DB connections)
DB_URL = 'postgresql://postgres:alina@localhost/forecast'

# Initialize SQLAlchemy instance
db = SQLAlchemy()


# Initialize the database connection and creating new database
def init_db(app):

    # Check if database exists, create if it doesn't
    if not database_exists(DB_URL):
        create_database(DB_URL)
        print("Database created successfully!")

    # Connection string
    app.config['SQLALCHEMY_DATABASE_URI'] = DB_URL
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Bind SQLAlchemy instance to Flask application
    db.init_app(app)


app = Flask(__name__)

# Initializing database
init_db(app)