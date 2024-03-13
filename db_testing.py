import queries
import sql_functions

# Database connection details
database_file = "database.db"

# Create SQLite connection
conn = sql_functions.create_connection(database_file)

for query in queries.drop_queries.values():
    sql_functions.execute_statement(conn, query, fetch_results=False)

# Execute schema initialization SQL file
schema_file_path = "init_database.sql"
sql_functions.execute_sql_file(conn, schema_file_path, fetch_results=False)

# Execute SQL file with test data
test_data_file_path = "add_test_data.sql"
sql_functions.execute_sql_file(conn, test_data_file_path, fetch_results=False)

sql_functions.execute_statement(conn, queries.SELECT_ALL_USERS)

# Close the SQLite connection
conn.close()