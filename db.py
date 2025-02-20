import sqlite3
from datetime import datetime

import pytz


def init_db():
    conn = sqlite3.connect('weather.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS WeatherHistory (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            city TEXT NOT NULL,
            temperature REAL NOT NULL,
            wind REAL NOT NULL,
            cloud REAL NOT NULL,
            date_time TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def create_forecast():
    conn = sqlite3.connect('weather.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS saved_forecasts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            city TEXT NOT NULL,
            temperature REAL NOT NULL,
            wind REAL NOT NULL,
            cloud INTEGER NOT NULL,
            date_time TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def db_add_forecast(city, temperature, wind, cloud, date_time):
    conn = sqlite3.connect('weather.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO saved_forecasts (city, temperature, wind, cloud, date_time)
        VALUES (?, ?, ?, ?, ?)
    ''', (city, temperature, wind,cloud, date_time))
    conn.commit()
    conn.close()

def get_forecasts():
    conn = sqlite3.connect('weather.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM saved_forecasts ORDER BY date_time DESC')
    forecasts = cursor.fetchall()
    conn.close()
    print(forecasts)
    return forecasts



def add_entry(city, temperature, wind, cloud):
    conn = sqlite3.connect('weather.db')
    cursor = conn.cursor()
    date_time = datetime.now(pytz.timezone('Asia/Atyrau')).strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute('''
        INSERT INTO WeatherHistory (city, temperature, wind, cloud, date_time)
        VALUES (?, ?, ?, ?, ?)
    ''', (city, temperature, wind, cloud, date_time))
    conn.commit()
    conn.close()


def get_history(limit=5):
    conn = sqlite3.connect('weather.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT city, temperature, wind, cloud, date_time
        FROM WeatherHistory
        ORDER BY date_time DESC
        LIMIT ?
    ''', (limit,))
    rows = cursor.fetchall()
    conn.close()
    return rows

def clear_history():
    conn = sqlite3.connect('weather.db')
    cursor = conn.cursor()
    cursor.execute('''
        DELETE FROM WeatherHistory
        WHERE id IN (
            SELECT id FROM WeatherHistory
            ORDER BY date_time DESC
            LIMIT 5
        )
    ''')


    conn.commit()
    conn.close()
