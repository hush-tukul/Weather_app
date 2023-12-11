import json

import requests
from datetime import datetime as dt
import os


BASE_URL = 'http://127.0.0.1:5000/weather'
X_TOKEN = 'x_token'  # Replace 'your_x_token_here' with your actual x_token


def kelvin_to_celsius(temp_kelvin):
    return temp_kelvin - 273.15  # Conversion from Kelvin to Celsius


def get_temperature_for_date(date):
    params = {'day': date}  # Update 'day' instead of 'date' for the query parameter
    headers = {'x-token': X_TOKEN}
    response = requests.get(BASE_URL, params=params, headers=headers)

    if response.status_code == 200:
        weather_data = response.json()

        print(f"Temperature data for {date}:")

        if isinstance(weather_data, list):
            for data_point in weather_data:
                timestamp = data_point.get('timestamp')
                temperature_kelvin = data_point.get('main', {}).get('temp')

                if timestamp is not None and temperature_kelvin is not None:
                    # Convert timestamp to human-readable date
                    timestamp_human_readable = dt.utcfromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')

                    # Convert temperature from Kelvin to Celsius
                    temperature_celsius = kelvin_to_celsius(temperature_kelvin)

                    print(
                        f"Time: {timestamp_human_readable}, Temperature: {temperature_celsius:.2f} °C")  # Print formatted data
                else:
                    print("Timestamp or temperature not found in the data.")
        else:
            timestamp = weather_data.get('timestamp')
            temperature_kelvin = weather_data.get('main', {}).get('temp')

            if timestamp is not None and temperature_kelvin is not None:
                # Convert timestamp to human-readable date
                timestamp_human_readable = dt.utcfromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')

                # Convert temperature from Kelvin to Celsius
                temperature_celsius = kelvin_to_celsius(temperature_kelvin)

                print(
                    f"Time: {timestamp_human_readable}, Temperature: {temperature_celsius:.2f} °C")  # Print formatted data
            else:
                print("Timestamp or temperature not found in the data.")
    else:
        print("Error:", response.json())

# Replace 'desired_date' with the date for which you want weather data in 'YYYY-MM-DD' format
desired_date = '2023-12-11'  # For example, fetching weather for December 11, 2023

get_temperature_for_date(desired_date)



