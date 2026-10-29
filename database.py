import sqlite3
from sqlite3 import Connection


class DatabaseOperations():
    @staticmethod
    def get_db() -> Connection:
        connection = sqlite3.connect("finance.db")
        connection.execute("PRAGMA foreign_keys = ON")
        return connection
    @staticmethod
    def init_db():
        connection = DatabaseOperations.get_db()
        connection.execute("""CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMARY KEY , email TEXT NOT NULL UNIQUE, phone_number TEXT NOT NULL , date TEXT NOT NULL)""")
        connection.execute("""CREATE TABLE IF NOT EXISTS transactions(id INTEGER PRIMARY KEY, user_id INTEGER NOT NULL REFERENCES users(id), amount INTEGER NOT NULL, category TEXT, date TEXT NOT NULL )""")
        connection.commit()
        connection.close()

