import sqlite3
from faker import Faker
from flask import Flask, request
from flask_restful import Resource, Api
from sqlalchemy import create_engine, text
from json import dumps
from flask_jsonpify import jsonify
import random
import json

# Количество записей
count_users = 1000

# Создаем соединение с базой данных
conn = sqlite3.connect('cinema.db')
cursor = conn.cursor()

# Проверяем, существует ли таблица
cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users'")
if cursor.fetchone() is None:
   # Создаем таблицу, если она не существует
   cursor.execute("""
       CREATE TABLE users (
           id INTEGER PRIMARY KEY,
           name TEXT,
           surname TEXT,
           patronymic TEXT,
           passport TEXT,
           birth_date TEXT,
           inn TEXT,
           city TEXT,
           phone_number TEXT,
           film TEXT,
           date TEXT
       )
   """)

# Создаем экземпляр класса Faker для генерации данных
fake = Faker('ru_RU')

# Создаем список из случайных названий фильмов
films = [fake.catch_phrase() for _ in range(count_users // 15 + 1)]

# Создаем словарь для хранения дат для каждого фильма
film_dates = {}
while films:
   # Выбираем от 1 до 3 случайных фильмов
   selected_films = [films.pop() for _ in range(min(len(films), random.randint(1, 3)))]
   # Генерируем дату для выбранных фильмов
   date = fake.date_between(start_date='-1y', end_date='today').strftime("%Y-%m-%d")
   for film in selected_films:
       film_dates[film] = date

# Заполняем базу данных
for _ in range(count_users):
    # Случайно выбираем пол
    gender = random.choice(['male', 'female'])
    if gender == 'male':
        name = fake.first_name_male()
        surname = fake.last_name_male()
        patronymic = fake.middle_name_male()
    else:
        name = fake.first_name_female()
        surname = fake.last_name_female()
        patronymic = fake.middle_name_female()

    passport = fake.unique.random_number(digits=10)
    birth_date = fake.date_of_birth(minimum_age=18, maximum_age=90).strftime("%Y-%m-%d")
    inn = fake.unique.random_number(digits=12)
    city = fake.city()
    phone_number = '7' + str(random.randint(900, 999)) + ''.join([str(random.randint(0, 9)) for _ in range(7)])
    film = random.choice(list(film_dates.keys()))
    date = film_dates[film]
    cursor.execute(
       "INSERT INTO users (name, surname, patronymic, passport, birth_date, inn, city, phone_number, film, date) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
       (name, surname, patronymic, passport, birth_date, inn, city, phone_number, film, date)
   )

# Сохраняем изменения
conn.commit()

# Закрываем соединение с базой данных
conn.close()

# Создаем соединение с базой данных через SQLAlchemy
db_connect = create_engine('sqlite:///cinema.db')

# Создаем Flask приложение
app = Flask(__name__)
api = Api(app)

# Главная страница
@app.route('/')
def home():
   return "Welcome to the Cinema API!"

# Ресурс для получения записей по заданным параметрам
class Tickets(Resource):
   def get(self):
       conn = db_connect.connect()
       query_params = request.args
       query_string = " AND ".join([f"{key} = :{key}" for key in query_params.keys()])
       query = conn.execute(text(f"select * from users where {query_string}"), query_params)
       result = {'data': [dict(zip(tuple(query.keys()), i)) for i in query.cursor]}
       return app.response_class(
           response=json.dumps(result, ensure_ascii=False),
           mimetype='application/json'
       )

# Добавляем ресурс в API
api.add_resource(Tickets, '/search')

if __name__ == '__main__':
   app.run(port='5002')