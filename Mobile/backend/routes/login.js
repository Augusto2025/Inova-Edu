const express = require("express");
const router = express.Router();
const pool = require("../config/db");

router.post("/", async (req, res) => {
  const { email, senha } = req.body;

  console.log("==================================");
  console.log("LOGIN RECEBIDO");
  console.log(req.body);

  try {

    const resultado = await pool.query(
      'SELECT "idUsuario","Nome","Email","Senha","Tipo" FROM usuario WHERE "Email"=$1',
      [email]
    );

    console.log("Quantidade encontrada:", resultado.rows.length);

    if (resultado.rows.length > 0) {
      console.log("Usuário retornado:");
      console.log(resultado.rows[0]);
    }

    if (resultado.rows.length === 0) {
      return res.status(401).json({
        sucesso: false,
        mensagem: "Usuário não encontrado"
      });
    }

    const usuario = resultado.rows[0];

    console.log("Senha banco:", usuario.Senha);
    console.log("Senha enviada:", senha);

    if (usuario.Senha !== senha) {
      return res.status(401).json({
        sucesso: false,
        mensagem: "Senha incorreta"
      });
    }

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