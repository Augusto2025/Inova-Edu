const express = require('express');
const router = express.Router();
const db = require('../config/db'); // Sua conexão do banco

router.get('/', async (req, res) => {
    try {
        const { cursoId } = req.query;

        if (!cursoId) {
            return res.status(400).json({ mensagem: 'O parâmetro cursoId é obrigatório.' });
        }

        // Query SQL com JOIN para buscar os dados da turma e o nome do professor (Usuario)
        // Adaptado com aspas duplas seguindo o padrão de maiúsculas gerado pelo Django
        const queryTexto = `
            SELECT 
                t."idTurma" AS idturma,
                t."Codigo_Turma" AS codigo_turma,
                t."Turno" AS turno,
                t."Ano" AS ano,
                u."Nome" AS professor
            FROM turma t
            LEFT JOIN usuario u ON t."professor_id" = u."id"
            WHERE t."ID_Curso" = $1
        `;

        const resultado = await db.query(queryTexto, [cursoId]);
        res.json(resultado.rows);

    } catch (error) {
        console.error('Erro ao buscar turmas no banco:', error);
        res.status(500).json({ mensagem: 'Erro interno no servidor de turmas.' });
    }
});

module.exports = router;