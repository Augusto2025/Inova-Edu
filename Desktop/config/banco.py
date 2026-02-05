import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

def conectar():
    return mysql.connector.connect(
        host=os.getenv("HOST"),
        user=os.getenv("USER"),
        password=os.getenv("PASSWORD"),
        database=os.getenv("NAME")
    )
    # banco externo:
    # return psycopg2.connect(os.getenv("DATABASE_URL"))

try:
    conexao = conectar()
    print("Conexão bem-sucedida ao banco de dados MySQL!")
except mysql.connector.Error as err:
    print(f"Erro ao conectar ao banco de dados: {err}")