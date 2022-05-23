import sqlite3 as sq
# https://youtu.be/m0ZRms4p7fc   -- туториал по базе
# https://github.com/DaniilSemizhonov/MrGiraffeBot/blob/main/db.py


class BotDB:
    def __init__(self, db_file):
        self.conn = sq.connect(db_file)
        self.cursor = self.conn.cursor()
        if self.conn:
            print("Data conn sqlite подключена!")


    def setup(self):
        print("creating table")
        stmt = "CREATE TABLE IF NOT EXISTS users (user_id, first_name, last_name, username)"
        self.conn.execute(stmt)
        self.conn.commit()


    def user_exists(self, user_id):
        """Проверяем, есть ли юзер в базе"""
        result = self.cursor.execute("SELECT `user_id` FROM `users` WHERE `user_id` = ?", (user_id,))
        return bool(len(result.fetchall()))


    def add_user(self, user_id, first_name, last_name, username):
        """Добавляем юзера в базу"""
        self.cursor.execute("INSERT INTO users VALUES(?,?,?,?)", (user_id, first_name, last_name, username))
        return self.conn.commit()

    # def get_user_name(self, first_name):
    #     """Достаем id юзера в базе по его user_id"""
    #     result = self.cursor.execute("SELECT `first_name` FROM `users` WHERE `user_id` = ?", (user_id))
    #     return result.fetchone()[0]

    # def get_records(self, user_name, max_num, win):
    #     """Достаем все записи"""

