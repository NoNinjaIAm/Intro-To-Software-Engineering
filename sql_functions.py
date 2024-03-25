import sqlite3

def create_connection(database_file):
    try:
        connection = sqlite3.connect(database_file)
        print(f"Connected to SQLite database: {database_file}")
        return connection
    except sqlite3.Error as e:
        print(f"Error: {e}")
        return None

def execute_statement(connection, statement, fetch_results=True):
    try:
        cursor = connection.cursor()
        cursor.execute(statement)

        if fetch_results:
            result = cursor.fetchall()
            print(f"Statement executed successfully. Result: {result}")

        connection.commit()

    except sqlite3.Error as e:
        print(f"Error executing statement: {e}")

def execute_sql_file(connection, file_path, fetch_results=True):
    try:
        cursor = connection.cursor()

        with open(file_path, 'r') as file:
            sql_script = file.read()

            cursor.executescript(sql_script)

        if fetch_results:
            result = cursor.fetchall()
            print(f"Statement executed successfully. Result: {result}")

        connection.commit()

    except sqlite3.Error as e:
        print(f"Error executing SQL file: {e}")
