const express = require('express');
const router = express.Router();
const db = require('../config/db'); // Puxa a sua conexão com o Postgres

// Rota GET para listar os cursos: https://inova-edu-api.onrender.com/cursos
router.get('/', async (req, res) => {
    try {
        // Buscamos no banco usando aspas duplas por causa das maiúsculas do Django
        // e apelidamos (AS) para o formato que o aplicativo espera ler
        const queryTexto = `
            SELECT 
                "idCurso" AS idcurso, 
                "Nome_curso" AS nome_curso, 
                "imagem_curso" AS imagem,
                "Descricao_curso" AS descricao_curso
            FROM curso
        `;
        
        const resultado = await db.query(queryTexto);
        
        // Devolve a lista de cursos encontrados para o celular
        res.json(resultado.rows);
        
    } catch (error) {
        console.error('⚠️ Erro ao buscar cursos no banco:', error.message);
        // Retorna array vazio em vez de erro 500 para permitir fallback no frontend
        res.json([]);
    }
});

module.exports = router;