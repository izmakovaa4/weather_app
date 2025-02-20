import os
import sqlite3
from datetime import datetime
import pytz
from flask import Flask, render_template, request, redirect, url_for, jsonify
import requests
from db import init_db, add_entry, get_history, clear_history, get_forecasts, db_add_forecast


app = Flask(__name__)

@app.route('/')
def index():
    current_time = datetime.now(pytz.timezone('Asia/Atyrau')).strftime("%Y-%m-%d %H:%M:%S")
    return render_template('index.html', city=None,temperature=None, cloud=None, current_time=current_time)


@app.route('/weather', methods=['POST'])
def weather():
    city_name = request.form.get('city')

    if not city_name:
        return "Город не указан", 400

    url = "https://weatherapi-com.p.rapidapi.com/current.json"
    headers = {
        "x-rapidapi-key": "6d91170cc5msh225dae2269b1fa4p1f32e5jsn93c87a393fbd",
        "x-rapidapi-host": "weatherapi-com.p.rapidapi.com"
    }
    params = {"q": city_name}
    response = requests.get(url, headers=headers, params=params)

    if response.status_code != 200:
        return "Ошибка при получении данных о погоде.", 500

    data = response.json()
    if 'current' not in data:
        return "Ошибка при получении данных о погоде.", 500

    temperature = data['current']['temp_c']
    cloud = data['current']['cloud']
    wind = data['current']['wind_kph']

    print(f"Temperature: {temperature}, Cloud: {cloud}, Wind: {wind}")

    add_entry(city_name, temperature, wind, cloud)

    return render_template('weather.html', city=city_name, temperature=temperature, cloud=cloud, wind=wind)

@app.route('/history')
def history():
    history = get_history()
    return render_template('history.html', history=history)

@app.route('/clear_history', methods=['POST'])
def clear_history_route():
    clear_history()
    return jsonify(success=True)

#recent
@app.route('/add_forecast', methods=['POST'])
def add_forecast_route():
    city = request.form['city']
    temperature = request.form['temperature']
    wind = request.form['wind']
    cloud = request.form['cloud']
    date_time = request.form['date_time']
    try:
        date_time = datetime.strptime(date_time, "%Y-%m-%d %H:%M:%S").strftime("%Y-%m-%d %H:%M:%S")
    except ValueError:
        date_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"Adding forecast: {city}, {temperature}, {wind}, {cloud}, {date_time}")
    db_add_forecast(city, temperature, wind, cloud, date_time)

    return redirect(url_for('saved_forecasts'))

@app.route('/saved_forecasts')
def saved_forecasts():
    forecasts = get_forecasts()
    return render_template('saved_forecasts.html', forecasts=forecasts)

#recent

if __name__ == '__main__':
    init_db()  # Инициализируем базу данных и создаем таблицы заново
    app.run(debug=True)

