import mysql.connector
import os
from dotenv import load_dotenv
import threading

import socket

# Carregar .env da pasta config
config_path = os.path.join(os.path.dirname(__file__), '.env')
print(f"[BANCO] Procurando .env em: {config_path}")
load_dotenv(config_path)

# Configurar timeout global de socket
socket.setdefaulttimeout(3)

def conectar():
    """Conecta ao banco com timeout real de 3 segundos"""
    host = os.getenv("HOST")
    user = os.getenv("USER")
    password = os.getenv("PASSWORD")
    database = os.getenv("NAME")
    port = int(os.getenv("PORT"))

    # Teste rápido de socket TCP para falha imediata
    try:
        print(f"[BANCO] Testando socket {host}:{port}...", flush=True)
        sock = socket.create_connection((host, port), timeout=2)
        sock.close()
    except Exception as e:
        msg = f"Timeout/TCP error ao conectar em {host}:{port} - {e}"
        print(f"[BANCO ERRO] {msg}", flush=True)
        raise Exception(msg)

    # Verificacao via subprocess com timeout absoluto para evitar bloqueio do mysql-connector
    try:
        import sys
        import subprocess

        checker = (
            "import mysql.connector, json; cfg=%s; "
            "conn=mysql.connector.connect(**cfg); conn.close(); print('OK')"
            % (repr({
                'host': host,
                'user': user,
                'password': password,
                'database': database,
                'port': port,
                'connection_timeout': 3,
                'use_pure': True,
            }))
        )

        print(f"[BANCO] Rodando checagem subprocess (timeout=3s)...", flush=True)
        completed = subprocess.run([sys.executable, "-c", checker], capture_output=True, text=True, timeout=3)
        if completed.returncode != 0:
            out = completed.stdout + completed.stderr
            msg = f"Subprocess de checagem falhou: {out.strip()}"
            print(f"[BANCO ERRO] {msg}", flush=True)
            raise Exception(msg)
        print(f"[BANCO] Checagem subprocess OK", flush=True)
    except subprocess.TimeoutExpired:
        msg = f"Timeout absoluto: checagem do MySQL demorou mais de 3 segundos"
        print(f"[BANCO ERRO] {msg}", flush=True)
        raise Exception(msg)
    except Exception as e:
        # Propaga erro já logado
        raise

    # Se checagem ok, tenta conectar na mesma thread com parametros seguros
    try:
        db_config = {
            'host': host,
            'user': user,
            'password': password,
            'database': database,
            'port': port,
            'connection_timeout': 3,
            'use_pure': True,
        }
        print(f"[BANCO] Conectando a {host}:{port} via mysql-connector (final)...", flush=True)
        conn = mysql.connector.connect(**db_config)
        print(f"[BANCO] Conexao OK", flush=True)
        return conn
    except Exception as err:
        msg = f"Erro ao conectar com mysql-connector: {err}"
        print(f"[BANCO ERRO] {msg}", flush=True)
        raise