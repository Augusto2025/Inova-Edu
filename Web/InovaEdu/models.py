from django.db import models

class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group_id = models.IntegerField()
    permission_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group_id', 'permission_id'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type_id = models.IntegerField()
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
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
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user_id = models.IntegerField()
    group_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user_id', 'group_id'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user_id = models.IntegerField()
    permission_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user_id', 'permission_id'),)


class Usuario(models.Model):
    idusuario = models.AutoField(db_column='idUsuario', primary_key=True)
    imagem = models.ImageField(db_column='imagem_usuario', upload_to='usuarios/', blank=True, null=True)
    tipo = models.CharField(db_column='Tipo', max_length=11)
    nome = models.CharField(db_column='Nome', max_length=20)
    sobrenome = models.CharField(db_column='Sobrenome', max_length=20)
    email = models.CharField(db_column='Email', max_length=45)
    senha = models.CharField(db_column='Senha', max_length=30)
    descricao = models.CharField(db_column='Descricao', max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'usuario'


class Curso(models.Model):
    idcurso = models.AutoField(db_column='idCurso', primary_key=True)
    imagem = models.ImageField(db_column='imagem_curso' , upload_to='curso/', blank=True, null= True)
    nome_curso = models.CharField(db_column='Nome_curso', max_length=45)
    descricao_curso = models.CharField(db_column='Descricao_curso', max_length=100, blank=True, null=True)
    data_inicio = models.DateField(db_column='Data_inicio', blank=True, null=True)
    data_final = models.DateField(db_column='Data_final', blank=True, null=True)
    usuario = models.ForeignKey(Usuario, models.DO_NOTHING, db_column='ID_Usuario', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'curso'

    def __str__(self):
        return self.nome_curso


class Turma(models.Model):
    idturma = models.AutoField(db_column='idTurma', primary_key=True)
    codigo_turma = models.CharField(db_column='Codigo_Turma', max_length=11)
    turno = models.CharField(db_column='Turno', max_length=5, blank=True, null=True)
    curso = models.ForeignKey(Curso, models.DO_NOTHING, db_column='Curso_idCurso')

    class Meta:
        managed = False
        db_table = 'turma'


class Projeto(models.Model):
    idprojeto = models.AutoField(db_column='idProjeto', primary_key=True)
    nome_projeto = models.CharField(db_column='Nome_projeto', max_length=30)
    data_de_criacao = models.DateField(db_column='Data_de_criacao')
    data_de_modificacao = models.DateField(db_column='Data_de_modificacao')
    caminho_do_arquivo = models.CharField(db_column='Caminho_do_arquivo', max_length=50)
    turma = models.ForeignKey(Turma, models.DO_NOTHING, db_column='Turma_idTurma')

    class Meta:
        managed = False
        db_table = 'projeto'


class UsuarioDaTurma(models.Model):
    id = models.BigAutoField(primary_key=True) 
    id_usuario = models.ForeignKey(Usuario, models.DO_NOTHING, db_column='ID_Usuario')
    id_turma = models.ForeignKey(Turma, models.DO_NOTHING, db_column='ID_Turma')

    class Meta:
        managed = False
        db_table = 'usuario_da_turma'
        unique_together = (('id_usuario', 'id_turma'),)


class Eventos(models.Model):
    ideventos = models.AutoField(db_column='idEventos', primary_key=True)
    nome_do_evento = models.CharField(db_column='Nome_do_evento', max_length=30)
    hora_do_evento = models.TimeField(db_column='Hora_do_evento')
    data_do_evento = models.DateField(db_column='Data_do_evento')
    descricao = models.CharField(db_column='Descricao', max_length=100)
    endereco = models.CharField(db_column='Endereco', max_length=30)
    
    STATUS_CHOICES = [
        ('criado', 'Criado'),
        ('andamento', 'Em Andamento'),
        ('finalizado', 'Finalizado'),
    ]
    
    status = models.CharField(
        db_column='Status',
        max_length=20,
        choices=STATUS_CHOICES,
        default='criado'
    )

    usuario = models.ForeignKey(
        Usuario,
        models.DO_NOTHING,
        db_column='ID_Usuario',
        blank=True,
        null=True
    )

    class Meta:
        managed = False
        db_table = 'eventos'

class Forum(models.Model):
    idforum = models.AutoField(db_column='idForum', primary_key=True)
    nome = models.CharField(db_column='Nome', max_length=30)
    data_criacao = models.DateField(db_column='Data_criacao')
    usuario = models.ForeignKey(Usuario, models.DO_NOTHING, db_column='Usuario_idUsuario', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'forum'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type_id = models.IntegerField(blank=True, null=True)
    user_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'