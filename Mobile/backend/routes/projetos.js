const express = require('express');
const router = express.Router();
const db = require('../config/db');

// Rota para listar projetos baseados em uma Turma específica
router.get('/', async (req, res) => {
    try {
        const { turmaId } = req.query;

        if (!turmaId) {
            return res.status(400).json({ mensagem: 'O parâmetro turmaId é obrigatório.' });
        }

        // Mapeamento idêntico às definições db_column do Django
        const queryTexto = `
            SELECT 
                "idProjeto" AS idprojeto,
                "Nome_projeto" AS nome_projeto,
                "Descricao" AS descricao,
                "Imagem" AS imagem
            FROM projeto
            WHERE "ID_Turma" = $1
            ORDER BY "idProjeto" DESC
        `;

        const resultado = await db.query(queryTexto, [turmaId]);
        res.json(resultado.rows);

    } catch (error) {
        res.status(500).json({ 
            mensagem: 'Erro interno no servidor de projetos.', 
            detalhe: error.message 
        });
    }
});

module.exports = router;