
from datetime import date
from sqlite3 import Connection
from database import DatabaseOperations


class TransactionRepo ():
    @staticmethod
    def create_transactions(amount:str, category:str, user_id:int)-> None: 
        connection: Connection = DatabaseOperations.get_db()
        today = date.today()
        string_date = today.isoformat()
        try:
            final_amount = float(amount)
            final_amount = round(final_amount*100)
            if final_amount <=0:
                raise ValueError("Amount cannot be less than zero")
            connection.execute("""INSERT INTO transactions(user_id, amount, category, date) VALUES(?,?,?,?)""", (user_id, final_amount, category, string_date))
            connection.commit()
        finally:
            connection.close()

    @staticmethod
    def get_transactions(user_id:int) -> list[tuple]:
        connection: Connection = DatabaseOperations.get_db()
        try:
            transactions = connection.execute("""SELECT * FROM transactions WHERE user_id = ? ORDER BY date DESC, id DESC""", (user_id,)).fetchall()
            return transactions
        finally:
            connection.close()
