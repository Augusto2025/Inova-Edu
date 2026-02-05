from config.banco import conectar

class CursosModel:
    def exibirCursos(self):
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT Nome_curso, imagem_curso, Descricao_curso, Data_inicio, Data_final FROM curso")
        usuario = cursor.fetchall()
        conn.close()
        return usuario