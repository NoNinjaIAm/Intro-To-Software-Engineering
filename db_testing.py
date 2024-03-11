import os
import queries
import sql_functions

# Database connection details
host = os.environ.get('DB_HOST')
user = os.environ.get('DB_USER')
password = os.environ.get('DB_PASSWORD')
database = os.environ.get('DB_DATABASE')

conn = sql_functions.create_connection(host, user, password, database)

print(sql_functions.execute_statement(conn, queries.DROP_ALL_TABLES, multi=True))
print(sql_functions.execute_sql_file(conn, "init_database.sql"))
print(sql_functions.execute_sql_file(conn, "add_test_data.sql"))
print(sql_functions.execute_statement(conn, queries.SELECT_ALL_USERS))

conn.close()