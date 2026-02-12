from config.banco import conectar

class UsuarioModel:
    def cadastrar(
        self,
        imagem,
        tipo,
        nome,
        sobrenome,
        email,
        senha,
        descricao
    ):
        conn = conectar()
        cursor = conn.cursor()

        sql = """
            INSERT INTO usuarios
            (imagem, tipo, nome, sobrenome, email, senha, descricao)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """

        cursor.execute(sql, (
            imagem,
            tipo,
            nome,
            sobrenome,
            email,
            senha,
            descricao
        ))

        conn.commit()
        cursor.close()
        conn.close()
