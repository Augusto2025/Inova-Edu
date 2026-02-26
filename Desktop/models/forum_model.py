from config.banco import conectar

def buscar_foruns_db():
    conn = conectar()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT idForum, Nome, Data_criacao, ID_Usuario
        FROM forum
        ORDER BY idForum DESC
    """)

    forums = cursor.fetchall()

    cursor.close()
    conn.close()

    return forums

def criar_forum_db(nome, usuario_id):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO forum (Nome, Data_criacao, ID_Usuario)
        VALUES (%s, NOW(), %s)
    """, (nome, usuario_id))

    conn.commit()
    cursor.close()
    conn.close()












def buscar_topicos_db(forum_id):
    conn = conectar()
    cursor = conn.cursor(dictionary=True)

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
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT m.Conteudo, m.Data_criacao, u.Nome
        FROM mensagem m
        JOIN usuario u ON u.idUsuario = m.ID_Usuario
        WHERE m.ID_Forum = %s
        ORDER BY m.Data_criacao ASC
    """, (forum_id,))

    mensagens = cursor.fetchall()

    cursor.close()
    conn.close()

    return mensagens


def enviar_mensagem(id_forum, id_usuario, conteudo):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO mensagem (ID_Forum, ID_Usuario, Conteudo)
        VALUES (%s, %s, %s)
    """, (id_forum, id_usuario, conteudo))

    conn.commit()
    conn.close()
    
    

