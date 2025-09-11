# essa página serve para distribuir por todo o template essas funções
from .models import *
from .views import *

def usuario(request):
    email = request.session.get('usuario_email')  # pega o email salvo no login
    usuario = None
    if email:
        usuario = Usuario.objects.filter(email__iexact=email).first()
    return {'usuario': usuario}