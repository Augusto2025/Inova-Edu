from config.banco import conectar

class ProjetoModel:
    def buscar_por_turma(self, id_turma):
        try:
            conn = conectar()
            cursor = conn.cursor()
            # Usando as colunas reais: idProjeto, Nome_projeto, Caminho_do_arquivo
            query = """SELECT idProjeto, Nome_projeto, Caminho_do_arquivo, Data_de_criacao 
                       FROM projeto 
                       WHERE ID_Turma = %s"""
            cursor.execute(query, (id_turma,))
            dados = cursor.fetchall()
            conn.close()
            return dados
        except Exception as e:
            print(f"Erro ao buscar projetos no banco: {e}")
            return []

    def deletar_projeto(self, id_projeto):
        try:
            conn = conectar()
            cursor = conn.cursor()
            query = "DELETE FROM projeto WHERE idProjeto = %s"
            cursor.execute(query, (id_projeto,))
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Erro ao deletar: {e}")
            return False
        
    def buscar_alunos_com_permissao(self, id_projeto, id_turma):
        # Seleciona todos os alunos da turma e faz um LEFT JOIN com a tabela de permissões
        # Se o ID do aluno estiver na tabela de permissões, 'tem_permissao' será 1, senão 0.
        sql = """
            SELECT u.id, u.nome, 
            CASE WHEN pae.usuario_id IS NOT NULL THEN 1 ELSE 0 END as tem_permissao
            FROM Usuario u
            INNER JOIN Usuario_Turma ut ON u.id = ut.usuario_id
            LEFT JOIN projeto_alunos_edicao pae ON u.id = pae.usuario_id AND pae.projeto_id = %s
            WHERE ut.turma_id = %s
        """
        # Execute a query usando seu cursor (ex: self.cursor.execute(sql, (id_projeto, id_turma)))
        # return self.cursor.fetchall()

    def sincronizar_alunos_edicao(self, id_projeto, lista_ids):
        try:
            # 1. Remove todas as permissões atuais deste projeto
            # 2. Insere apenas os IDs que vieram do checklist (lista_ids)
            # Use uma transação para garantir que não apague e falhe ao inserir
            self.cursor.execute("DELETE FROM projeto_alunos_edicao WHERE projeto_id = %s", (id_projeto,))
            for user_id in lista_ids:
                self.cursor.execute(
                    "INSERT INTO projeto_alunos_edicao (projeto_id, usuario_id) VALUES (%s, %s)",
                    (id_projeto, user_id)
                )
            self.db.commit()
            return True
        except Exception as e:
            print(f"Erro: {e}")
            return False
        
    def buscar_alunos_com_status_edicao(self, id_projeto, id_turma):
        try:
            conn = conectar()
            cursor = conn.cursor()
            # LEFT JOIN: Traz todos os alunos da turma. 
            # Se o aluno estiver na tabela de permissão, tem_permissao será 1.
            sql = """
                SELECT u.id_usuario, u.nome_usuario,
                CASE WHEN pae.usuario_id IS NOT NULL THEN 1 ELSE 0 END as tem_permissao
                FROM Usuario u
                INNER JOIN Usuario_Turma ut ON u.id_usuario = ut.id_usuario
                LEFT JOIN projeto_alunos_edicao pae ON u.id_usuario = pae.usuario_id 
                    AND pae.projeto_id = %s
                WHERE ut.id_turma = %s
            """
            cursor.execute(sql, (id_projeto, id_turma))
            dados = cursor.fetchall()
            conn.close()
            return dados
        except Exception as e:
            print(f"Erro ao buscar status de edição: {e}")
            return []

    def salvar_permissoes_projeto(self, id_projeto, lista_ids):
        conn = conectar()
        try:
            cursor = conn.cursor()
            # 1. Limpa as permissões antigas desse projeto (Lógica .set() do Django)
            cursor.execute("DELETE FROM projeto_alunos_edicao WHERE projeto_id = %s", (id_projeto,))
            
            # 2. Insere as novas marcadas no checklist
            for id_aluno in lista_ids:
                cursor.execute(
                    "INSERT INTO projeto_alunos_edicao (projeto_id, usuario_id) VALUES (%s, %s)", 
                    (id_projeto, id_aluno)
                )
            
            conn.commit()
            return True
        except Exception as e:
            conn.rollback()
            print(f"Erro ao salvar permissões: {e}")
            return False
        finally:
            conn.close()