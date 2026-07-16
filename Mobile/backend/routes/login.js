const express = require("express");
const router = express.Router();
const pool = require("../config/db");

router.post("/", async (req, res) => {
  // 1. CAPTURA O TIPO TAMBÉM (enviado pelo front-end)
  const { email, senha, tipo } = req.body;

  console.log("==================================");
  console.log("LOGIN RECEBIDO");
  console.log(req.body);

  try {
    // Mantemos a busca pelo e-mail
    const resultado = await pool.query(
      'SELECT "idUsuario","Nome","Email","Senha","Tipo" FROM usuario WHERE "Email"=$1',
      [email]
    );

    console.log("Quantidade encontrada:", resultado.rows.length);

    if (resultado.rows.length === 0) {
      return res.status(401).json({
        sucesso: false,
        mensagem: "Usuário não encontrado"
      });
    }

    const usuario = resultado.rows[0];

    console.log("Senha banco:", usuario.Senha);
    console.log("Senha enviada:", senha);

    // Validação da senha
    if (usuario.Senha !== senha) {
      return res.status(401).json({
        sucesso: false,
        mensagem: "Senha incorreta"
      });
    }

    // 2. O PULO DO GATO: Validação do Perfil/Tipo
    // Compara o tipo que está no banco com o tipo selecionado na tela
    // Usamos .toLowerCase() para evitar problemas caso um esteja "Aluno" e o outro "aluno"
    if (usuario.Tipo.toLowerCase() !== tipo.toLowerCase()) {
      return res.status(403).json({
        sucesso: false,
        mensagem: `Este usuário está cadastrado como ${usuario.Tipo} e não como ${tipo}.`
      });
    }

    // Se passou na senha e no tipo, libera o login
    return res.json({
      sucesso: true,
      usuario: {
        id: usuario.idUsuario,
        nome: usuario.Nome,
        email: usuario.Email,
        tipo: usuario.Tipo
      }
    });

  } catch (err) {
    console.log("ERRO COMPLETO");
    console.log(err);

    return res.status(500).json({
      sucesso: false,
      mensagem: err.message
    });
  }
});

module.exports = router;