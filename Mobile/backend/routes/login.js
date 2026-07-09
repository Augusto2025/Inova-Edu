const express = require('express');
const router = express.Router();
const pool = require('../config/db'); 

router.post('/', async (req, res) => {
  const { email, senha } = req.body;
  if (!email || !senha) {
    return res.status(400).json({ sucesso: false, mensagem: 'Campos obrigatórios ausentes.' });
  }

  try {
    let queryText = 'SELECT idusuario, nome, email, senha, tipo FROM usuario WHERE email = $1';
    let resultado;
    
    try {
      resultado = await pool.query(queryText, [email.trim()]);
    } catch (e) {
      queryText = 'SELECT "idUsuario", "Nome", "Email", "Senha", "Tipo" FROM usuario WHERE "Email" = $1';
      resultado = await pool.query(queryText, [email.trim()]);
    }

    if (!resultado || resultado.rows.length === 0) {
      return res.status(401).json({ sucesso: false, mensagem: 'E-mail ou senha incorretos!' });
    }

    const row = resultado.rows[0];
    const usuarioSenha = row.senha || row.Senha;

    if (usuarioSenha !== senha) {
      return res.status(401).json({ sucesso: false, mensagem: 'E-mail ou senha incorretos!' });
    }

    return res.json({
      sucesso: true,
      mensagem: 'Login efetuado com sucesso!',
      usuario: {
        id: row.idusuario || row.idUsuario,
        nome: row.nome || row.Nome,
        email: row.email || row.Email,
        tipo: row.tipo || row.Tipo
      }
    });
  } catch (err) {
    console.error('Erro crítico no login:', err);
    return res.status(500).json({ sucesso: false, mensagem: err.message });
  }
});

module.exports = router;