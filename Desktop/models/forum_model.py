from config.banco import conectar
import traceback

class ForumModel:
    # --- OPERAÇÕES DE SESSÃO / USUÁRIO ---
    def obter_usuario_por_email(self, email):
        """Busca o idUsuario e o Nome do usuário baseado no e-mail salvo na sessão"""
        conn = None
        try:
            conn = conectar()
            cursor = conn.cursor()
            
            # NOTA: Ajuste "Email" caso no seu pgAdmin a coluna use outra grafia (ex: email tudo minúsculo)
            cursor.execute("""
                SELECT "idUsuario", "Nome" 
                FROM usuario 
                WHERE "Email" = %s;
            """, (email,))
            
            usuario = cursor.fetchone()
            cursor.close()
            return usuario  # Retorna a tupla (id, Nome) ou None se não encontrar
        except Exception as e:
            print(f"[MODEL USUARIO ERRO] {str(e)}")
            return None
        finally:
            if conn: conn.close()

    # --- OPERAÇÕES DE FÓRUM ---
    def obter_todos_foruns(self):
        conn = None
        try:
            conn = conectar()
            cursor = conn.cursor()
            cursor.execute('SELECT idforum, nome, data_criacao, usuario_id FROM forum ORDER BY nome;')
            foruns = cursor.fetchall()
            cursor.close()
            return foruns
        except Exception as e:
            print(f"[MODEL FORUM ERRO] {str(e)}")
            return []
        finally:
            if conn: conn.close()

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

    # --- OPERAÇÕES DE TÓPICO ---
    def obter_topicos_por_forum(self, id_forum):
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
            return topicos
        except Exception as e:
            print(f"[MODEL TOPICO ERRO] {str(e)}")
            return []
        finally:
            if conn: conn.close()

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

    # --- OPERAÇÕES DE MENSAGEM ---
    def obter_mensagens_por_topico(self, id_topico):
        conn = None
        try:
            conn = conectar()
            cursor = conn.cursor()
            # Mantendo u."Nome", m."Conteudo", m."Data_criacao", m."ID_Usuario" e m."ID_Topico" validados anteriormente
            cursor.execute("""
                SELECT m.id, m."Conteudo", m."Data_criacao", u."Nome" 
                FROM mensagem m
                JOIN usuario u ON m."ID_Usuario" = u."idUsuario"
                WHERE m."ID_Topico" = %s AND m.excluida = FALSE
                ORDER BY m."Data_criacao" ASC;
            """, (id_topico,))
            mensagens = cursor.fetchall()
            cursor.close()
            return mensagens
        except Exception as e:
            print(f"[MODEL MENSAGEM ERRO] {str(e)}")
            return []
        finally:
            if conn: conn.close()

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
            return True
        except Exception as e:
            if conn: conn.rollback()
            print(f"[MODEL MENSAGEM ERRO] {str(e)}")
            return False
        finally:
            if conn: conn.close()