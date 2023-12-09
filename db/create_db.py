import mysql.connector


def delete_db():
    query_delete = """DROP DATABASE algo;"""
    cursor.execute(query_delete)


def make_db():
    query0 = """CREATE DATABASE algo"""
    query1 = """CREATE TABLE algo.users(
                id_user INT AUTO_INCREMENT PRIMARY KEY,
                username TEXT,
                login TEXT,
                password TEXT,
                photo TEXT) """
    cursor.execute(query0)
    cursor.execute(query1)


if __name__ == '__main__':
    db = mysql.connector.connect(
        host="localhost",
        user="Admin",
        password="Admin",
    )
    cursor = db.cursor()
    delete_db()
    make_db()
