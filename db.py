from flask import Flask
from connection import db, init_db

app = Flask(__name__)

# Initialize database connection
init_db(app)


# Defining the tables
class WeatherDetails(db.Model):
    __tablename__ = 'weather_details'

    id = db.Column(db.Integer, primary_key=True)
    temperature = db.Column(db.Numeric(5, 2))
    feels_like = db.Column(db.Numeric(5, 2))
    temp_min = db.Column(db.Numeric(5, 2))
    temp_max = db.Column(db.Numeric(5, 2))
    pressure = db.Column(db.Integer)
    humidity = db.Column(db.Integer)
    wind_speed = db.Column(db.Numeric(5, 2))
    wind_dir = db.Column(db.String(50))
    clouds = db.Column(db.Integer)
    visibility = db.Column(db.Integer)
    sunrise = db.Column(db.DateTime)
    sunset = db.Column(db.DateTime)
    description = db.Column(db.String(50))


class CitiesDates(db.Model):
    __tablename__ = 'cities_dates'

    id = db.Column(db.Integer, primary_key=True)
    city_name = db.Column(db.String(30), nullable=False)
    datetime = db.Column(db.DateTime, nullable=False)
    weather_id = db.Column(db.Integer, db.ForeignKey('weather_details.id'))

    weather = db.relationship('WeatherDetails', backref='city_dates')


# Creating tables in database
def create_tables():
    with app.app_context():
        db.create_all()
        print("Tables created successfully!")


if __name__ == '__main__':
    create_tables()