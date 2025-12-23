from django.db import models
from django.contrib.auth.models import AbstractUser


# -------------------------------
# Usuário personalizado (se necessário)
# -------------------------------
class Usuario(models.Model):
    idusuario = models.AutoField(db_column='idUsuario', primary_key=True)
    imagem = models.ImageField(db_column='imagem_usuario', upload_to='usuarios/', blank=True, null=True)
    tipo = models.CharField(db_column='Tipo', max_length=11)
    nome = models.CharField(db_column='Nome', max_length=20)
    sobrenome = models.CharField(db_column='Sobrenome', max_length=20)
    email = models.CharField(db_column='Email', max_length=45)
    senha = models.CharField(db_column='Senha', max_length=128)  # aumentado para compatibilidade Django
    descricao = models.CharField(db_column='Descricao', max_length=100, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'usuario'

    def __str__(self):
        return f'{self.nome} {self.sobrenome}'


# -------------------------------
# Curso
# -------------------------------
class Curso(models.Model):
    idcurso = models.AutoField(db_column='idCurso', primary_key=True)
    nome_curso = models.CharField(db_column='Nome_curso', max_length=45)
    imagem = models.ImageField(db_column='imagem_curso', upload_to='curso/', blank=True, null=True)
    descricao_curso = models.CharField(db_column='Descricao_curso', max_length=100, blank=True, null=True)
    data_inicio = models.DateField(db_column='Data_inicio', blank=True, null=True)
    data_final = models.DateField(db_column='Data_final', blank=True, null=True)
    usuario = models.ForeignKey(Usuario, models.SET_NULL, db_column='ID_Usuario', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'curso'

    def __str__(self):
        return self.nome_curso


# -------------------------------
# Turma
# -------------------------------
class Turma(models.Model):
    idturma = models.AutoField(db_column='idTurma', primary_key=True)
    codigo_turma = models.CharField(db_column='Codigo_Turma', max_length=11)
    turno = models.CharField(db_column='Turno', max_length=5, blank=True, null=True)
    ano = models.IntegerField(db_column='Ano')
    curso = models.ForeignKey(Curso, models.CASCADE, db_column='ID_Curso')

    class Meta:
        managed = True
        db_table = 'turma'

    def __str__(self):
        return f'{self.codigo_turma} - {self.curso.nome_curso}'


# -------------------------------
# Projeto
# -------------------------------
class Projeto(models.Model):
    idprojeto = models.AutoField(db_column='idProjeto', primary_key=True)
    nome_projeto = models.CharField(db_column='Nome_projeto', max_length=30)
    data_de_criacao = models.DateField(auto_now_add=True)
    data_de_modificacao = models.DateField(auto_now=True)
    turma = models.ForeignKey(Turma, models.CASCADE, db_column='ID_Turma')
    curso = models.ForeignKey(Curso, models.CASCADE, db_column='ID_Curso', blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'projeto'

    def __str__(self):
        return self.nome_projeto


# -------------------------------
# UsuarioDaTurma (many-to-many)
# -------------------------------
class UsuarioDaTurma(models.Model):
    id = models.BigAutoField(primary_key=True)
    id_usuario = models.ForeignKey(Usuario, models.CASCADE, db_column='ID_Usuario')
    id_turma = models.ForeignKey(Turma, models.CASCADE, db_column='ID_Turma')

    class Meta:
        managed = False
        db_table = 'usuario_da_turma'
        unique_together = (('id_usuario', 'id_turma'),)

    def __str__(self):
        return f'{self.id_usuario} -> {self.id_turma}'


# -------------------------------
# Eventos
# -------------------------------
class Eventos(models.Model):
    ideventos = models.AutoField(db_column='idEventos', primary_key=True)
    nome_do_evento = models.CharField(db_column='Nome_do_evento', max_length=30)
    hora_do_evento = models.TimeField(db_column='Hora_do_evento')
    data_do_evento = models.DateField(db_column='Data_do_evento')
    descricao = models.CharField(db_column='Descricao', max_length=100)
    endereco = models.CharField(db_column='Endereco', max_length=30)
    usuario = models.ForeignKey(Usuario, models.SET_NULL, db_column='ID_Usuario', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'eventos'

    def __str__(self):
        return self.nome_do_evento


# -------------------------------
# Forum
# -------------------------------
class Forum(models.Model):
    idforum = models.AutoField(db_column='idForum', primary_key=True)
    nome = models.CharField(db_column='Nome', max_length=30)
    data_criacao = models.DateField(db_column='Data_criacao')
    usuario = models.ForeignKey(Usuario, models.SET_NULL, db_column='ID_Usuario', blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'forum'

    def __str__(self):
        return self.nome


# -------------------------------
# Mensagem
# -------------------------------
class Mensagem(models.Model):
    forum = models.ForeignKey(Forum, on_delete=models.CASCADE, db_column='ID_Forum', related_name='mensagens')
    autor = models.ForeignKey(Usuario, on_delete=models.CASCADE, db_column='ID_Usuario')
    conteudo = models.TextField(db_column='Conteudo')
    criado_em = models.DateTimeField(db_column='Data_criacao', auto_now_add=True)

    class Meta:
        db_table = 'mensagem'

    def __str__(self):
        nome_autor = getattr(self.autor, "username", getattr(self.autor, "nome", str(self.autor.id)))
        return f'{nome_autor}: {self.conteudo[:30]}'