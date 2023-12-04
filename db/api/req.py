def add_user(cursor,username, login, password, photo):
    q = """SELECT id_user FROM users;"""

    cursor.execute(q)
    new_id = max(cursor.fetchall())[0]
    filename = f"{new_id}.{photo.filename.split('.')[1]}"
    query = f"""INSERT INTO users (id_user, username, login, password, photo)
                    VALUES (null, "{username}", "{login}", "{password}", "{filename}");"""
    photo.save(f"static/img/users/{filename}")
    cursor.execute(query)
