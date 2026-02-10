#!/usr/bin/env python3
"""Script para diagnosticar problemas de conexão com MySQL"""
import socket
import sys
from pathlib import Path

# Adicionar Desktop ao path
sys.path.insert(0, str(Path(__file__).parent))

def testar_porta(host, porta):
    """Testa se a porta está aberta"""
    print(f"[TESTE] Verificando se {host}:{porta} está acessível...")
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(2)
        resultado = sock.connect_ex((host, porta))
        sock.close()
        
        if resultado == 0:
            print(f"[OK] Porta {porta} está ABERTA - MySQL pode estar rodando")
            return True
        else:
            print(f"[ERRO] Porta {porta} está FECHADA - MySQL provavelmente nao esta rodando")
            return False
    except Exception as e:
        print(f"[ERRO] Erro ao testar porta: {e}")
        return False

def testar_env():
    """Testa se .env está configurado corretamente"""
    print("\n[TESTE] Verificando arquivo .env...")
    env_path = Path(__file__).parent / "config" / ".env"
    
    if not env_path.exists():
        print(f"[ERRO] Arquivo nao encontrado: {env_path}")
        return False
    
    print(f"[OK] Arquivo encontrado: {env_path}")
    
    try:
        with open(env_path, 'r') as f:
            content = f.read()
            if "HOST" in content:
                print("[OK] .env contém HOST")
            else:
                print("[AVISO] .env nao contem HOST")
    except Exception as e:
        print(f"[ERRO] Nao consegui ler .env: {e}")
        return False
    
    return True

def main():
    print("=" * 60)
    print("DIAGNOSTICO DE CONEXAO COM MYSQL")
    print("=" * 60)
    
    # Teste 1: Verificar .env
    if not testar_env():
        return
    
    # Teste 2: Verificar porta
    testar_porta("localhost", 3306)
    
    # Teste 3: Tentar conectar
    print("\n[TESTE] Tentando conexao com mysql-connector...")
    try:
        import mysql.connector
        print("[OK] mysql-connector-python esta instalado")
        
        from config.banco import conectar
        print("[TESTE] Tentando conectar...")
        conn = conectar()
        print("[OK] CONEXAO BEM-SUCEDIDA!")
        conn.close()
        
    except TimeoutError:
        print("[ERRO] Timeout - MySQL nao respondeu a tempo")
    except Exception as e:
        print(f"[ERRO] {e}")

if __name__ == "__main__":
    main()
