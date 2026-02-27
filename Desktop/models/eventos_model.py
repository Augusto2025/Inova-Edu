# models/eventos_model.py
from config.banco import conectar
import traceback

class Eventos:
    def obter_todos_eventos(self):
        """Retorna todos os eventos da tabela"""
        conn = None
        try:
            print("[MODEL EVENTOS] Buscando todos os eventos...")
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
            return eventos
        except Exception as e:
            print(f"[MODEL EVENTOS ERRO] {str(e)}")
            print(f"[MODEL EVENTOS TRACEBACK] {traceback.format_exc()}")
            return []
        finally:
            if conn: conn.close()

    def obter_evento_por_id(self, id_evento):
        """Retorna um evento específico por ID"""
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
            return evento
        except Exception as e:
            print(f"[MODEL EVENTOS ERRO] {str(e)}")
            return None
        finally:
            if conn: conn.close()

    def obter_eventos_por_usuario(self, id_usuario):
        """Retorna eventos de um usuário específico"""
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
            return eventos
        except Exception as e:
            print(f"[MODEL EVENTOS ERRO] {str(e)}")
            return []
        finally:
            if conn: conn.close()

    def criar_evento(self, nome, hora, data, descricao, endereco, id_usuario):
        """Cria um novo evento"""
        conn = None
        try:
            print(f"[MODEL EVENTOS] Criando novo evento: {nome}")
            conn = conectar()
            cursor = conn.cursor()
            # No INSERT, as colunas também precisam de aspas duplas
            cursor.execute("""
                INSERT INTO eventos 
                ("Nome_do_evento", "Hora_do_evento", "Data_do_evento", "Descricao", "Endereco", "ID_Usuario")
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (nome, hora, data, descricao, endereco, id_usuario))
            conn.commit()
            cursor.close()
            return True
        except Exception as e:
            if conn: conn.rollback() # Reverte em caso de erro no insert
            print(f"[MODEL EVENTOS ERRO] {str(e)}")
            return False
        finally:
            if conn: conn.close()

    def deletar_evento(self, id_evento):
        """Deleta um evento"""
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