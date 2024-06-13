import logging
import random
from faker import Faker

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class Data:
    def __init__(self):
        self.fake = Faker('ru_RU')
        self.users = []
        self.films = []
        self.views = []

    def gen_users(self, num):
        for i in range(num):
            gender = random.choice(['male', 'female'])
            if gender == 'male':
                name = self.fake.first_name_male()
                surname = self.fake.last_name_male()
                patronymic = self.fake.middle_name_male()
            else:
                name = self.fake.first_name_female()
                surname = self.fake.last_name_female()
                patronymic = self.fake.middle_name_female()

            passport = self.fake.unique.random_number(digits=10)
            birth_date = self.fake.date_of_birth(minimum_age=18, maximum_age=90).strftime("%Y-%m-%d")
            inn = self.fake.unique.random_number(digits=12)
            city = self.fake.city()
            phone_number = '7' + str(random.randint(900, 999)) + ''.join([str(random.randint(0, 9)) for _ in range(7)])

            self.users.append([name, surname, patronymic, passport, birth_date, inn, city, phone_number])

            if i % 100000 == 0:
                logging.info(f"Создание пользователей  [{i}  из  {num}]...")
            elif i + 1 == num:
                logging.info(f"Создание пользователей  [{i + 1}  из  {num}]...")
        return self.users

    def gen_films(self, num):
        for i in range(num):
            film = self.fake.catch_phrase()
            date = self.fake.date_between(start_date='-5y', end_date='today').strftime("%Y-%m-%d")

            self.films.append([film, date])

            if i % 100000 == 0:
                logging.info(f"Создание фильмов  [{i}  из  {num}]...")
            elif i + 1 == num:
                logging.info(f"Создание фильмов  [{i + 1}  из  {num}]...")
        return self.films

    def gen_views(self):
        for i in range(len(self.users)):
            if round(((i + 1) / 30) + 0.5) < int(len(self.users) / 30):
                self.views.append([i + 1, round(((i + 1) / 30) + 0.5)])
            else:
                self.views.append([i + 1, int(len(self.users) / 30)])

            if i % 100000 == 0:
                logging.info(f"Создание посещений кинотеатра  [{i}  из  {len(self.users)}]...")
            elif i + 1 == len(self.users):
                logging.info(f"Создание посещений кинотеатра   [{i + 1}  из  {len(self.users)}]...")

        return self.views


class Database_save(Data):
    def users_add(self, sql, db, num):
        sql.executemany("INSERT INTO users(name, surname, patronymic, passport, birth_date, inn, city, phone_number)"
                        "VALUES (?, ?, ?, ?, ?, ?, ?, ?)", (self.gen_users(num)))
        db.commit()
        logging.info(f"Пользователи добавлены в БД")

    def films_add(self, sql, db, num):
        sql.executemany("INSERT INTO films(film, date)"
                        "VALUES (?, ?)", (self.gen_films(num)))
        db.commit()
        logging.info(f"Фильмы добавлены в БД")

    def views_add(self, sql, db):
        sql.executemany("INSERT INTO views(id_users, id_film)"
                        "VALUES (?, ?)", (self.gen_views()))
        db.commit()
        logging.info(f"Просмотры добавлены в БД")


class Create(Database_save):
    def test(self, sql, db, num):
        self.users_add(sql, db, num)
        self.films_add(sql, db, int(num / 30))
        self.views_add(sql, db)
