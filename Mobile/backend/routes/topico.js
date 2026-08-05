const express = require('express');
const router = express.Router();
const pool = require('../config/db'); // Sua conexão com o Postgres

// ==========================================
// HELPER: verifica se o usuário é Professor (moderador)
// ==========================================
async function ehProfessor(usuarioId) {
    if (!usuarioId) return false;
    const resultado = await pool.query(
        'SELECT "Tipo" FROM usuario WHERE "idUsuario" = $1',
        [usuarioId]
    );
    const tipo = resultado.rows[0]?.Tipo;
    return !!tipo && tipo.toLowerCase() === 'professor';
}

// 1. GET: Listar todos os tópicos de um fórum específico
// URL: /topico/forum/:forumId
router.get('/forum/:forumId', async (req, res) => {
    const { forumId } = req.params;

    try {
        const queryText = `
            SELECT 
                t."idtopico" AS id, 
                t."titulo", 
                t."descricao" AS mensagem, 
                t."forum_id" AS "forumId", 
                t."usuario_id" AS "usuarioIdCriador",
                u."Nome" AS autor
            FROM topico t
            LEFT JOIN usuario u ON t."usuario_id" = u."idUsuario"
            WHERE t."forum_id" = $1
            ORDER BY t."idtopico" DESC
        `;
        const resultado = await pool.query(queryText, [forumId]);
        return res.json(resultado.rows);
    } catch (err) {
        console.error('❌ Erro ao buscar tópicos:', err.message);
        return res.status(500).json({ sucesso: false, mensagem: 'Erro ao buscar tópicos do servidor.' });
    }
});

// 2. POST: Criar um novo tópico dentro do fórum
// URL: /topico
router.post('/', async (req, res) => {
    const { titulo, descricao, forumId, usuarioId } = req.body;

    try {
        const queryText = `
            INSERT INTO topico ("titulo", "descricao", "forum_id", "usuario_id") 
            VALUES ($1, $2, $3, $4) 
            RETURNING "idtopico" AS id
        `;
        const resultado = await pool.query(queryText, [titulo, descricao, forumId, usuarioId]);
        
        return res.status(201).json({
            sucesso: true,
            mensagem: 'Tópico criado com sucesso!',
            id: resultado.rows[0].id
        });
    } catch (err) {
        console.error('❌ Erro ao criar tópico:', err.message);
        return res.status(500).json({ sucesso: false, mensagem: 'Erro interno ao criar tópico.' });
    }
});

// 3. PUT: Editar um tópico existente (Valida se quem edita é o dono OU um professor/moderador)
// URL: /topico/:id
router.put('/:id', async (req, res) => {
    const { id } = req.params;
    const { titulo, descricao, usuarioId } = req.body;

    try {
        // Validação de segurança: Verifica se o tópico realmente pertence a quem está editando
        const checarDono = await pool.query('SELECT "usuario_id" FROM topico WHERE "idtopico" = $1', [id]);
        
        if (checarDono.rows.length === 0) {
            return res.status(404).json({ sucesso: false, mensagem: 'Tópico não encontrado.' });
        }

        const donoTopico = checarDono.rows[0].usuario_id;
        const moderador = await ehProfessor(usuarioId);

        if (donoTopico !== parseInt(usuarioId) && !moderador) {
            return res.status(403).json({ sucesso: false, mensagem: 'Você não tem permissão para editar este tópico.' });
        }

        const queryText = 'UPDATE topico SET "titulo" = $1, "descricao" = $2 WHERE "idtopico" = $3';
        await pool.query(queryText, [titulo, descricao, id]);

        return res.json({ sucesso: true, mensagem: 'Tópico atualizado com sucesso!' });
    } catch (err) {
        console.error('❌ Erro ao editar tópico:', err.message);
        return res.status(500).json({ sucesso: false, mensagem: 'Erro interno ao editar tópico.' });
    }
});

// 4. DELETE: Excluir um tópico (Valida se quem apaga é o dono OU um professor/moderador)
// URL: /topico/:id
router.delete('/:id', async (req, res) => {
    const { id } = req.params;
    const { usuarioId } = req.body;

    try {
        const checarDono = await pool.query('SELECT "usuario_id" FROM topico WHERE "idtopico" = $1', [id]);

        if (checarDono.rows.length === 0) {
            return res.status(404).json({ sucesso: false, mensagem: 'Tópico não encontrado.' });
        }

        const donoTopico = checarDono.rows[0].usuario_id;
        const moderador = await ehProfessor(usuarioId);

        if (donoTopico !== parseInt(usuarioId) && !moderador) {
            return res.status(403).json({ sucesso: false, mensagem: 'Você não tem permissão para apagar este tópico.' });
        }

        // Apaga também as mensagens desse tópico antes de apagar o tópico em si
        await pool.query('DELETE FROM mensagem WHERE "ID_Topico" = $1', [id]);
        await pool.query('DELETE FROM topico WHERE "idtopico" = $1', [id]);
        return res.json({ sucesso: true, mensagem: 'Tópico excluído com sucesso!' });
    } catch (err) {
        console.error('❌ Erro ao excluir tópico:', err.message);
        return res.status(500).json({ sucesso: false, mensagem: 'Erro interno ao excluir tópico.' });
    }
});

module.exports = router;