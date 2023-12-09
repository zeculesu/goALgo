import mysql.connector


class FDataBase:
    def __init__(self, db):
        self.__db = db
        self.cursor = db.cursor()

    def delete_db(self):
        query_delete = """DROP DATABASE algo;"""
        self.cursor.execute(query_delete)

    def make_db(self):
        query0 = """CREATE DATABASE algo"""
        query1 = """CREATE TABLE algo.users(
                    id_user INT AUTO_INCREMENT PRIMARY KEY,
                    name TEXT,
                    surname TEXT,
                    thirdname TEXT,
                    documentID TEXT,
                    login TEXT,
                    password TEXT,
                    photo TEXT) """
        res = self.cursor.execute(query0)
        res = self.cursor.execute(query1)

    def add_user(self, name, surname, thirdname, documentID, login, password, photo):
        q = """SELECT id_user FROM algo.users;"""

        self.cursor.execute(q)
        k = self.cursor.fetchall()
        if k:
            new_id = max(k)[0] + 1
        else:
            new_id = 1
        filename = f"{new_id}.{photo.filename.split('.')[1]}"
        query = f"""INSERT INTO algo.users (id_user, name, surname, thirdname, documentID, login, password, photo)
                        VALUES (null, "{name}", "{surname}", "{thirdname}", "{documentID}", "{login}", "{password}", "{filename}");"""
        photo.save(f"static/img/users/{filename}")
        self.cursor.execute(query)
        self.__db.commit()

    def getUserByLogin(self, login):
        q = f"""SELECT * FROM algo.users WHERE login = "{login}";"""
        self.cursor.execute(q)
        res = self.cursor.fetchall()
        return res

    def getUser(self, userid):
        q = f"""SELECT * FROM algo.users WHERE id_user = "{userid[0]}";"""
        self.cursor.execute(q)
        res = self.cursor.fetchall()
        return userid
