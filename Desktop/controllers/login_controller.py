from models.login_model import LoginUsuario
import traceback
from security.crypto import verify_password
from security.rate_limiter import login_limiter
from security.logger import get_logger

logger = get_logger(__name__)


def autenticar(user: str, senha: str, tipo: str = "") -> tuple:
    """
    Autentica usuário verificando hash da senha.

    Args:
        user: Email do usuário
        senha: Senha em texto plano fornecida pelo usuário
        tipo: Não utilizado (mantido para compatibilidade)

    Returns:
        (tipo_usuario, True) se sucesso
        (mensagem_erro, False) se falha
    """
    logger.info(f"Tentativa de login para: {user}")

    # Rate limiting por IP/email
    allowed, remaining, retry_after = login_limiter.check_rate_limit(user)
    if not allowed:
        msg = f"Muitas tentativas. Tente novamente em {retry_after} segundos."
        logger.warning(f"Rate limit excedido para: {user}")
        return (msg, False)

    try:
        print("[CONTROLLER] Buscando usuarios...")
        usuarios = LoginUsuario().exibir_usuarios()
        print(f"[CONTROLLER] {len(usuarios)} usuarios carregados")
    except Exception as e:
        logger.error(f"Erro ao acessar banco: {str(e)}")
        return (f"Erro ao acessar banco: {str(e)}", False)

    try:
        for email_user, senha_hash, tipo_user in usuarios:
            if user.lower() == email_user.lower():
                # Verifica hash da senha (PBKDF2-SHA256)
                if verify_password(senha, senha_hash):
                    # Login bem-sucedido - reseta rate limiter
                    login_limiter.reset(user)
                    logger.info(f"Login bem-sucedido: {user} ({tipo_user})")
                    return (tipo_user, True)
                else:
                    logger.warning(f"Senha incorreta para: {user}")
                    return ("Senha incorreta.", False)

        logger.warning(f"Email não encontrado: {user}")
        return ("Email não encontrado.", False)

    except Exception as e:
        logger.error(f"Erro na autenticação: {str(e)}")
        return (f"Erro: {str(e)}", False)