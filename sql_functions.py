import mysql.connector
from mysql.connector import Error

# Function to create a MySQL database connection
def create_connection(host, user, password, database):
    try:
        connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        if connection.is_connected():
            print(f"Connected to MySQL database: {database}")
            return connection

    except Error as e:
        print(f"Error: {e}")
        return None

# Function to execute an SQL statement and optionally fetch results
def execute_statement(connection, statement, fetch_results=True, multi=False):
    try:
        cursor = connection.cursor()
        cursor.execute(statement, multi=multi)

        if fetch_results:
            return cursor.fetchall()
        connection.commit()

    except Error as e:
        return f"Error executing statement: {e}"

# Function to run an SQL file and print the results
def execute_sql_file(connection, file_path, multi=True):
    try:
        cursor = connection.cursor()

        with open(file_path, 'r') as file:
            sql_script = file.read()
            cursor.execute(sql_script, multi=multi)

        connection.commit()
        return cursor.fetchall()

    except Error as e:
        return f"Error executing SQL file: {e}"
