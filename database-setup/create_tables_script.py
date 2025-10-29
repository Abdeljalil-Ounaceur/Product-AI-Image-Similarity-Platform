import oracledb
import os

if __name__ == "__main__":
    DB_USER = os.environ.get("DB_USER", "C##abdeljalil")
    DB_PASSWORD = os.environ.get("DB_PASSWORD", "toor")
    DB_HOST = os.environ.get("DB_HOST", "localhost")
    DB_PORT = os.environ.get("DB_PORT", "1521")
    DB_SERVICE_NAME = os.environ.get("DB_SERVICE_NAME", "freepdb1")

    dsn = f"{DB_HOST}:{DB_PORT}/{DB_SERVICE_NAME}"
    sql_script_path = os.path.join(os.path.dirname(__file__), 'create_tables.sql')

    with oracledb.connect(user=DB_USER, password=DB_PASSWORD, dsn=dsn) as connection:
        with connection.cursor() as cursor:
            with open(sql_script_path, 'r') as f:
                sql_script = f.read().strip().rstrip('/')
                cursor.execute(sql_script)

    print("All done, tables and indexes are created or replaced!")