const express = require('express');
const router = express.Router();
const pool = require('../config/db');

// Rota que alimenta a HomeScreen em tempo real
router.get('/', async (req, res) => {
  try {
    // Executa as três consultas em paralelo usando Promise.all de forma limpa
    const [eventosRes, cursosRes, forumRes, projetosRes] = await Promise.all([
      // Eventos (usa colunas do DB)
      pool.query('SELECT "idEventos" AS id, "Nome_do_evento" AS title, "Hora_do_evento" AS time, "Data_do_evento" AS date, "Descricao" AS description, "Endereco" AS local FROM eventos ORDER BY "Data_do_evento" ASC LIMIT 3'),
      // Cursos (tabela e colunas corretas)
      pool.query('SELECT "idCurso" AS idcurso, "Nome_curso" AS nome_curso, "imagem_curso" AS imagem, "Descricao_curso" AS descricao FROM curso ORDER BY "Nome_curso" ASC'),
      // Fórum: junta com usuário para retornar título/autor
      pool.query(`SELECT f.idforum AS id, f.nome AS titulo, f.data_criacao, f.usuario_id, u."Nome" AS autor
                  FROM forum f LEFT JOIN usuario u ON f.usuario_id = u."idUsuario" ORDER BY f.idforum DESC LIMIT 1`),
      // Projetos/repositórios
      pool.query('SELECT "idProjeto" AS id, "Nome_projeto" AS nome, "Imagem" AS imagem, "Descricao" AS descricao FROM projeto ORDER BY "idProjeto" DESC LIMIT 4')
    ]);

    res.json({
      sucesso: true,
      usuario: { nome: "Estudante" }, 
      eventos: eventosRes.rows || [],
      cursos: cursosRes.rows || [],
      forum: forumRes.rows || [],
      projetos: projetosRes.rows || []
    });
    } catch (err) {
    console.error('Erro na rota /home:', err && err.stack ? err.stack : err);
    res.status(500).json({
      sucesso: false,
      mensagem: 'Erro interno ao carregar dados da Home.',
      eventos: [],
      cursos: [],
      forum: [],
      projetos: []
    });
  }
});

module.exports = router;