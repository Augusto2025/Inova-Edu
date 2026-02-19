from config.banco import conectar

class TurmasModel:
    def buscar_por_curso(self, id_curso):
        conn = conectar()
        cursor = conn.cursor()
        query = "SELECT idTurma, Codigo_Turma, Turno, Ano FROM turma WHERE ID_Curso = %s"
        cursor.execute(query, (id_curso,))
        dados = cursor.fetchall()
        conn.close()
        return dados