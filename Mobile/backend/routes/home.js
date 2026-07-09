const express = require('express');
const router = express.Router();
const pool = require('../config/db');

// Rota que alimenta a HomeScreen em tempo real
router.get('/', async (req, res) => {
  try {
    // Executa apenas as três consultas originais, sem mexer com repositórios
    const [eventosRes, cursosRes, forumRes] = await Promise.all([
      pool.query('SELECT id, title, date, time, local FROM evento ORDER BY date ASC LIMIT 3'),
      pool.query('SELECT idcurso, nome_curso, imagem, descricao FROM curso ORDER BY nome_curso ASC'),
      pool.query('SELECT id, titulo, descricao, mensagens FROM forum ORDER BY id DESC LIMIT 1')
    ]);

    res.json({
      sucesso: true,
      usuario: { nome: "Estudante" }, 
      eventos: eventosRes.rows,
      cursos: cursosRes.rows,
      forum: forumRes.rows
    });
  } catch (err) {
    console.error('Erro na rota home.js original:', err.message);
    res.status(500).json({ 
      sucesso: false, 
      mensagem: 'Erro interno ao carregar dados da Home.',
      eventos: [],
      cursos: [],
      forum: []
    });
  }
});

module.exports = router;