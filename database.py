import sqlite3


def execute_query(sql_query):
    connection = sqlite3.connect("sales.db")
    cursor = connection.cursor()

    cursor.execute(sql_query)

    result = cursor.fetchall()

    connection.close()

    return result