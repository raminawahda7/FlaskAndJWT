import pyodbc
server = 'tcp:sql-test-legistai.database.windows.net,1433'  # Replace with actual server details
database = 'legistai.db'
username = 'legistai-server'
password = 'Sql@123123'
driver = '{ODBC Driver 17 for SQL Server}'  # Adjust if needed

try:
    conn = pyodbc.connect(f"Driver={driver};Server={server};Database={database};UID={username};PWD={password};Trusted_Connection=no;")
    print("Connection successful!")
    conn.close()
except pyodbc.Error as ex:
    print("Connection error:", ex)