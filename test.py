# Імпортування необхідних бібліотек
import json
import threading
import time
import requests
import schedule
from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask, jsonify
import os
from dotenv import load_dotenv

# Завантаження змінних середовища
load_dotenv()

# Ініціалізація Flask-додатку та планувальника на фоновому режимі
app = Flask(__name__)
scheduler = BackgroundScheduler()
scheduler.start()

# Встановлення URL API та необхідних параметрів
BASE_URL = 'http://api.openweathermap.org/data/2.5/weather'
API_KEY = os.getenv('API_KEY')
X_TOKEN = os.getenv('X_TOKEN')
CITY = 'Kyiv'

# Функція для отримання даних про погоду
def get_weather():
  params = {
      'q': CITY,
      'appid': API_KEY
  }

  headers = {
      'x-token': X_TOKEN
  }

  # Відправка GET-запиту до API
  response = requests.get(BASE_URL, params=params, headers=headers)

  # Перевірка успішності запиту
  if response.status_code == 200:
      weather_data = response.json()

      # Додавання часу до даних про погоду
      timestamp = int(time.time()) # Отримання поточного часу
      weather_data['timestamp'] = timestamp # Додавання часу до даних

      # Завантаження існуючих даних про погоду
      try:
          with open('weather_data.json', 'r') as file:
              data = json.load(file)
      except (FileNotFoundError, json.JSONDecodeError):
          data = []

      # Переконання, що 'data' є списком, навіть якщо він починається порожнім або з попередніх даних JSON
      if not isinstance(data, list):
          data = []

      # Додавання нових даних про погоду до списку
      data.append(weather_data)

      # Збереження оновлених даних про погоду
      with open('weather_data.json', 'w') as file:
          json.dump(data, file)
  else:
      print('Error: Weather data not available')

# Функція для виконання запланованих завдань
def update_weather():
  while True:
      schedule.run_pending()
      time.sleep(1)

# Маршрут Flask для отримання даних про погоду
@app.route('/weather')
def retrieve_weather():
  try:
      with open('weather_data.json', 'r') as file:
          weather = json.load(file)
          return jsonify(weather)
  except (FileNotFoundError, json.JSONDecodeError):
      return jsonify({'error': 'Weather data not available'}), 404

# Головний блок виконання
if __name__ == '__main__':
  get_weather() # Отримання даних про погоду спочатку
  schedule.every().hour.do(get_weather) # Запланувати отримання даних про погоду кожну годину

  # Запуск нового потоку для виконання планувальника
  update_thread = threading.Thread(target=update_weather)
  update_thread.start()

  # Запуск Flask-додатку
  app.run()




