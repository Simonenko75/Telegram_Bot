
import sqlite3


class BotDB:

    def __init__(self, db_file):
        """Ініціалізація з'єднання з БД"""
        self.conn = sqlite3.connect(db_file)
        self.cursor = self.conn.cursor()

    def user_exists(self, user_id):
        """Перевірка чи існую БД"""
        result = self.cursor.execute("SELECT `id` FROM `users` WHERE `user_id` = ?", (user_id,))
        return bool(len(result.fetchall()))

    def get_user_id(self, user_id):
        """Отримання id користувача по його user_id в телеграмі"""
        result = self.cursor.execute("SELECT `user_id` FROM `users` WHERE `user_id` = ?", (user_id,))
        return int(*result.fetchall()[0])

    def add_user(self, user_id):
        """Додання користувача у БД"""
        self.cursor.execute("INSERT INTO `users` (`user_id`) VALUES (?)", (user_id,))
        return self.conn.commit()

    def add_date_interview(self, user_id, first_name, last_name, favorite_sport, favorite_movie_genre, gender, relationship):
        """Додання до бази даних отриманих в результаті опитування даних"""
        self.cursor.execute("INSERT INTO `interview` ("
                            "`user_id`,"
                            "`first_name`,"
                            "`last_name`,"
                            "`favorite_sport`,"
                            "`favorite_movie_genre`,"
                            "`gender`,"
                            "`relationship`)"
                            "VALUES (?, ?, ?, ?, ?, ?, ?)",
                            (self.get_user_id(user_id),
                             first_name,
                             last_name,
                             favorite_sport,
                             favorite_movie_genre,
                             gender,
                             relationship == 'так' or relationship == 'звісно'))
        return self.conn.commit()

    def date_(self, sport, movie, gender, relationship):
        """Зчитування даних з БД"""
        try:
            # Зчитування даних опитування користувачів
            users = self.cursor.execute("SELECT"
                                        "`favorite_sport`,"
                                        "`favorite_movie_genre`,"
                                        "`gender`,"
                                        "`relationship`"
                                        "FROM `interview`")

            for s, m, g, r in tuple(users):
                sport.append(s)
                movie.append(m)
                gender.append(g)
                relationship.append(r)

            # Підтвердження змін
            self.conn.commit()

            return sport, movie, gender, relationship

        except sqlite3.Error as error:
            print("Error", error)

    def close(self):
        """Закриття з'єднення з БД"""
        self.conn.close()
