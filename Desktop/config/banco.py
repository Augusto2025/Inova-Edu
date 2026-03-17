import psycopg2
from psycopg2 import OperationalError
import os
import sys
import socket
from urllib.parse import urlparse
from dotenv import load_dotenv

def resource_path(relative_path):
    """ Encontra o caminho do arquivo na mesma pasta do script ou no .exe """
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    
    # Pega a pasta onde o banco.py está (pasta config)
    base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, relative_path)

def conectar():
    env_path = resource_path(".env")
    
    # Carrega o arquivo
    if not load_dotenv(env_path):
        print(f"[BANCO ERRO] Não encontrou o .env em: {env_path}")
    
    database_url = os.getenv("DATABASE_URL")

    if database_url:
        try:
            # Remova espaços em branco extras que podem vir do .env
            database_url = database_url.strip()
            
            result = urlparse(database_url)
            hostname = result.hostname
            port = result.port or 5432
            
            print(f"[BANCO] Testando socket em {hostname}:{port}...", flush=True)
            socket.create_connection((hostname, port), timeout=4)
            
            conn = psycopg2.connect(database_url, connect_timeout=5)
            print(f"[BANCO] Conexão OK!", flush=True)
            return conn

        except Exception as err:
            print(f"[BANCO ERRO] Falha: {err}")
            raise
    else:
        print(f"[BANCO ERRO] DATABASE_URL não encontrada. Verifique o conteúdo de: {env_path}")
        raise Exception("Configuração ausente.")

conectar()