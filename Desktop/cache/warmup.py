"""
Cache Warm-up - Pré-carrega dados comuns na inicialização
Chame cache_warmup() no main.py após login bem-sucedido
"""
import threading
from typing import Optional

# Import lazy para evitar dependência circular
def _get_models():
    from models.repositorio_model import RepositorioModel
    from models.eventos_model import Eventos
    from models.forum_model import ForumModel
    from models.projetos_model import ProjetoModel
    from models.turmas_models import TurmasModel
    from models.cursos_model import CursosModel
    from models.perfil_model import PerfilModel
    from models.sessao import UsuarioSessao
    return (
        RepositorioModel, Eventos, ForumModel,
        ProjetoModel, TurmasModel, CursosModel,
        PerfilModel, UsuarioSessao
    )


def cache_warmup(turma_id: Optional[int] = None, projeto_id: Optional[int] = None, usuario_id: Optional[int] = None):
    """
    Pré-carrega cache com dados mais acessados.
    Executa em thread separada para não bloquear UI.
    """
    def _warmup():
        try:
            (RepositorioModel, Eventos, ForumModel,
             ProjetoModel, TurmasModel, CursosModel,
             PerfilModel, UsuarioSessao) = _get_models()

            print("[CACHE WARMUP] Iniciando pré-carregamento...")

            # 1. Cursos (global, muda pouco)
            cursos = CursosModel()
            cursos.exibirCursos()
            print("[CACHE WARMUP] Cursos carregados")

            # 2. Eventos (global)
            eventos = Eventos()
            eventos.obter_todos_eventos()
            print("[CACHE WARMUP] Eventos carregados")

            # 3. Fóruns (global)
            forum = ForumModel()
            forum.obter_todos_foruns()
            print("[CACHE WARMUP] Fóruns carregados")

            # 4. Se tem turma, carrega turmas e projetos
            if turma_id:
                turmas = TurmasModel()
                # Precisa do id_curso - buscar via sessão ou outro meio
                # Por ora, carrega apenas se temos contexto
                pass

            # 5. Se tem projeto, carrega repositório
            if projeto_id:
                repo = RepositorioModel()
                repo.buscar_conteudo(projeto_id)
                print(f"[CACHE WARMUP] Repositório projeto {projeto_id} carregado")

            # 6. Perfil do usuário logado
            if usuario_id:
                sessao = UsuarioSessao()
                if sessao.email:
                    perfil = PerfilModel()
                    perfil.obter_dados_perfil(sessao.email)
                    print(f"[CACHE WARMUP] Perfil {sessao.email} carregado")

            print("[CACHE WARMUP] Concluído!")
        except Exception as e:
            print(f"[CACHE WARMUP ERRO] {e}")

    # Executa em background
    thread = threading.Thread(target=_warmup, daemon=True)
    thread.start()
    return thread


def cache_invalidate_on_navigation(tela: str):
    """
    Invalida cache seletivo ao navegar entre telas principais.
    Útil para forçar refresh ao voltar para uma tela que pode ter mudado.
    """
    from cache import cache, CacheTags

    tag_map = {
        "repositorio": CacheTags.REPOSITORIO,
        "eventos": CacheTags.EVENTO,
        "forum": CacheTags.FORUM,
        "projetos": CacheTags.PROJETO,
        "turmas": CacheTags.TURMA,
        "cursos": CacheTags.CURSO,
        "perfil": CacheTags.PERFIL,
    }

    tag = tag_map.get(tela.lower())
    if tag:
        count = cache.invalidate_tag(tag)
        print(f"[CACHE INVALIDATE] Tela '{tela}' - {count} entradas removidas")


def get_cache_stats():
    """Retorna estatísticas do cache para debug/monitoramento"""
    from cache import cache
    return cache.get_stats()


def clear_all_cache():
    """Limpa todo o cache (útil para logout ou reset)"""
    from cache import cache
    count = cache.clear()
    print(f"[CACHE CLEAR] {count} entradas removidas")
    return count