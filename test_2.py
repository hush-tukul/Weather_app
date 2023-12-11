# Імпортування необхідних бібліотек
import requests
from datetime import datetime as dt
import os
from dotenv import load_dotenv

# Завантаження змінних середовища
load_dotenv()
BASE_URL = 'http://127.0.0.1:5000/weather'
X_TOKEN = os.getenv('X_TOKEN')

# Функція для перетворення температури з Кельвіна в Цельсію
def kelvin_to_celsius(temp_kelvin):
   return temp_kelvin - 273.15

# Функція для отримання температури для певної дати
def get_temperature_for_date(date):
   params = {'day': date}
   headers = {'x-token': X_TOKEN}
   response = requests.get(BASE_URL, params=params, headers=headers)

   # Перевірка успішності запиту
   if response.status_code == 200:
       weather_data = response.json()

       print(f"Temperature data for {date}:")

       # Перевірка, чи є дані списком
       if isinstance(weather_data, list):
           for data_point in weather_data:
               timestamp = data_point.get('timestamp')
               temperature_kelvin = data_point.get('main', {}).get('temp')

               # Перевірка, чи є в даних час і температура
               if timestamp is not None and temperature_kelvin is not None:
                  timestamp_human_readable = dt.utcfromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
                  temperature_celsius = kelvin_to_celsius(temperature_kelvin)
                  print(f"Time: {timestamp_human_readable}, Temperature: {temperature_celsius:.2f} °C")
               else:
                  print("Timestamp or temperature not found in the data.")
       else:
           timestamp = weather_data.get('timestamp')
           temperature_kelvin = weather_data.get('main', {}).get('temp')

           # Перевірка, чи є в даних час і температура
           if timestamp is not None and temperature_kelvin is not None:
               timestamp_human_readable = dt.utcfromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
               temperature_celsius = kelvin_to_celsius(temperature_kelvin)
               print(f"Time: {timestamp_human_readable}, Temperature: {temperature_celsius:.2f} °C")
           else:
               print("Timestamp or temperature not found in the data.")
   else:
       print("Error:", response.json())

# Використання функції для отримання температури для певної дати
desired_date = '2023-12-11'
get_temperature_for_date(desired_date)




