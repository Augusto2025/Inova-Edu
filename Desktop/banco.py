import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()  

def conectar():
    return mysql.connector.connect(
        host=os.getenv("localhost"),
        user=os.getenv("root"),
        password=os.getenv(""),
        database=os.getenv("DB_NAME")
    )

# banco externo:
# return psycopg2.connect(os.getenv("DATABASE_URL"))
