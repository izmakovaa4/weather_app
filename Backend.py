from apps import Flask, render_template, request, redirect, url_for, jsonify
import requests
import sqlite3
from datetime import datetime

app = Flask(__name__)

# Настройки API
API_KEY = "6d91170cc5msh225dae2269b1fa4p1f32e5jsn93c87a393fbd"
API_HOST = "weatherapi-com.p.rapidapi.com"
API_URL = "https://weatherapi-com.p.rapidapi.com/current.json"

# Подключение к базе данных
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

# Главная страница
@app.route('/')
def index():
    return render_template('index.html')

# Показать текущую погоду
@app.route('/weather', methods=['POST'])
def weather():
    city_name = request.form['city']
    headers = {
        "x-rapidapi-key": API_KEY,
        "x-rapidapi-host": API_HOST
    }
    params = {"q": city_name}
    response = requests.get(API_URL, headers=headers, params=params)
    if response.status_code == 200:
        data = response.json()
        temperature = data['current']['temp_c']
        cloud = data['current']['cloud']
        wind = data['current']['wind_kph']
        weather_info = {
            "city": city_name,
            "temperature": temperature,
            "cloud": cloud,
            "wind": wind
        }
        # Сохранение в базу данных
        conn = get_db_connection()
        conn.execute('INSERT INTO search_history (city_name, timestamp) VALUES (?, ?)',
                     (city_name, datetime.now()))
        conn.commit()
        conn.close()
        return render_template('weather.html', weather=weather_info)
    else:
        return "Не удалось получить данные о погоде"

# История запросов
@app.route('/history')
def history():
    conn = get_db_connection()
    history = conn.execute('SELECT * FROM search_history ORDER BY timestamp DESC LIMIT 5').fetchall()
    conn.close()
    return render_template('history.html', history=history)

# Очистка истории запросов
@app.route('/clear_history')
def clear_history():
    conn = get_db_connection()
    conn.execute('DELETE FROM search_history')
    conn.commit()
    conn.close()
    return redirect(url_for('history'))

# Просмотр сохраненного прогноза для города
@app.route('/city/<int:id>')
def city(id):
    conn = get_db_connection()
    city = conn.execute('SELECT * FROM search_history WHERE id = ?', (id,)).fetchone()
    conn.close()
    if city is None:
        return "Город не найден"
    return render_template('weather.html', weather=city)

if __name__ == '__main__':
    app.run(debug=True)
