from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField
from cloudinary.utils import cloudinary_url


# =========================
# USUÁRIO (perfil estendido)
# =========================
class Usuario(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    imagem = CloudinaryField('imagem_usuario', blank=True, null=True)
    tipo = models.CharField(max_length=20)
    descricao = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.user.username


# =========================
# CURSO
# =========================
class Curso(models.Model):
    nome_curso = models.CharField(max_length=45)
    imagem = CloudinaryField('imagem_curso', blank=True, null=True)
    descricao_curso = models.CharField(max_length=100, blank=True, null=True)
    data_inicio = models.DateField(blank=True, null=True)
    data_final = models.DateField(blank=True, null=True)
    criador = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.nome_curso


# =========================
# TURMA
# =========================
class Turma(models.Model):
    codigo_turma = models.CharField(max_length=11)
    turno = models.CharField(max_length=10, blank=True, null=True)
    ano = models.IntegerField()
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)

    def __str__(self):
        return self.codigo_turma


# =========================
# PROJETO
# =========================
class Projeto(models.Model):
    nome_projeto = models.CharField(max_length=30)
    data_de_criacao = models.DateField(auto_now_add=True)
    data_de_modificacao = models.DateField(auto_now=True)
    turma = models.ForeignKey(Turma, on_delete=models.CASCADE)

    def __str__(self):
        return self.nome_projeto


# =========================
# USUÁRIO NA TURMA
# =========================
class UsuarioDaTurma(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    turma = models.ForeignKey(Turma, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('usuario', 'turma')

    def __str__(self):
        return f'{self.usuario} - {self.turma}'


# =========================
# EVENTOS
# =========================
class Evento(models.Model):
    nome_do_evento = models.CharField(max_length=30)
    hora_do_evento = models.TimeField()
    data_do_evento = models.DateField()
    descricao = models.CharField(max_length=100)
    endereco = models.CharField(max_length=50)
    usuario = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.nome_do_evento


# =========================
# FÓRUM
# =========================
class Forum(models.Model):
    nome = models.CharField(max_length=30)
    data_criacao = models.DateField(auto_now_add=True)
    criador = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.nome


class Topico(models.Model):
    forum = models.ForeignKey(Forum, on_delete=models.CASCADE, related_name='topicos')
    titulo = models.CharField(max_length=100)
    descricao = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.titulo


class Mensagem(models.Model):
    forum = models.ForeignKey(Forum, on_delete=models.CASCADE, related_name='mensagens')
    autor = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    conteudo = models.TextField()
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.autor} - {self.conteudo[:30]}'


# =========================
# PASTAS E ARQUIVOS
# =========================
class Pasta(models.Model):
    nome = models.CharField(max_length=100)
    criada_por = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    criada_em = models.DateTimeField(auto_now_add=True)
    turma = models.ForeignKey(Turma, on_delete=models.CASCADE)
    pasta_pai = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='subpastas'
    )

    def __str__(self):
        return self.nome


class Arquivo(models.Model):
    nome = models.CharField(max_length=100)
    arquivo = CloudinaryField(resource_type='auto')
    enviado_por = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    enviado_em = models.DateTimeField(auto_now_add=True)
    turma = models.ForeignKey(Turma, on_delete=models.CASCADE)
    pasta = models.ForeignKey(Pasta, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.nome

    @property
    def download_url(self):
        url, _ = cloudinary_url(
            self.arquivo.public_id,
            resource_type='auto',
            attachment=self.nome
        )
        return url
