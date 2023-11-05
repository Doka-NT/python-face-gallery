import sqlite3


def init_database(db_connection: sqlite3.Connection):
    sql_list = [
        """
            CREATE TABLE IF NOT EXISTS photo (
                id STRING PRIMARY KEY,
                file_path STRING
            );
        """,
        """
            CREATE TABLE IF NOT EXISTS face (
                id STRING PRIMARY KEY
            );
        """,
        """
            CREATE TABLE IF NOT EXISTS face_photo (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                face_id INTEGER,
                photo_id STRING
            )
        """,
    ]

    cursor = db_connection.cursor()

    for sql in sql_list:
        cursor.execute(sql)
