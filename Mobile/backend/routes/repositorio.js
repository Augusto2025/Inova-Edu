const express = require('express');
const router = express.Router();
const db = require('../config/db');

router.get('/', async (req, res) => {
    try {
        const { projetoId, pastaId } = req.query;

        if (!projetoId) {
            return res.status(400).json({ mensagem: 'O parâmetro projetoId é obrigatório.' });
        }

        let pastasQuery = '';
        let arquivosQuery = '';
        let params = [];

        // Verifica se estamos navegando dentro de uma pasta ou na raiz do projeto
        if (pastaId && pastaId !== 'null' && pastaId !== 'undefined') {
            pastasQuery = `SELECT id, nome FROM pasta WHERE pasta_pai_id = $1 ORDER BY nome ASC`;
            arquivosQuery = `SELECT id, nome, url FROM arquivo WHERE pasta_id = $1 ORDER BY nome ASC`;
            params = [pastaId];
        } else {
            pastasQuery = `SELECT id, nome FROM pasta WHERE projeto_id = $1 AND pasta_pai_id IS NULL ORDER BY nome ASC`;
            arquivosQuery = `SELECT id, nome, url FROM arquivo WHERE projeto_id = $1 AND pasta_id IS NULL ORDER BY nome ASC`;
            params = [projetoId];
        }

        const [pastasRes, arquivosRes] = await Promise.all([
            db.query(pastasQuery, params),
            db.query(arquivosQuery, params)
        ]);

        // Calcula dinamicamente a quantidade de subitens de cada pasta
        const pastasComContagem = await Promise.all(pastasRes.rows.map(async (pasta) => {
            const subpastasCont = await db.query(`SELECT COUNT(*) FROM pasta WHERE pasta_pai_id = $1`, [pasta.id]);
            const arquivosCont = await db.query(`SELECT COUNT(*) FROM arquivo WHERE pasta_id = $1`, [pasta.id]);
            const totalItens = parseInt(subpastasCont.rows[0].count) + parseInt(arquivosCont.rows[0].count);
            
            return {
                id: pasta.id,
                nome: pasta.nome,
                itens: totalItens
            };
        }));

        res.json({
            pastas: pastasComContagem,
            arquivos: arquivosRes.rows.map(arq => ({
                id: arq.id,
                nome: arq.nome,
                url: arq.url,
                tamanho: "Arquivo"
            }))
        });

    } catch (error) {
        res.status(500).json({ 
            mensagem: 'Erro interno no servidor do repositório.', 
            detalhe: error.message 
        });
    }
});

module.exports = router;