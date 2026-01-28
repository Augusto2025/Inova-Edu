import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()  

def conectar():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
    )

# banco externo:
# return psycopg2.connect(os.getenv("DATABASE_URL"))
