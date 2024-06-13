import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class Search:
    def views(self, sql):
        self.film = input("Введите название фильма: ")
        self.date = input("Введите дату показа: ")

        sql.execute(f"SELECT id FROM films WHERE film = ? AND date = ?", (self.film, self.date))
        id_film = sql.fetchone()
        if id_film is not None:
            sql.execute(f"SELECT id_users FROM views WHERE id_film = {id_film[0]}")
            id_users = sql.fetchall()

            info_users = []
            for id_user in id_users:
                sql.execute(f"SELECT * FROM users WHERE id = {id_user[0]}")
                info_users.append(sql.fetchone())

                if len(info_users) > 0:
                    for user_data in info_users:
                        print(user_data)
                else:
                    logging.info(f"На фильм никто не пришел")
        else:
            logging.info(f"Данный фильм в указанную вами дату не найден")

    def params(self, sql, name: str = None, surname: str = None, patronymic: str = None, passport: int = None,
               birth_date: str = None, inn: int = None, city: str = None, phone_number: int = None):

        """
            Осуществляет поиск бронирования по одной или нескольким критериям

            :param sql: Курсор
            :param name: Имя
            :param surname: Фамилия
            :param patronymic: Отчество
            :param passport: Номер паспорта
            :param birth_date: Дата рождения в формате: 1976-01-04
            :param inn: ИНН
            :param city: Город
            :param phone_number: Номер телефона
            :return: История бронирования
        """

        all_query = {"name": name,
                     "surname": surname,
                     "patronymic": patronymic,
                     "passport": passport,
                     "birth_date": birth_date,
                     "inn": inn,
                     "city": city,
                     "phone_number": phone_number}

        query_params = ""
        query_string = []
        count_values = ""
        for key, value in all_query.items():
            if value is not None:
                query_params += f" {key} = ? AND"
                query_string.append(value)
                count_values += "? "

        sql.execute(f"SELECT * FROM users WHERE{query_params[0:-4]}", query_string)
        info_users = sql.fetchall()
        logging.info(f"Данные пользователей получены")

        all_views = {}

        for i in range(len(info_users)):
            sql.execute(f"SELECT id_film FROM views WHERE id_users = ?", [info_users[i][0]])
            all_views[info_users[i][0]] = sql.fetchall()[0]
            logging.info(f"Получение данных о просмотрах  [{i + 1}  из  {len(info_users)}]...")

        for i in range(len(info_users)):
            if info_users[i][0] in all_views:
                for num_id in all_views[info_users[i][0]]:
                    sql.execute(f"SELECT film, date FROM films WHERE id = ?", [num_id])
                    logging.info(f"{info_users[i]}  |  {sql.fetchall()[0]}")
            else:
                logging.info(info_users[i])

