import oracledb
import os
from dotenv import load_dotenv
load_dotenv()


DB_USER = os.environ.get("DB_USER")
DB_PASSWORD = os.environ.get("DB_PASSWORD")
DB_HOST = os.environ.get("DB_HOST")
DB_PORT = os.environ.get("DB_PORT")
DB_SERVICE_NAME = os.environ.get("DB_SERVICE_NAME")


if __name__ == "__main__":
    oracledb.init_oracle_client()  
    dsn = f"{DB_HOST}:{DB_PORT}/{DB_SERVICE_NAME}"
    sql_script_path = os.path.join(os.path.dirname(__file__), 'database_setup.sql')

    with oracledb.connect(user=DB_USER, password=DB_PASSWORD, dsn=dsn) as connection:
        with connection.cursor() as cursor:
            with open(sql_script_path, 'r') as f:
                sql_script = f.read().strip().rstrip('/')
                cursor.execute(sql_script)

    print("All done, tables and indexes are created or replaced!")