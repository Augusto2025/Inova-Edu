from config.banco import conectar

class RepositorioModel:
    def buscar_conteudo(self, turma_id, pasta_pai_id=None):
        try:
            conn = conectar()
            cursor = conn.cursor(dictionary=True)

            # 1. Buscar Pastas
            # Note: Tabela 'usuario' (minúsculo), Colunas 'idUsuario' e 'Nome' (conforme seu print)
            query_pastas = """
                SELECT p.id, p.nome, IFNULL(u.Nome, 'Sistema') as autor, p.criada_em as data
                FROM pasta p
                LEFT JOIN usuario u ON p.criada_por_id = u.idUsuario
                WHERE p.turma_id = %s AND p.pasta_pai_id <=> %s
            """
            cursor.execute(query_pastas, (turma_id, pasta_pai_id))
            pastas = cursor.fetchall()

            # 2. Buscar Arquivos
            query_arquivos = """
                SELECT a.id, a.nome, IFNULL(u.Nome, 'Sistema') as autor, a.enviado_em as data
                FROM arquivo a
                LEFT JOIN usuario u ON a.enviado_por_id = u.idUsuario
                WHERE a.turma_id = %s AND a.pasta_id <=> %s
            """
            cursor.execute(query_arquivos, (turma_id, pasta_pai_id))
            arquivos = cursor.fetchall()

            conn.close()
            return pastas, arquivos
        except Exception as e:
            print(f"Erro no RepositorioModel: {e}")
            return [], []