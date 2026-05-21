// backend/routes/login.js
const express = require('express');
const router = express.Router();
const pool = require('../config/db'); // Puxa a conexão que testamos e funcionou!

// Rota de Login (POST: http://localhost:3000/login)
router.post('/login', async (req, res) => {
  const { email, senha } = req.body;

  console.log(`📩 Tentativa de login recebida para o e-mail: ${email}`);

  try {
    // 1. Procura o usuário na tabela do banco de dados pelo e-mail
    const queryText = 'SELECT idUsuario, Nome, Email, Senha FROM usuarios WHERE Email = $1';
    const resultado = await pool.query(queryText, [email]);

    // 2. Se o banco não retornar nenhuma linha, significa que o e-mail não existe
    if (resultado.rows.length === 0) {
      return res.status(401).json({
        sucesso: false,
        mensagem: 'E-mail ou senha incorretos!'
      });
    }

    const usuarioEncontrado = resultado.rows[0];

    // 3. Verifica se a senha digitada bate com a senha do banco
    if (usuarioEncontrado.Senha !== senha) {
      return res.status(401).json({
        sucesso: false,
        mensagem: 'E-mail ou senha incorretos!'
      });
    }

    // 4. Se passou por tudo, o login deu certo! Retorna os dados (escondendo a senha)
    return res.json({
      sucesso: true,
      mensagem: 'Login efetuado com sucesso!',
      usuario: {
        id: usuarioEncontrado.idUsuario,
        nome: usuarioEncontrado.Nome,
        email: usuarioEncontrado.Email
      }
    });

  } catch (err) {
    console.error('❌ Erro interno ao tentar fazer login:', err.message);
    return res.status(500).json({
      sucesso: false,
      mensagem: 'Erro interno no servidor ao processar o login.'
    });
  }
});

module.exports = router;