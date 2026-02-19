from models.cursos_model import CursosModel

def obter_cursos():
    cursos_brutos = CursosModel().exibirCursos()
    lista_formatada = []
    
    for linha in cursos_brutos:
        lista_formatada.append({
            "id": linha[0],        
            "name": str(linha[1]), # Garante que o nome seja string
            "image": linha[2],
            "description": linha[3]
        })
    
    return lista_formatada