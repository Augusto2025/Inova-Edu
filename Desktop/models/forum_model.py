from config.banco import conectar
import traceback
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from cache import cache, invalidate_on_write, CacheTags

class ForumModel:
    # ===== LEITURA (COM CACHE) =====

    def obter_usuario_por_email(self, email):
        """Busca o idUsuario e o Nome do usuário baseado no e-mail (cache 10 min)"""
        cache_key = f"forum:usuario_por_email:{email}"
        cached_value = cache.get(cache_key)
        if cached_value is not None:
            return cached_value

        conn = None
        try:
            conn = conectar()
            cursor = conn.cursor()

            cursor.execute("""
                SELECT "idUsuario", "Nome"
                FROM usuario
                WHERE "Email" = %s;
            """, (email,))

            usuario = cursor.fetchone()
            cursor.close()

            if usuario:
                # Cache por 10 minutos - usuário muda pouco
                cache.set(cache_key, usuario, ttl=600, tags=[CacheTags.USUARIO, CacheTags.FORUM])
            return usuario
        except Exception as e:
            print(f"[MODEL USUARIO ERRO] {str(e)}")
            return None
        finally:
            if conn: conn.close()

    def obter_todos_foruns(self):
        """Retorna todos os fóruns (cache 5 min)"""
        cache_key = "forum:obter_todos"
        cached_value = cache.get(cache_key)
        if cached_value is not None:
            return cached_value

        conn = None
        try:
            conn = conectar()
            cursor = conn.cursor()
            cursor.execute('SELECT idforum, nome, data_criacao, usuario_id FROM forum ORDER BY nome;')
            foruns = cursor.fetchall()
            cursor.close()

            cache.set(cache_key, foruns, ttl=300, tags=[CacheTags.FORUM])
            return foruns
        except Exception as e:
            print(f"[MODEL FORUM ERRO] {str(e)}")
            return []
        finally:
            if conn: conn.close()

    def obter_topicos_por_forum(self, id_forum):
        """Retorna tópicos de um fórum (cache 2 min - muda mais frequentemente)"""
        cache_key = f"forum:topicos:{id_forum}"
        cached_value = cache.get(cache_key)
        if cached_value is not None:
            return cached_value

        conn = None
        try:
            conn = conectar()
            cursor = conn.cursor()
            cursor.execute(
                'SELECT idtopico, forum_id, titulo, descricao, usuario_id FROM topico WHERE forum_id = %s;',
                (id_forum,)
            )
            topicos = cursor.fetchall()
            cursor.close()

            cache.set(cache_key, topicos, ttl=120, tags=[CacheTags.FORUM, CacheTags.projeto_especifico(id_forum)])
            return topicos
        except Exception as e:
            print(f"[MODEL TOPICO ERRO] {str(e)}")
            return []
        finally:
            if conn: conn.close()

    def obter_mensagens_por_topico(self, id_topico):
        """Retorna mensagens de um tópico (cache 1 min - tempo real)"""
        cache_key = f"forum:mensagens:{id_topico}"
        cached_value = cache.get(cache_key)
        if cached_value is not None:
            return cached_value

        conn = None
        try:
            conn = conectar()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT m.id, m."Conteudo", m."Data_criacao", u."Nome"
                FROM mensagem m
                JOIN usuario u ON m."ID_Usuario" = u."idUsuario"
                WHERE m."ID_Topico" = %s AND m.excluida = FALSE
                ORDER BY m."Data_criacao" ASC;
            """, (id_topico,))
            mensagens = cursor.fetchall()
            cursor.close()

            # Cache curto para mensagens (1 min)
            cache.set(cache_key, mensagens, ttl=60, tags=[CacheTags.FORUM])
            return mensagens
        except Exception as e:
            print(f"[MODEL MENSAGEM ERRO] {str(e)}")
            return []
        finally:
            if conn: conn.close()

    # ===== ESCRITA (INVALIDA CACHE) =====

    @invalidate_on_write(tags=[CacheTags.FORUM])
    def criar_forum(self, nome, id_usuario):
        conn = None
        try:
            conn = conectar()
            cursor = conn.cursor()
            cursor.execute(
                'INSERT INTO forum (nome, data_criacao, usuario_id) VALUES (%s, CURRENT_DATE, %s) RETURNING idforum;',
                (nome, id_usuario)
            )
            id_forum = cursor.fetchone()[0]
            conn.commit()
            cursor.close()
            return id_forum
        except Exception as e:
            if conn: conn.rollback()
            print(f"[MODEL FORUM ERRO] {str(e)}")
            return None
        finally:
            if conn: conn.close()

    @invalidate_on_write(tags=[CacheTags.FORUM])
    def editar_forum(self, id_forum, novo_nome):
        conn = None
        try:
            conn = conectar()
            cursor = conn.cursor()
            cursor.execute('UPDATE forum SET nome = %s WHERE idforum = %s;', (novo_nome, id_forum))
            conn.commit()
            cursor.close()
            return True
        except Exception as e:
            if conn: conn.rollback()
            print(f"[MODEL FORUM ERRO EDITAR] {str(e)}")
            return False
        finally:
            if conn: conn.close()

    @invalidate_on_write(tags=[CacheTags.FORUM])
    def excluir_forum(self, id_forum):
        conn = None
        try:
            conn = conectar()
            cursor = conn.cursor()
            cursor.execute('DELETE FROM mensagem WHERE "ID_Topico" IN (SELECT idtopico FROM topico WHERE forum_id = %s);', (id_forum,))
            cursor.execute('DELETE FROM topico WHERE forum_id = %s;', (id_forum,))
            cursor.execute('DELETE FROM forum WHERE idforum = %s;', (id_forum,))
            conn.commit()
            cursor.close()
            return True
        except Exception as e:
            if conn: conn.rollback()
            print(f"[MODEL FORUM ERRO EXCLUIR] {str(e)}")
            return False
        finally:
            if conn: conn.close()

    @invalidate_on_write(tags=[CacheTags.FORUM])
    def criar_topico(self, id_forum, titulo, descricao, id_usuario):
        conn = None
        try:
            conn = conectar()
            cursor = conn.cursor()
            cursor.execute(
                'INSERT INTO topico (forum_id, titulo, descricao, usuario_id) VALUES (%s, %s, %s, %s) RETURNING idtopico;',
                (id_forum, titulo, descricao, id_usuario)
            )
            id_topico = cursor.fetchone()[0]
            conn.commit()
            cursor.close()
            return id_topico
        except Exception as e:
            if conn: conn.rollback()
            print(f"[MODEL TOPICO ERRO] {str(e)}")
            return None
        finally:
            if conn: conn.close()

    @invalidate_on_write(tags=[CacheTags.FORUM])
    def editar_topico(self, id_topico, novo_titulo):
        conn = None
        try:
            conn = conectar()
            cursor = conn.cursor()
            cursor.execute('UPDATE topico SET titulo = %s WHERE idtopico = %s;', (novo_titulo, id_topico))
            conn.commit()
            cursor.close()
            return True
        except Exception as e:
            if conn: conn.rollback()
            print(f"[MODEL TOPICO ERRO EDITAR] {str(e)}")
            return False
        finally:
            if conn: conn.close()

    @invalidate_on_write(tags=[CacheTags.FORUM])
    def excluir_topico(self, id_topico):
        conn = None
        try:
            conn = conectar()
            cursor = conn.cursor()
            cursor.execute('DELETE FROM mensagem WHERE "ID_Topico" = %s;', (id_topico,))
            cursor.execute('DELETE FROM topico WHERE idtopico = %s;', (id_topico,))
            conn.commit()
            cursor.close()
            return True
        except Exception as e:
            if conn: conn.rollback()
            print(f"[MODEL TOPICO ERRO EXCLUIR] {str(e)}")
            return False
        finally:
            if conn: conn.close()

    @invalidate_on_write(tags=[CacheTags.FORUM])
    def criar_mensagem(self, id_topico, id_usuario, conteudo):
        conn = None
        try:
            conn = conectar()
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO mensagem ("ID_Topico", "ID_Usuario", "Conteudo", "Data_criacao", excluida)
                VALUES (%s, %s, %s, NOW(), FALSE);
            """, (id_topico, id_usuario, conteudo))
            conn.commit()
            cursor.close()
            # Invalida mensagens deste tópico especificamente
            cache.invalidate_keys([f"forum:mensagens:{id_topico}"])
            return True
        except Exception as e:
            if conn: conn.rollback()
            print(f"[MODEL MENSAGEM ERRO] {str(e)}")
            return False
        finally:
            if conn: conn.close()

    @invalidate_on_write(tags=[CacheTags.FORUM])
    def editar_mensagem(self, id_mensagem, novo_conteudo):
        conn = None
        try:
            conn = conectar()
            cursor = conn.cursor()
            cursor.execute('UPDATE mensagem SET "Conteudo" = %s WHERE id = %s;', (novo_conteudo, id_mensagem))
            conn.commit()
            cursor.close()
            return True
        except Exception as e:
            if conn: conn.rollback()
            print(f"[MODEL MENSAGEM ERRO EDITAR] {str(e)}")
            return False
        finally:
            if conn: conn.close()

    @invalidate_on_write(tags=[CacheTags.FORUM])
    def excluir_mensagem(self, id_mensagem):
        conn = None
        try:
            conn = conectar()
            cursor = conn.cursor()
            cursor.execute('UPDATE mensagem SET excluida = TRUE WHERE id = %s;', (id_mensagem,))
            conn.commit()
            cursor.close()
            return True
        except Exception as e:
            if conn: conn.rollback()
            print(f"[MODEL MENSAGEM ERRO EXCLUIR] {str(e)}")
            return False
        finally:
            if conn: conn.close()