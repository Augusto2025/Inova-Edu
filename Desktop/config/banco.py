import mysql.connector
import os
import sys
import socket
from dotenv import load_dotenv

def resource_path(relative_path):
    """ Encontra o caminho real dos arquivos dentro do .exe ou em dev """
    try:
        # Caminho da pasta temporária onde o PyInstaller extrai tudo
        base_path = sys._MEIPASS
    except Exception:
        # Caminho em modo de desenvolvimento (VS Code)
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# --- CARREGAMENTO DO .ENV ---
# Como este arquivo está em 'config/banco.py', buscamos o .env na pasta 'config' 
# que será incluída no executável através do comando --add-data
config_path = resource_path(os.path.join('config', '.env'))

print(f"[BANCO] Procurando .env em: {config_path}")

if os.path.exists(config_path):
    load_dotenv(config_path)
    print("[BANCO] .env carregado com sucesso.")
else:
    # Caso não encontre na config interna, tenta na pasta atual (ao lado do .exe)
    fallback_path = os.path.join(os.path.dirname(sys.executable), "config", ".env")
    load_dotenv(fallback_path)
    print(f"[BANCO] Tentando fallback em: {fallback_path}")

# Configurar timeout global de socket
socket.setdefaulttimeout(3)

def conectar():
    """Conecta ao banco com tratamento de erro e carregamento de variáveis"""
    
    # IMPORTANTE: No .env, mude 'localhost' para '127.0.0.1' para evitar bloqueios do Windows
    host = os.getenv("HOST", "127.0.0.1")
    user = os.getenv("USER", "root")
    password = os.getenv("PASSWORD", "182105")
    database = os.getenv("NAME", "db_repositorio")
    
    try:
        port = int(os.getenv("PORT", "3306"))
    except:
        port = 3306

    # 1. Teste rápido de socket TCP (falha rápida se o MySQL estiver desligado)
    try:
        print(f"[BANCO] Testando socket {host}:{port}...", flush=True)
        sock = socket.create_connection((host, port), timeout=2)
        sock.close()
    except Exception as e:
        msg = f"Servidor MySQL inacessível em {host}:{port}. Verifique se o banco está ligado."
        print(f"[BANCO ERRO] {msg}")
        raise Exception(msg)

    # 2. Conexão via mysql-connector
    try:
        db_config = {
            'host': host,
            'user': user,
            'password': password,
            'database': database,
            'port': port,
            'connection_timeout': 3,
            'use_pure': True, # Melhora a compatibilidade no PyInstaller
            'auth_plugin': 'mysql_native_password',
        }
        print(f"[BANCO] Conectando a {host}:{port} via mysql-connector...", flush=True)
        conn = mysql.connector.connect(**db_config)
        print(f"[BANCO] Conexão OK", flush=True)
        return conn
    except Exception as err:
        msg = f"Erro de credenciais ou banco inexistente: {err}"
        print(f"[BANCO ERRO] {msg}", flush=True)
        raise Exception(msg)