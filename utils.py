import pyodbc
import config
def connect_to_database():
    """Connects to the Azure SQL Database using provided configuration."""
    DatabaseConfig = config.DATABASE_CONFIG
    try:
        conn = pyodbc.connect(f"Driver={DatabaseConfig['driver']};Server={DatabaseConfig['server']};Database={DatabaseConfig['database']};UID={DatabaseConfig['username']};PWD={DatabaseConfig['password']};Trusted_Connection=no;")
        return conn
    except pyodbc.Error as ex:
        print("Database connection error:", ex)
        return None

# Add other utility functions here, like token decoding (if needed)
