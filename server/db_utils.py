import sqlite3
import aiosqlite
import datetime
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class DBUtils:
    def __init__(self, db_name):
        self.db_name = db_name
        self.conn = sqlite3.connect(self.db_name, check_same_thread=False)
        self.cursor = self.conn.cursor()

    def create_table(self, table_name, columns):
        query = f"CREATE TABLE IF NOT EXISTS {table_name} ({columns})"
        self.cursor.execute(query)
        self.conn.commit()

    def insert(self, table_name, columns, values):
        query = f"INSERT INTO {table_name} ({columns}) VALUES ({values})"
        self.cursor.execute(query)
        self.conn.commit()

    def select(self, table_name, columns, condition='1=1'):
        query = f"SELECT {columns} FROM {table_name} WHERE {condition}"

        logger.debug(f"Executing query {query}")

        self.cursor.execute(query)
        return self.cursor.fetchall()

    def update(self, table_name, columns, condition):
        query = f"UPDATE {table_name} SET {columns} WHERE {condition}"
        self.cursor.execute(query)
        self.conn.commit()

    def delete(self, table_name, condition):
        query = f"DELETE FROM {table_name} WHERE {condition}"
        self.cursor.execute(query)
        self.conn.commit()

    def execute_query(self, query):
        self.cursor.execute(query)
        self.conn.commit()

    def execute_query_with_return(self, query):
        self.cursor.execute(query)
        return self.cursor.fetchall()
    
    def execute_query_with_return_one(self, query):
        self.cursor.execute(query)
        return self.cursor.fetchone()
    
    def execute_script(self, script):
        logger.debug(f"Executing script {script}")
        
        with open(script, 'r') as sql_script:

            self.cursor.executescript(sql_script.read())
        logger.debug(f"Finished executing script {script}")
        self.conn.commit()

    def add_reservation(self, customer_id, equipment, start_date, end_date, cost, downpayment, location):
        #print(f"'{customer_id}', '{equipment}', '{start_date}', '{end_date}', 'TRUE', '{cost}', '{downpayment}','{location}'")
        self.insert("reservations", "username, equipment, start_date, end_date, active, cost, downpayment, location",
                    f"'{customer_id}', '{equipment}', '{start_date}', '{end_date}', TRUE, '{cost}', '{downpayment}','{location}'")
        
    def show_reservations(self):
        return self.select("reservations", "*", "active = TRUE")
    
    def cancel_reservation(self, reservation_id : int) -> tuple:
        self.update("reservations", "active = FALSE", f"reservation_id = {reservation_id}")

        # return the downpayment and reservation_date
        res = self.select("reservations", "downpayment, start_date", f"reservation_id = {reservation_id}")
        
        start_date = res[0][1]
        start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d %H:%M:%S')

        downpayment = res[0][0]

        return downpayment, start_date
        

    def check_reservation(self, reservation_id : int) -> list:
    
        return self.select("reservations", "*", f"reservation_id = {reservation_id}")
    
    def list_reservations(self, start_date : datetime.datetime, end_date : datetime.datetime):
        return self.select("reservations", "*", f"start_date >= '{start_date}' AND end_date <= '{end_date}'")
    
    def remove_user(self, username : str):
        self.update("users", "active = FALSE", f"username = '{username}'")

    def add_user(self, username : str, first_name : str, role : str) -> None:

        self.insert("users", "username, first_name, active", f"'{username}', '{first_name}', 'TRUE'")
        # get user id
        uid=self.select("users","user_id", f"username = '{username}'")
        if uid:
            uid=uid[0][0]
        else:
            return
        # get role id
        role=self.select("roles","role_id", f"role = '{role}'")
        if role:
            role=role[0][0]
        else:
            return

        add = f"'{uid}', '{role}'"
        self.insert("user_roles", "user_id, role_id", add)

    def change_user_role(self, username : str, role : str) -> None:
        # get role id
        role=self.select("roles","role_id", f"role = '{role}'")
        if role:
            role=role[0][0]
        else:
            return
        # get user id
        uid=self.select("users","user_id", f"username = '{username}'")
        if uid:
            uid=uid[0][0]


            self.update("user_roles", f"role_id = '{role}'", f"user_id = {uid}")

    def login_user(self, username : str) -> str:
        print(f"username = '{username}' and active = TRUE")
        return self.select("users", "first_name", f"username = '{username}' and active = 'TRUE'")[0][0]

    def close(self):
        self.conn.close()