const express = require('express');
const router = express.Router();
const pool = require('../config/db');

// Função auxiliar para executar queries com tratamento de erro individual
async function executeQuery(query, label) {
  try {
    const result = await pool.query(query);
    return { success: true, data: result.rows, label };
  } catch (err) {
    console.error(`❌ Erro ao executar query ${label}:`, err.message);
    return { success: false, data: [], label, error: err.message };
  }
}

// Rota que alimenta a HomeScreen em tempo real com fallback para dados parciais
router.get('/', async (req, res) => {
  try {
    // Executa todas as consultas em paralelo com tratamento individual de erros
    const results = await Promise.all([
      // Eventos (usa colunas do DB)
      executeQuery(
        `SELECT "idEventos" AS id, "Nome_do_evento" AS title, "Hora_do_evento" AS time, 
                "Data_do_evento" AS date, "Descricao" AS description, "Endereco" AS local 
         FROM eventos ORDER BY "Data_do_evento" ASC LIMIT 3`,
        'EVENTOS'
      ),
      // Cursos (tabela e colunas corretas)
      executeQuery(
        `SELECT "idCurso" AS idcurso, "Nome_curso" AS nome_curso, "imagem_curso" AS imagem, 
                "Descricao_curso" AS descricao 
         FROM curso ORDER BY "Nome_curso" ASC`,
        'CURSOS'
      ),
      // Fórum: junta com usuário para retornar título/autor
      executeQuery(
        `SELECT f.idforum AS id, f.nome AS titulo, f.data_criacao, f.usuario_id, u."Nome" AS autor
         FROM forum f LEFT JOIN usuario u ON f.usuario_id = u."idUsuario" 
         ORDER BY f.idforum DESC LIMIT 1`,
        'FORUM'
      ),
      // Projetos/repositórios
      executeQuery(
        `SELECT "idProjeto" AS id, "Nome_projeto" AS nome, "Imagem" AS imagem, "Descricao" AS descricao 
         FROM projeto ORDER BY "idProjeto" DESC LIMIT 4`,
        'PROJETOS'
      )
    ]);

    // Verifica se todas as queries foram bem-sucedidas
    const allSuccess = results.every(r => r.success);

    // Monta a resposta com dados parciais mesmo se alguma query falhar
    const response = {
      sucesso: allSuccess,
      usuario: { nome: "Estudante" },
      eventos: results[0].data || [],
      cursos: results[1].data || [],
      forum: results[2].data || [],
      projetos: results[3].data || []
    };

    // Se alguma query falhou, adiciona informação de fallback
    if (!allSuccess) {
      const failedQueries = results
        .filter(r => !r.success)
        .map(r => `${r.label}: ${r.error}`)
        .join(', ');
      
      console.warn(`⚠️ /home retornando dados parciais. Queries com falha: ${failedQueries}`);
      response.aviso = `Alguns dados não puderam ser carregados (${failedQueries})`;
    }

    // Retorna 200 mesmo com dados parciais (para não desencadear fallback no frontend)
    res.status(200).json(response);

  } catch (err) {
    console.error('❌ Erro crítico na rota /home:', err && err.stack ? err.stack : err);
    res.status(500).json({
      sucesso: false,
      mensagem: 'Erro interno ao carregar dados da Home.',
      usuario: { nome: "Estudante" },
      eventos: [],
      cursos: [],
      forum: [],
      projetos: [],
      erro_detalhes: err.message
    });
  }
});

module.exports = router;