from config.banco import conectar
from psycopg2.extras import RealDictCursor

def buscar_foruns_db():
    conn = conectar()
    cursor = conn.cursor(cursor_factory=RealDictCursor)

    cursor.execute("""
        SELECT idforum, nome, data_criacao
        FROM forum
        ORDER BY idforum DESC
    """)

    forums = cursor.fetchall()

    cursor.close()
    conn.close()

    return forums


def criar_forum_db(nome, usuario_id):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO forum (nome, data_criacao, id_usuario)
        VALUES (%s, NOW(), %s)
    """, (nome, usuario_id))

    conn.commit()
    cursor.close()
    conn.close()


def buscar_topicos_db(forum_id):
    conn = conectar()
    cursor = conn.cursor(cursor_factory=RealDictCursor)

    cursor.execute("""
        SELECT idtopico, titulo, descricao
        FROM topico
        WHERE forum_id = %s
    """, (forum_id,))

    topicos = cursor.fetchall()

    cursor.close()
    conn.close()

    return topicos

def buscar_mensagens_db(forum_id):
    conn = conectar()
    cursor = conn.cursor(cursor_factory=RealDictCursor)

    cursor.execute("""
        SELECT m.conteudo, m.data_criacao, u.nome
        FROM mensagem m
        JOIN usuario u ON u.idusuario = m.id_usuario
        WHERE m.idforum = %s
        ORDER BY m.data_criacao ASC
    """, (forum_id,))

    mensagens = cursor.fetchall()

    cursor.close()
    conn.close()

    return mensagens


def enviar_mensagem(id_forum, id_usuario, conteudo):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO mensagem (idforum, id_usuario, conteudo)
        VALUES (%s, %s, %s)
    """, (id_forum, id_usuario, conteudo))

    conn.commit()
    cursor.close()
    conn.close()