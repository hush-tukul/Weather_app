import datetime
import json
import threading
import time

import requests
import schedule
from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask, request, jsonify


app = Flask(__name__)
scheduler = BackgroundScheduler()
scheduler.start()


BASE_URL = 'http://api.openweathermap.org/data/2.5/weather'

API_KEY = 'ca385afe9e09204fa0ebfa0b4f968f12'
X_TOKEN = 'x_token'
CITY = 'Kyiv'


def get_weather():
    params = {
        'q': CITY,
        'appid': API_KEY
    }

    headers = {
        'x-token': X_TOKEN
    }

    response = requests.get(BASE_URL, params=params, headers=headers)

    if response.status_code == 200:
        weather_data = response.json()

        # Add timestamp to the weather data
        timestamp = int(time.time())  # Get current timestamp
        weather_data['timestamp'] = timestamp  # Add timestamp to the data

        try:
            with open('weather_data.json', 'r') as file:
                data = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            data = []

        # Ensure 'data' is a list, even if it starts empty or from previous JSON data
        if not isinstance(data, list):
            data = []

        data.append(weather_data)

        with open('weather_data.json', 'w') as file:
            json.dump(data, file)
    else:
        print('Error: Weather data not available')

def update_weather():
    while True:
        schedule.run_pending()
        time.sleep(1)

@app.route('/weather')
def retrieve_weather():
    try:
        with open('weather_data.json', 'r') as file:
            weather = json.load(file)
            return jsonify(weather)
    except (FileNotFoundError, json.JSONDecodeError):
        return jsonify({'error': 'Weather data not available'}), 404

if __name__ == '__main__':
    get_weather()  # Get weather data initially
    schedule.every(1).minutes.do(get_weather)  # Schedule to get weather data every 5 minutes

    update_thread = threading.Thread(target=update_weather)
    update_thread.start()

    app.run()




