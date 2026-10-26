#!/usr/bin/env python3
"""
Script para gerar o executável do Inova Edu Desktop
Inclui o novo módulo de cache
"""

import subprocess
import sys
import os

def build_exe(with_console=False):
    """Gera o executável com PyInstaller"""

    # Argumentos base
    args = [
        "pyinstaller",
        "--noconfirm",
        "--onedir",
        "--name", "InovaEdu",
        "--add-data", "assets;assets",
        "--add-data", "views;views",
        "--add-data", "controllers;controllers",
        "--add-data", "sidebar_AP.py;.",
        "--add-data", "config;config",
        "--add-data", "models;models",
        "--add-data", "cache;cache",          # NOVO: módulo de cache
        "--add-data", ".env;.",
        "--collect-all", "psycopg2",
        "--hidden-import", "psycopg2",
        "--hidden-import", "requests",
        "--hidden-import", "cache",           # NOVO: import explícito do cache
        "--hidden-import", "cache.warmup",    # NOVO: import explícito do warmup
        "--icon=assets/img/LOGOBRANCO.ico",
        "main.py"
    ]

    # Adiciona --windowed se NÃO quiser terminal
    if not with_console:
        args.insert(3, "--windowed")  # After --noconfirm

    print(f"Executando: {' '.join(args)}")

    # Muda para o diretório Desktop
    desktop_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(desktop_dir)

    try:
        result = subprocess.run(args, check=True, capture_output=True, text=True)
        print("Build concluído com sucesso!")
        print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Erro no build: {e}")
        print(f"Stdout: {e.stdout}")
        print(f"Stderr: {e.stderr}")
        return False

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Build InovaEdu Desktop")
    parser.add_argument("--console", action="store_true", help="Build com terminal (console)")
    args = parser.parse_args()

    success = build_exe(with_console=args.console)
    sys.exit(0 if success else 1)