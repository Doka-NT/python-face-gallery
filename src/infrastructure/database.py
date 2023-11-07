import sqlite3


def create_database(db_connection: sqlite3.Connection):
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
        """
            CREATE TABLE IF NOT EXISTS similar_face (
                face_id STRING,
                similar_face_id STRING
            )
        """,
    ]

    cursor = db_connection.cursor()

    for sql in sql_list:
        cursor.execute(sql)


def drop_database(db_connection: sqlite3.Connection):
    sql_list = [
        "DROP TABLE IF EXISTS face",
        "DROP TABLE IF EXISTS face_photo",
        "DROP TABLE IF EXISTS photo",
        "DROP TABLE IF EXISTS similar_face",
    ]

    cursor = db_connection.cursor()

    for sql in sql_list:
        cursor.execute(sql)
