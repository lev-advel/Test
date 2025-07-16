from flask import Flask, render_template, request, redirect, url_for, jsonify
import requests
from datetime import datetime
from connection import db, init_db
from db import db, WeatherDetails, CitiesDates
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
init_db(app)

API_KEY = os.getenv('API_KEY', 'd9db6586cfd1077e913484e6117d8b3d')


@app.route('/', methods=['GET', 'POST'])
def weather():
    if request.method == 'POST':
        city = request.form.get('city')
        return redirect(url_for('get_weather', city=city))

    return render_template('index.html')


@app.route('/weather/<city>')
def get_weather(city):
    try:
        parts = [part.strip() for part in city.split(',')]
        city_name = parts[0]
        country_code = parts[1] if len(parts) > 1 else None

        if country_code:
            url = f"http://api.openweathermap.org/data/2.5/weather?q={city_name},{country_code}&appid={API_KEY}&units=metric"
        else:
            url = f"http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={API_KEY}&units=metric"

        response = requests.get(url).json()

        # Check for API error
        if response.get('cod') != 200:
            return render_template('index.html',
                               city=city,
                               error=response.get('message', 'Unknown error'))

        # Convert timestamps
        sunrise = datetime.fromtimestamp(response['sys']['sunrise'])
        sunset = datetime.fromtimestamp(response['sys']['sunset'])

        # Wind direction
        wind_deg = response['wind']['deg']
        directions = ['North', 'Northeast', 'East', 'Southeast',
                     'South', 'Southwest', 'West', 'Northwest']
        wind_dir = directions[round(wind_deg / 45) % 8]

        # Save data to database
        with app.app_context():
            weather_data = WeatherDetails(
                temperature=response['main']['temp'],
                feels_like=response['main']['feels_like'],
                temp_min=response['main']['temp_min'],
                temp_max=response['main']['temp_max'],
                pressure=response['main']['pressure'],
                humidity=response['main']['humidity'],
                wind_speed=response['wind']['speed'],
                wind_dir=wind_dir,
                clouds=response['clouds']['all'],
                visibility=response.get('visibility'),
                sunrise=sunrise,
                sunset=sunset,
                description=response['weather'][0]['description']
            )

            db.session.add(weather_data)
            db.session.flush()

            city_date = CitiesDates(
                city_name=f"{response['name']}, {response['sys']['country']}",
                datetime=datetime.now(),
                weather_id=weather_data.id
            )

            db.session.add(city_date)
            db.session.commit()

        # Prepare data for template
        weather_info = {
            'temperature': response['main']['temp'],
            'feels_like': response['main']['feels_like'],
            'temp_min': response['main']['temp_min'],
            'temp_max': response['main']['temp_max'],
            'pressure': response['main']['pressure'],
            'humidity': response['main']['humidity'],
            'wind_speed': response['wind']['speed'],
            'wind_dir': wind_dir,
            'clouds': response['clouds']['all'],
            'visibility': response['visibility'],
            'sunrise': sunrise,
            'sunset': sunset,
            'description': response['weather'][0]['description'],
        }

        return render_template('index.html',
                           city=city,
                           weather_data=weather_info)

    except Exception as e:
        return render_template('index.html',
                           city=city if 'city' in locals() else '',
                           error=f"Error: {str(e)}")


@app.route('/autocomplete')
def autocomplete():
    query = request.args.get('q', '')
    if len(query) < 2:
        return jsonify([])

    url = f"http://api.openweathermap.org/geo/1.0/direct?q={query}&limit=5&appid={API_KEY}"
    response = requests.get(url).json()

    suggestions = []
    for location in response:
        name = f"{location['name']}, {location.get('country', '')}"
        if 'state' in location:
            name += f", {location['state']}"
        suggestions.append({
            'name': name,
            'value': f"{location['name']},{location.get('country', '')}"
        })

    return jsonify(suggestions)


@app.route('/history')
def show_history():
    try:
        with app.app_context():
            # Get request history with weather information
            history = db.session.query(CitiesDates, WeatherDetails) \
                .join(WeatherDetails, CitiesDates.weather_id == WeatherDetails.id) \
                .order_by(CitiesDates.datetime.desc()) \
                .all()

            # Convert results to convenient format
            history_data = []
            for city_date, weather in history:
                history_data.append({
                    'city_name': city_date.city_name,
                    'datetime': city_date.datetime,
                    'weather': {
                        'temperature': weather.temperature,
                        'feels_like': weather.feels_like,
                        'temp_min': weather.temp_min,
                        'temp_max': weather.temp_max,
                        'pressure': weather.pressure,
                        'humidity': weather.humidity,
                        'wind_speed': weather.wind_speed,
                        'wind_dir': weather.wind_dir,
                        'clouds': weather.clouds,
                        'visibility': weather.visibility,
                        'sunrise': weather.sunrise,
                        'sunset': weather.sunset,
                        'description': weather.description,
                    }
                })

        return render_template('index.html', history_data=history_data)

    except Exception as e:
        return render_template('index.html',
                           error=f"Error getting history: {str(e)}")


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        #Add a comment
    app.run(host='0.0.0.0', port=5000)