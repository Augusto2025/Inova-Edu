from models.cursos_model import CursosModel

def obter_cursos():
    cursos = CursosModel().exibirCursos()
    for nome_curso, imagem_curso, descricao_curso, data_inicio, data_final in cursos:
        quantidade = len(cursos)
        return nome_curso, imagem_curso, descricao_curso, data_inicio, data_final, quantidade