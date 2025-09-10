# essa página serve para distribuir por todo o template essas funções
from .models import *

def usuario_tipo(request):
    email = request.GET.get('email')  # ou request.POST.get('email')
    usuario = None
    if email:
        usuario = Usuario.objects.filter(email=email).first()
    return {'usuario': usuario}