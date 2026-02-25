import psycopg2
from psycopg2 import OperationalError
import os
import sys
import socket
from urllib.parse import urlparse
from dotenv import load_dotenv

# Carregar .env da pasta config
config_path = os.path.join(os.path.dirname(__file__), '.env')
print(f"[BANCO] Procurando .env em: {config_path}")
load_dotenv(config_path)

def conectar():
    """Conecta ao PostgreSQL usando DATABASE_URL ou parâmetros individuais"""
    
    database_url = os.getenv("DATABASE_URL")

    if database_url:
        try:
            # 1. Teste rápido de socket antes de tentar a conexão pesada
            # Extraímos o host e porta da URL para testar se o banco externo responde
            result = urlparse(database_url)
            hostname = result.hostname
            port = result.port or 5432
            
            print(f"[BANCO] Testando socket externo {hostname}:{port}...", flush=True)
            socket.create_connection((hostname, port), timeout=3)
            
            # 2. Conexão real via URL
            print(f"[BANCO] Conectando via DATABASE_URL...", flush=True)
            conn = psycopg2.connect(database_url, connect_timeout=5)
            print(f"[BANCO] Conexão PostgreSQL Externa OK", flush=True)
            return conn

        except socket.timeout:
            msg = "Timeout: O servidor externo do banco não respondeu ao teste de socket."
            print(f"[BANCO ERRO] {msg}")
            raise Exception(msg)
        except OperationalError as err:
            msg = f"Erro operacional no PostgreSQL (URL): {err}"
            print(f"[BANCO ERRO] {msg}")
            raise Exception(msg)
        except Exception as err:
            msg = f"Falha na conexão externa: {err}"
            print(f"[BANCO ERRO] {msg}")
            raise Exception(msg)
    else:
        print("[BANCO ERRO] DATABASE_URL não encontrada no .env")
        raise Exception("Configuração de banco de dados ausente.")