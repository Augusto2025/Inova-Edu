from django.db import models
from cloudinary.models import CloudinaryField
from cloudinary.utils import cloudinary_url
from django.contrib.auth.models import User

# =========================
# AUTENTICAÇÃO (não gerenciados)
# =========================
class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'AuthGroup'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group_id = models.IntegerField()
    permission_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'AuthGroupPermissions'
        unique_together = (('group_id', 'permission_id'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type_id = models.IntegerField()
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'AuthPermission'
        unique_together = (('content_type_id', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'AuthUser'


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user_id = models.IntegerField()
    group_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'AuthUserGroups'
        unique_together = (('user_id', 'group_id'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user_id = models.IntegerField()
    permission_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'AuthUserUserPermissions'
        unique_together = (('user_id', 'permission_id'),)


# =========================
# USUÁRIO
# =========================
class Usuario(models.Model):
    imagem = CloudinaryField('imagem_usuario', blank=True, null=True)
    tipo = models.CharField(max_length=20)
    nome = models.CharField(max_length=20)
    sobrenome = models.CharField(max_length=20)
    email = models.CharField(max_length=45)
    senha = models.CharField(max_length=30)
    descricao = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        db_table = 'Usuario'

    def __str__(self):
        return self.nome


# =========================
# CURSO
# =========================
class Curso(models.Model):
    nome_curso = models.CharField(max_length=45)
    imagem = CloudinaryField('imagem_curso', blank=True, null=True)
    descricao_curso = models.CharField(max_length=100, blank=True, null=True)
    data_inicio = models.DateField(blank=True, null=True)
    data_final = models.DateField(blank=True, null=True)
    usuario = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        db_table = 'Curso'

    def __str__(self):
        return self.nome_curso


# =========================
# TURMA
# =========================
class Turma(models.Model):
    codigo_turma = models.CharField(max_length=11)
    turno = models.CharField(max_length=5, blank=True, null=True)
    ano = models.IntegerField()
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)

    class Meta:
        db_table = 'Turma'

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

    class Meta:
        db_table = 'Projeto'

    def __str__(self):
        return self.nome_projeto


# =========================
# USUÁRIO NA TURMA
# =========================
class UsuarioDaTurma(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    turma = models.ForeignKey(Turma, on_delete=models.CASCADE)

    class Meta:
        db_table = 'UsuarioDaTurma'
        unique_together = ('usuario', 'turma')

    def __str__(self):
        return f'{self.usuario} - {self.turma}'


# =========================
# EVENTOS
# =========================
class Eventos(models.Model):
    nome_do_evento = models.CharField(max_length=30)
    hora_do_evento = models.TimeField()
    data_do_evento = models.DateField()
    descricao = models.CharField(max_length=100)
    endereco = models.CharField(max_length=30)
    usuario = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        db_table = 'Eventos'

    def __str__(self):
        return self.nome_do_evento


# =========================
# FÓRUM
# =========================
class Forum(models.Model):
    nome = models.CharField(max_length=30)
    data_criacao = models.DateField()
    usuario = models.ForeignKey(Usuario, on_delete=models.DO_NOTHING, null=True, blank=True)

    class Meta:
        db_table = 'Forum'


class Topico(models.Model):
    forum = models.ForeignKey(Forum, on_delete=models.CASCADE, related_name='topicos')
    descricao = models.TextField(blank=True, null=True)
    titulo = models.CharField(max_length=100)

    class Meta:
        db_table = 'Topico'


class Mensagem(models.Model):
    forum = models.ForeignKey(Forum, on_delete=models.CASCADE, related_name='mensagens')
    autor = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    conteudo = models.TextField()
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'Mensagem'

    def __str__(self):
        nome_autor = getattr(self.autor, "nome", str(self.autor.id))
        return f'{nome_autor}: {self.conteudo[:30]}'


# =========================
# PASTAS E ARQUIVOS
# =========================
class Pasta(models.Model):
    nome = models.CharField(max_length=100)
    criada_por = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    criada_em = models.DateTimeField(auto_now_add=True)
    turma = models.ForeignKey(Turma, on_delete=models.CASCADE)
    pasta_pai = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='subpastas')

    class Meta:
        db_table = 'Pasta'

    def __str__(self):
        return self.nome


class Arquivo(models.Model):
    nome = models.CharField(max_length=100)
    arquivo = CloudinaryField(resource_type='auto')
    enviado_por = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    enviado_em = models.DateTimeField(auto_now_add=True)
    turma = models.ForeignKey(Turma, on_delete=models.CASCADE)
    pasta = models.ForeignKey(Pasta, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        db_table = 'Arquivo'

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
