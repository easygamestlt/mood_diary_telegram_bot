import psycopg2
from datetime import datetime

class Db_bot:
    def __init__(self, db_url) -> None:
        self.conn = psycopg2.connect(db_url)
        self.cursor = self.conn.cursor()

    async def get_users(self):
        self.cursor.execute("SELECT id FROM users")
        return self.cursor.fetchall()

    async def get_user(self, user_id):
        self.cursor.execute(f"SELECT id, age, name, gender FROM users WHERE id = {user_id}")
        return self.cursor.fetchone()
    
    async def user_exists(self, user_id):
        self.cursor.execute("SELECT id FROM users WHERE id = %s", (user_id,))
        return bool(len(self.cursor.fetchall()))

    async def add_user(self, user_id, age, name, gender):
        self.cursor.execute("INSERT INTO users (id, age, name, gender) VALUES (%s, %s, %s, %s)",(user_id, age, name, gender))
        return self.conn.commit()

    async def checkup_date_exists(self, user_id, date):
        self.cursor.execute("SELECT date FROM feeling WHERE id = %s AND date = %s", (user_id, date))
        return bool(len(self.cursor.fetchall()))

    async def add_checkup(self, user_id, feel, mood, comment, date):
        self.cursor.execute("INSERT INTO feeling (id, feel, mood, comment, date) VALUES (%s, %s, %s, %s, %s)",(user_id, feel, mood, comment, date))
        return self.conn.commit()

    async def get_checkup_date(self, user_id):
        self.cursor.execute(f"SELECT feel, mood, comment, date FROM public.feeling WHERE (date BETWEEN '2023-{datetime.now().month}-01' AND '2023-{datetime.now().month}-30') AND id = {user_id};")
        return self.cursor.fetchall()
    
    async def close(self):
        self.conn.close()