# models/login_model.py
from config.banco import conectar
import traceback
from typing import List, Tuple, Optional
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from cache import cache, invalidate_on_write, CacheTags

class LoginUsuario:
    def exibir_usuarios(self) -> List[Tuple[str, str, str]]:
        """
        Retorna lista de usuários para autenticação.
        RETORNA: (email, senha_hash, tipo) - NUNCA a senha em texto plano
        Cache: 10 min (usuários mudam pouco)
        """
        cache_key = "login:exibir_usuarios"
        cached_value = cache.get(cache_key)
        if cached_value is not None:
            print("[MODEL LOGIN] Cache HIT - exibir_usuarios")
            return cached_value

        print("[MODEL LOGIN] Cache MISS - buscando do banco")
        conn = None
        try:
            print("[MODEL] Conectando ao PostgreSQL...")
            conn = conectar()
            cursor = conn.cursor()
            print("[MODEL] Executando query...")
            query = 'SELECT "Email", "Senha", "Tipo" FROM usuario'
            cursor.execute(query)
            usuarios = cursor.fetchall()
            cursor.close()
            print(f"[MODEL] {len(usuarios)} usuarios encontrados")

            # Cache por 10 minutos
            cache.set(cache_key, usuarios, ttl=600, tags=[CacheTags.USUARIO])
            return usuarios

        except Exception as e:
            print(f"[MODEL ERRO] Erro ao buscar usuários no Postgres: {str(e)}")
            print(f"[MODEL TRACEBACK] {traceback.format_exc()}")
            return []

        finally:
            if conn:
                try:
                    conn.close()
                    print("[MODEL] Conexão encerrada.")
                except:
                    pass

    def buscar_usuario_por_email(self, email: str) -> Optional[Tuple[str, str, str]]:
        """
        Busca um usuário específico por email.
        RETORNA: (email, senha_hash, tipo) ou None se não encontrado
        Cache: 5 min
        """
        cache_key = f"login:usuario:{email.lower()}"
        cached_value = cache.get(cache_key)
        if cached_value is not None:
            return cached_value

        conn = None
        try:
            conn = conectar()
            cursor = conn.cursor()
            query = 'SELECT "Email", "Senha", "Tipo" FROM usuario WHERE "Email" ILIKE %s'
            cursor.execute(query, (email,))
            usuario = cursor.fetchone()
            cursor.close()

            if usuario:
                cache.set(cache_key, usuario, ttl=300, tags=[CacheTags.USUARIO, CacheTags.usuario_especifico(0)])
            return usuario

        except Exception as e:
            print(f"[MODEL ERRO] Erro ao buscar usuário: {str(e)}")
            return None

        finally:
            if conn:
                try:
                    conn.close()
                except:
                    pass