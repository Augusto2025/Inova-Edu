const express = require('express');
const router = express.Router();
const pool = require('../config/db'); // Conexão com o Postgres

// 1. GET: Listar todas as mensagens de um tópico específico (que não foram excluídas)
// URL: /mensagem/topico/:topicoId
router.get('/topico/:topicoId', async (req, res) => {
    const { topicoId } = req.params;

    try {
        const queryText = `
            SELECT 
                m."id", 
                m."Conteudo" AS texto, 
                m."Data_criacao" AS data,
                m."ID_Usuario" AS "autorId",
                u."Nome" AS nome,
                u."imagem_usuario" AS foto
            FROM mensagem m
            LEFT JOIN usuario u ON m."ID_Usuario" = u."idUsuario"
            WHERE m."ID_Topico" = $1 AND m."excluida" = false
            ORDER BY m."Data_criacao" ASC
        `;
        const resultado = await pool.query(queryText, [topicoId]);
        return res.json(resultado.rows);
    } catch (err) {
        console.error('❌ Erro ao buscar mensagens:', err.message);
        return res.status(500).json({ sucesso: false, mensagem: 'Erro ao buscar mensagens.' });
    }
});

// POST: Enviar uma nova mensagem no tópico
// URL: /conversa
router.post('/', async (req, res) => {
    const { conteudo, topicoId, usuarioId } = req.body;

    try {
        const queryText = `
            INSERT INTO mensagem ("Conteudo", "ID_Topico", "ID_Usuario", "excluida", "Data_criacao") 
            VALUES ($1, $2, $3, false, NOW()) 
            RETURNING "id"
        `;
        const resultado = await pool.query(queryText, [conteudo, topicoId, usuarioId]);

        const topicoRes = await pool.query(
            'SELECT "usuario_id", "titulo" FROM topico WHERE "idtopico" = $1',
            [topicoId]
        );

        if (topicoRes.rows.length > 0) {
            const donoTopico = topicoRes.rows[0];
            if (donoTopico.usuario_id !== parseInt(usuarioId, 10)) {
                await pool.query(
                    `INSERT INTO notifications (usuario_id, tipo, titulo, subtitulo, tela_destino, parametros, entidade_id)
                     VALUES ($1, $2, $3, $4, $5, $6, $7)`,
                    [
                        donoTopico.usuario_id,
                        'Forum',
                        'Nova resposta no seu tópico',
                        `Nova mensagem no tópico "${donoTopico.titulo}"`,
                        'Conversa',
                        JSON.stringify({ topicoId, titulo: donoTopico.titulo }),
                        topicoId
                    ]
                );
            }
        }

        return res.status(201).json({
            sucesso: true,
            mensagem: 'Mensagem enviada!',
            id: resultado.rows[0].id
        });
    } catch (err) {
        console.error('❌ Erro detalhado no banco Postgres:', err.message);
        console.error('❌ Stack:', err);
        return res.status(500).json({ sucesso: false, mensagem: 'Erro interno ao enviar mensagem.' });
    }
});

// 3. PUT: Editar o texto de uma mensagem (Apenas o autor pode alterar)
// URL: /mensagem/:id
router.put('/:id', async (req, res) => {
    const { id } = req.params;
    const { conteudo, usuarioId } = req.body;

    try {
        // Validação de segurança do proprietário
        const checarDono = await pool.query('SELECT "ID_Usuario" FROM mensagem WHERE "id" = $1', [id]);
        
        if (checarDono.rows.length === 0) {
            return res.status(404).json({ sucesso: false, mensagem: 'Mensagem não encontrada.' });
        }

        if (checarDono.rows[0].ID_Usuario !== parseInt(usuarioId)) {
            return res.status(403).json({ sucesso: false, message: 'Permissão negada.' });
        }

        const queryText = 'UPDATE mensagem SET "Conteudo" = $1 WHERE "id" = $2';
        await pool.query(queryText, [conteudo, id]);

        return res.json({ sucesso: true, mensagem: 'Mensagem atualizada!' });
    } catch (err) {
        console.error('❌ Erro ao editar mensagem:', err.message);
        return res.status(500).json({ sucesso: false, mensagem: 'Erro interno ao editar mensagem.' });
    }
});

// 4. DELETE: Exclusão lógica (Soft Delete) mudando 'excluida' para true
// URL: /mensagem/:id
router.delete('/:id', async (req, res) => {
    const { id } = req.params;
    const { usuarioId } = req.body;

    try {
        const checarDono = await pool.query('SELECT "ID_Usuario" FROM mensagem WHERE "id" = $1', [id]);

        if (checarDono.rows.length === 0) {
            return res.status(404).json({ sucesso: false, mensagem: 'Mensagem não encontrada.' });
        }

        if (checarDono.rows[0].ID_Usuario !== parseInt(usuarioId)) {
            return res.status(403).json({ sucesso: false, mensagem: 'Permissão negada.' });
        }

        // Soft delete conforme a propriedade 'excluida' do seu model
        const queryText = 'UPDATE mensagem SET "excluida" = true WHERE "id" = $1';
        await pool.query(queryText, [id]);
        
        return res.json({ sucesso: true, mensagem: 'Mensagem removida com sucesso!' });
    } catch (err) {
        console.error('❌ Erro ao excluir mensagem:', err.message);
        return res.status(500).json({ sucesso: false, mensagem: 'Erro interno ao remover mensagem.' });
    }
});

module.exports = router;