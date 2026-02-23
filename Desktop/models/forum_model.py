from config.banco import conectar

def buscar_foruns_db():
    conn = conectar()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT idforum, nome, data_criacao
        FROM forum
        ORDER BY data_criacao DESC
    """)

    dados = cursor.fetchall()
    cursor.close()
    conn.close()

    foruns = []

    for f in dados:
        foruns.append({
            "nome": f["nome"],
            "idforum": f["idforum"],
            "data_criacao": str(f["data_criacao"]),
            "topics": []
        })

    return foruns


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