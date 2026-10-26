# models/eventos_model.py
from config.banco import conectar
import traceback
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from cache import cache, cached, invalidate_on_write, CacheTags

class Eventos:
    # ===== LEITURA (COM CACHE) =====

    def obter_todos_eventos(self):
        """Retorna todos os eventos da tabela (cache 5 min)"""
        return self._obter_todos_eventos_cached()

    def _obter_todos_eventos_cached(self):
        cache_key = "eventos:obter_todos"
        cached_value = cache.get(cache_key)
        if cached_value is not None:
            print("[MODEL EVENTOS] Cache HIT - obtendo todos eventos")
            return cached_value

        print("[MODEL EVENTOS] Cache MISS - buscando do banco")
        conn = None
        try:
            conn = conectar()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT "idEventos", "Nome_do_evento", "Hora_do_evento",
                       "Data_do_evento", "Descricao", "Endereco", "ID_Usuario"
                FROM eventos
            """)
            eventos = cursor.fetchall()
            cursor.close()
            print(f"[MODEL EVENTOS] {len(eventos)} eventos encontrados")

            # Cacheia por 5 minutos
            cache.set(cache_key, eventos, ttl=300, tags=[CacheTags.EVENTO])
            return eventos
        except Exception as e:
            print(f"[MODEL EVENTOS ERRO] {str(e)}")
            print(f"[MODEL EVENTOS TRACEBACK] {traceback.format_exc()}")
            return []
        finally:
            if conn: conn.close()

    def obter_evento_por_id(self, id_evento):
        """Retorna um evento específico por ID (cache 5 min)"""
        cache_key = f"eventos:obter_por_id:{id_evento}"
        cached_value = cache.get(cache_key)
        if cached_value is not None:
            return cached_value

        conn = None
        try:
            print(f"[MODEL EVENTOS] Buscando evento ID {id_evento}...")
            conn = conectar()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT "idEventos", "Nome_do_evento", "Hora_do_evento",
                       "Data_do_evento", "Descricao", "Endereco", "ID_Usuario"
                FROM eventos
                WHERE "idEventos" = %s
            """, (id_evento,))
            evento = cursor.fetchone()
            cursor.close()

            if evento:
                cache.set(cache_key, evento, ttl=300, tags=[CacheTags.EVENTO])
            return evento
        except Exception as e:
            print(f"[MODEL EVENTOS ERRO] {str(e)}")
            return None
        finally:
            if conn: conn.close()

    def obter_eventos_por_usuario(self, id_usuario):
        """Retorna eventos de um usuário específico (cache 5 min)"""
        cache_key = f"eventos:por_usuario:{id_usuario}"
        cached_value = cache.get(cache_key)
        if cached_value is not None:
            return cached_value

        conn = None
        try:
            print(f"[MODEL EVENTOS] Buscando eventos do usuário ID {id_usuario}...")
            conn = conectar()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT "idEventos", "Nome_do_evento", "Hora_do_evento",
                       "Data_do_evento", "Descricao", "Endereco", "ID_Usuario"
                FROM eventos
                WHERE "ID_Usuario" = %s
            """, (id_usuario,))
            eventos = cursor.fetchall()
            cursor.close()

            cache.set(cache_key, eventos, ttl=300, tags=[CacheTags.EVENTO, CacheTags.usuario_especifico(id_usuario)])
            return eventos
        except Exception as e:
            print(f"[MODEL EVENTOS ERRO] {str(e)}")
            return []
        finally:
            if conn: conn.close()

    # ===== ESCRITA (INVALIDA CACHE) =====

    @invalidate_on_write(tags=[CacheTags.EVENTO])
    def criar_evento(self, nome, hora, data, descricao, endereco, id_usuario):
        """Cria um novo evento e invalida cache"""
        conn = None
        try:
            print(f"[MODEL EVENTOS] Criando novo evento: {nome}")
            conn = conectar()
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO eventos
                ("Nome_do_evento", "Hora_do_evento", "Data_do_evento", "Descricao", "Endereco", "ID_Usuario")
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (nome, hora, data, descricao, endereco, id_usuario))
            conn.commit()
            cursor.close()
            return True
        except Exception as e:
            if conn: conn.rollback()
            print(f"[MODEL EVENTOS ERRO] {str(e)}")
            return False
        finally:
            if conn: conn.close()

    @invalidate_on_write(tags=[CacheTags.EVENTO])
    def editar_evento(self, id_evento, nome, hora, data, descricao, endereco):
        """Atualiza os dados de um evento existente e invalida cache"""
        conn = None
        try:
            print(f"[MODEL EVENTOS] Editando evento ID {id_evento}...")
            conn = conectar()
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE eventos
                SET "Nome_do_evento" = %s, "Hora_do_evento" = %s, "Data_do_evento" = %s,
                    "Descricao" = %s, "Endereco" = %s
                WHERE "idEventos" = %s
            """, (nome, hora, data, descricao, endereco, id_evento))
            conn.commit()
            cursor.close()
            return True
        except Exception as e:
            if conn: conn.rollback()
            print(f"[MODEL EVENTOS ERRO EDITAR] {str(e)}")
            return False
        finally:
            if conn: conn.close()

    @invalidate_on_write(tags=[CacheTags.EVENTO])
    def deletar_evento(self, id_evento):
        """Deleta um evento e invalida cache"""
        conn = None
        try:
            print(f"[MODEL EVENTOS] Deletando evento ID {id_evento}...")
            conn = conectar()
            cursor = conn.cursor()
            cursor.execute('DELETE FROM eventos WHERE "idEventos" = %s', (id_evento,))
            conn.commit()
            cursor.close()
            return True
        except Exception as e:
            if conn: conn.rollback()
            print(f"[MODEL EVENTOS ERRO] {str(e)}")
            return False
        finally:
            if conn: conn.close()