"""
Certificate views.
Require authentication.
"""
import json
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.contrib import messages

from ..models import Usuario, Certificado
from .utils import get_usuario_from_session, require_login


@require_http_methods(["POST", "DELETE"])
@require_login
def salvar_certificado(request):
    """
    API endpoint para criar, editar ou excluir certificados.
    """
    usuario = request.usuario

    try:
        if request.method == "POST":
            data = json.loads(request.body)

            cert_id = data.get("id")
            nome = data.get("nome", "").strip()
            descricao = data.get("descricao", "").strip()
            data_inicio = data.get("data_inicio") or None
            data_final = data.get("data_final") or None

            if not nome:
                msg = "O nome do certificado é obrigatório."
                messages.warning(request, msg)
                return JsonResponse({"message": msg}, status=400)

            # EDITAR
            if cert_id:
                try:
                    certificado = Certificado.objects.get(
                        idcertificado=cert_id,
                        usuario=usuario
                    )

                    certificado.nome = nome
                    certificado.descricao = descricao
                    certificado.data_inicio = data_inicio
                    certificado.data_final = data_final
                    certificado.save()

                    msg = "Certificado atualizado com sucesso!"
                    messages.success(request, msg)
                    return JsonResponse({"message": msg}, status=200)

                except Certificado.DoesNotExist:
                    msg = "Certificado não encontrado."
                    messages.error(request, msg)
                    return JsonResponse({"message": msg}, status=404)

            # CRIAR
            else:
                Certificado.objects.create(
                    nome=nome,
                    descricao=descricao,
                    data_inicio=data_inicio,
                    data_final=data_final,
                    usuario=usuario
                )

                msg = "Certificado criado com sucesso!"
                messages.success(request, msg)
                return JsonResponse({"message": msg}, status=200)

        # EXCLUIR
        if request.method == "DELETE":
            data = json.loads(request.body)
            cert_id = data.get("id")

            try:
                certificado = Certificado.objects.get(
                    idcertificado=cert_id,
                    usuario=usuario
                )

                certificado.delete()

                msg = "Certificado excluído com sucesso!"
                messages.success(request, msg)
                return JsonResponse({"message": msg}, status=200)

            except Certificado.DoesNotExist:
                msg = "Certificado não encontrado."
                messages.error(request, msg)
                return JsonResponse({"message": msg}, status=404)

        msg = "Método HTTP não permitido."
        messages.error(request, msg)
        return JsonResponse({"message": msg}, status=405)

    except Exception as e:
        msg = f"Erro no processamento do certificado: {str(e)}"
        messages.error(request, msg)
        return JsonResponse({"message": msg}, status=500)