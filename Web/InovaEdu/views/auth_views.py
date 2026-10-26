"""
Authentication views: login, CSRF failure.
Password reset views are commented out per user request.
"""
import os
import logging

from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods
from django.views.decorators.cache import never_cache
from django_ratelimit.decorators import ratelimit

from ..models import Usuario
from .utils import get_usuario_from_session

logger = logging.getLogger(__name__)


# =========================================================================
# LOGIN
# =========================================================================

@ratelimit(key='ip', rate='5/m', method='POST', block=True)
@never_cache
@require_http_methods(["GET", "POST"])
def login(request):
    """
    Handle user login with rate limiting and session fixation protection.
    """
    if request.method == "GET":
        # Se já logado, redireciona para home apropriada
        usuario = get_usuario_from_session(request)
        if usuario:
            if usuario.tipo == "Coordenador":
                return redirect("HomeCoord")
            return redirect("home")
        return render(request, "login.html", {"erro": "", "email": "", "senha": ""})

    # POST - processar login
    email = request.POST.get("email")
    senha = request.POST.get("senha")

    # Busca o usuário ignorando maiúsculas/minúsculas no e-mail
    usuario = Usuario.objects.filter(email__iexact=email).first()

    if usuario and usuario.check_password(senha):
        # Regenera a sessão para prevenir session fixation
        request.session.cycle_key()
        request.session["usuario_email"] = usuario.email
        request.session["usuario_id"] = usuario.idusuario
        request.session["usuario_tipo"] = usuario.tipo

        logger.info(f"Login successful: {usuario.email} ({usuario.tipo})")

        if usuario.tipo == "Coordenador":
            return redirect("HomeCoord")
        elif usuario.tipo in ("Aluno", "Professor"):
            return redirect("home")

    # Falha no login
    logger.warning(f"Login failed for email: {email} - IP: {request.META.get('REMOTE_ADDR')}")
    return render(
        request,
        "login.html",
        {"erro": "Usuário ou senha inválidos.", "email": email, "senha": ""},
    )


# =========================================================================
# CSRF FAILURE VIEW
# =========================================================================

def csrf_failure(request, reason=""):
    """
    View customizada para falha de CSRF.
    Loga a tentativa e retorna erro 403 amigável.
    """
    logger.warning(
        f"CSRF failure: {reason} - IP: {request.META.get('REMOTE_ADDR')} - Path: {request.path}"
    )
    return render(request, '403.html', {'reason': reason}, status=403)


# =========================================================================
# LOGOUT
# =========================================================================

@never_cache
@require_http_methods(["GET", "POST"])
def logout(request):
    """
    Realiza logout do usuário limpando a sessão e redireciona para login.
    """
    usuario_email = request.session.get('usuario_email')
    if usuario_email:
        logger.info(f"Logout: {usuario_email}")

    # Limpa toda a sessão
    request.session.flush()

    return redirect('login')


# =========================================================================
# PASSWORD RESET - COMMENTED OUT PER USER REQUEST
# =========================================================================
#
# from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
# from django.utils.encoding import force_bytes, force_str
# from django.contrib.auth.tokens import default_token_generator as token_generator
# from django.urls import reverse
# import resend
#
# @ratelimit(key='ip', rate='3/h', method='POST', block=True)
# @never_cache
# def pedir_email(request):
#     """Solicita e-mail para redefinição de senha."""
#     if request.method == "POST":
#         nome = request.POST.get("nome")
#         sobrenome = request.POST.get("sobrenome")
#         usuario = Usuario.objects.filter(nome=nome, sobrenome=sobrenome).first()
#
#         if usuario and usuario.email:
#             token = token_generator.make_token(usuario)
#             uid = urlsafe_base64_encode(force_bytes(usuario.idusuario))
#             link = request.build_absolute_uri(reverse('redefinir_senha', kwargs={'uidb64': uid, 'token': token}))
#
#             resend_api_key = os.environ.get('RESEND_API_KEY')
#             if resend_api_key:
#                 resend.api_key = resend_api_key
#                 resend.Emails.send({
#                     "from": "Inova Edu <onboarding@resend.dev>",
#                     "to": usuario.email,
#                     "subject": "Redefinição de Senha",
#                     "html": f"<p>Link: <a href='{link}'>{link}</a></p>"
#                 })
#             else:
#                 logger.warning(f"[DEV] Password reset link for {usuario.email}: {link}")
#
#             return render(request, "pedir_email.html", {"sucesso": True})
#
#     return render(request, "pedir_email.html")
#
#
# @ratelimit(key='ip', rate='5/h', method='POST', block=True)
# @never_cache
# def redefinir_senha(request, uidb64, token):
#     """Redefine a senha do usuário via token seguro."""
#     try:
#         uid = force_str(urlsafe_base64_decode(uidb64))
#         usuario = Usuario.objects.get(idusuario=uid)
#     except Exception:
#         usuario = None
#
#     if usuario and token_generator.check_token(usuario, token):
#         if request.method == 'POST':
#             nova = request.POST.get('nova_senha')
#             confirma = request.POST.get('confirmar_senha')
#
#             if nova == confirma:
#                 usuario.set_password(nova)
#                 usuario.save()
#                 return redirect('login')
#             else:
#                 return render(request, 'redefinir_senha.html', {'erro': 'Senhas não conferem'})
#
#         return render(request, 'redefinir_senha.html')
#     else:
#         return render(request, 'redefinir_senha.html', {'erro': 'Link inválido ou já utilizado.'})