from datetime import date
from sqlite3 import Connection

from database import DatabaseOperations

class UserRepo():
    @staticmethod
    def create_user(email: str, phone:str) -> int:
        connection: Connection = DatabaseOperations.get_db()
        today = date.today()
        string_date = today.isoformat()
        try:
            row = connection.execute("""SELECT id FROM users WHERE email =?""", (email,)).fetchone()
            if row:
                user_id = row[0]
            else:
                user = connection.execute("""INSERT INTO users(email, phone_number, date) VALUES(?,?,?)""", (email, phone, string_date,))
                user_id = user.lastrowid
            connection.commit()
            return user_id
        finally:
            connection.close()
        