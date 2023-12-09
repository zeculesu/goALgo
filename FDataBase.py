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
                    username TEXT,
                    login TEXT,
                    password TEXT,
                    photo TEXT) """
        res = self.cursor.execute(query0)
        res = self.cursor.execute(query1)

    def add_user(self, username, login, password, photo):
        q = """SELECT id_user FROM algo.users;"""

        self.cursor.execute(q)
        new_id = max(self.cursor.fetchall())[0] + 1 if self.cursor.fetchall() else 1
        filename = f"{new_id}.{photo.filename.split('.')[1]}"
        query = f"""INSERT INTO algo.users (id_user, username, login, password, photo)
                        VALUES (null, "{username}", "{login}", "{password}", "{filename}");"""
        photo.save(f"static/img/users/{filename}")
        self.cursor.execute(query)
        self.__db.commit()
    # def getMenu(self):
    #     sql = '''SELECT * FROM user'''
    #     try:
    #         self.__cur.execute(sql)
    #         res = self.__cur.fetchall()
    #         if res: return res
    #     except:
    #         print("Ошибка чтения из БД")
    #     return []
