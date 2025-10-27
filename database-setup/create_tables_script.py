import oracledb
import os

# --- Database Connection Details (Replace with your actual credentials) ---
# It's recommended to use environment variables for security.
DB_USER = os.environ.get("DB_USER", "C##abdeljalil")
DB_PASSWORD = os.environ.get("DB_PASSWORD", "toor")
DB_HOST = os.environ.get("DB_HOST", "localhost")
DB_PORT = os.environ.get("DB_PORT", "1521")
DB_SERVICE_NAME = os.environ.get("DB_SERVICE_NAME", "freepdb1")

# Construct the connection string
dsn = f"{DB_HOST}:{DB_PORT}/{DB_SERVICE_NAME}"

# Path to the SQL script
sql_script_path = os.path.join(os.path.dirname(__file__), 'create_tables.sql')

def execute_sql_from_file(file_path):
    """Reads and executes a SQL script."""
    try:
        with oracledb.connect(user=DB_USER, password=DB_PASSWORD, dsn=dsn) as connection:
            with connection.cursor() as cursor:
                with open(file_path, 'r') as f:
                    # Read the script, remove leading/trailing whitespace and the trailing '/'
                    sql_script = f.read().strip().rstrip('/')
                    # The script uses PL/SQL, so we execute it as a single block.
                    cursor.execute(sql_script)
                print(f"Successfully executed SQL script: {file_path}")
    except oracledb.DatabaseError as e:
        print(f"Database error: {e}")
    except FileNotFoundError:
        print(f"Error: SQL script not found at {file_path}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    execute_sql_from_file(sql_script_path)
