const express = require('express');
const router = express.Router();
const db = require('../config/db');

// Rota para listar projetos baseados em uma Turma específica OU todos
router.get('/', async (req, res) => {
    try {
        const { turmaId } = req.query;

        console.log(`📝 GET /projetos chamado | turmaId=${turmaId || 'null'}`);

        let queryTexto;
        let params = [];

        // Se turmaId for fornecido E for um número válido, filtra por turma
        if (turmaId && !isNaN(turmaId)) {
            console.log(`🏫 Filtrando projetos da turma: ${turmaId}`);
            queryTexto = `
                SELECT 
                    "idProjeto" AS idprojeto,
                    "Nome_projeto" AS nome_projeto,
                    "Descricao" AS descricao,
                    "Imagem" AS imagem
                FROM projeto
                WHERE "ID_Turma" = $1
                ORDER BY "idProjeto" DESC
            `;
            params = [parseInt(turmaId, 10)];
        } else {
            // Modo HOME: retorna todos os projetos
            console.log(`📄 Modo HOME: retornando projetos`);
            queryTexto = `
                SELECT 
                    "idProjeto" AS idprojeto,
                    "Nome_projeto" AS nome_projeto,
                    "Descricao" AS descricao,
                    "Imagem" AS imagem
                FROM projeto
                ORDER BY "idProjeto" DESC
                LIMIT 4
            `;
        }

        const resultado = await db.query(queryTexto, params);
        console.log(`✅ Retornando ${resultado.rows.length} projetos`);
        
        // SEMPRE retorna status 200 com array
        return res.status(200).json(resultado.rows);

    } catch (error) {
        console.error('❌ Erro em /projetos GET:', error.message);
        
        // IMPORTANTE: Mesmo em erro, retorna status 200 com array vazio
        // Isso garante que o fallback no frontend nunca receba erro
        return res.status(200).json([]);
    }
});

module.exports = router;