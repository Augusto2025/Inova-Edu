"""
Home page views.
"""
from django.shortcuts import render
from ..models import Curso


def homePage(request):
    """Public home page showing recent courses."""
    cursos = Curso.objects.all().order_by('-idcurso')[:6]
    return render(request, "homePage.html", {"cursos": cursos})