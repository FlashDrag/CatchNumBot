import psycopg2 as ps
from config import DB_URL


class BotDB:
    def __init__(self, DB_URL):
        self.conn = ps.connect((DB_URL), sslmode='require')
        self.cursor = self.conn.cursor()
        if self.conn:
            print("Bot успешно подключен к базе heroku_postgresql!")


    def user_exists(self, user_id):
        """Проверяем, есть ли юзер в базе"""
        result = self.cursor.execute("SELECT user_id FROM users WHERE user_id = {user_id}")
        return bool(len(result.fetchall()))


    def add_user(self, user_id, first_name, last_name, username):
        """Добавляем юзера в базу"""
        self.cursor.execute("""
        INSERT INTO users (user_id, first_name, last_name, username)
        VALUES (%s,%s,%s,%s)""", (user_id, first_name, last_name, username))
        return self.conn.commit()
    

    def get_user_name(self, first_name):
        """Достаем id юзера в базе по его user_id"""
        result = self.cursor.execute("SELECT `first_name` FROM `users` WHERE `user_id` = ?", (first_name,))
        return result.fetchone()[0]