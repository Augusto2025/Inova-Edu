const express = require('express');
const router = express.Router();
const db = require('../config/db'); 

// ==========================================
// HELPER: verifica se o usuário é Professor (moderador)
// ==========================================
async function ehProfessor(usuarioId) {
    if (!usuarioId) return false;
    const resultado = await db.query(
        'SELECT "Tipo" FROM usuario WHERE "idUsuario" = $1',
        [usuarioId]
    );
    const tipo = resultado.rows[0]?.Tipo;
    return !!tipo && tipo.toLowerCase() === 'professor';
}

// ==========================================
// 1. ROTA: LISTAR TODOS OS TÓPICOS (GET)
// ==========================================
router.get('/', async (req, res) => {
    try {
        const query = `
            SELECT 
                f.idforum AS id,
                f.nome AS titulo,
                f.data_criacao,
                f.usuario_id,
                u."Nome" AS autor
            FROM forum f
            LEFT JOIN usuario u ON f.usuario_id = u."idUsuario"
            ORDER BY f.idforum DESC
        `;
        
        const resultado = await db.query(query);

        const topicosFormatados = resultado.rows.map(item => ({
            id: item.id,
            titulo: item.titulo,
            descricao: "Clique para abrir este fórum e participar das discussões.", 
            categoria: "Geral", 
            mensagens: 0, // Fixado em 0 por enquanto, ignorando a tabela de mensagens
            tempo: formatarData(item.data_criacao),
            autor: item.autor || "Usuário Anônimo",
            usuarioIdCriador: item.usuario_id, // Enviado ao Frontend para controle de permissões
            cor: "#0e68d6" 
        }));

        res.json(topicosFormatados);

    } catch (error) {
        console.error("⚠️ Erro ao listar tópicos do fórum:", error.message);
        // Retorna array vazio em vez de erro 500 para permitir fallback no frontend
        res.json([]);
    }
});

// ==========================================
// 2. ROTA: CRIAR NOVO TÓPICO (POST)
// ==========================================
router.post('/', async (req, res) => {
    const { titulo, usuarioId } = req.body;

    if (!titulo || !titulo.trim()) {
        return res.status(400).json({ mensagem: 'O título do tópico é obrigatório.' });
    }

    try {
        const query = `
            INSERT INTO forum (nome, usuario_id, data_criacao)
            VALUES ($1, $2, CURRENT_DATE)
            RETURNING idforum
        `;
        const valores = [titulo, usuarioId];
        const resultado = await db.query(query, valores);

        res.status(201).json({ 
            mensagem: 'Tópico criado com sucesso!', 
            idforum: resultado.rows[0].idforum 
        });

    } catch (error) {
        console.error("Erro ao criar tópico:", error);
        res.status(500).json({ mensagem: 'Erro ao salvar o tópico no fórum.', detalhe: error.message });
    }
});

// ==========================================
// 3. ROTA: EDITAR UM FÓRUM (PUT) - VALIDA DONO OU PROFESSOR (MODERADOR)
// ==========================================
router.put('/:id', async (req, res) => {
    const { id } = req.params;
    const { titulo, usuarioId } = req.body; // Recebe quem está tentando editar

    try {
        const moderador = await ehProfessor(usuarioId);

        // Se for professor, atualiza sem exigir que seja o dono do fórum.
        // Caso contrário, mantém a validação original (só o dono pode editar).
        const query = moderador
            ? `UPDATE forum SET nome = $1 WHERE idforum = $2 RETURNING idforum`
            : `UPDATE forum SET nome = $1 WHERE idforum = $2 AND usuario_id = $3 RETURNING idforum`;

        const valores = moderador ? [titulo, id] : [titulo, id, usuarioId];
        const resultado = await db.query(query, valores);

        if (resultado.rows.length === 0) {
            return res.status(403).json({ mensagem: 'Ação negada: Você não é o criador deste tópico.' });
        }

        res.json({ mensagem: 'Tópico atualizado com sucesso!' });

    } catch (error) {
        console.error("Erro ao editar tópico:", error);
        res.status(500).json({ mensagem: 'Erro ao atualizar o tópico.', detalhe: error.message });
    }
});

// ==========================================
// 4. ROTA: DELETAR UM FÓRUM (DELETE) - VALIDA DONO OU PROFESSOR (MODERADOR)
//    Exclui em cascata: mensagens dos tópicos -> tópicos -> fórum,
//    tudo dentro de uma transação (se algo falhar, desfaz tudo).
// ==========================================
router.delete('/:id', async (req, res) => {
    const { id } = req.params;
    const { usuarioId } = req.body; // Recebe quem está tentando deletar

    const client = await db.connect();

    try {
        const moderador = await ehProfessor(usuarioId);

        await client.query('BEGIN');

        // 1) Apaga as mensagens de todos os tópicos que pertencem a este fórum
        await client.query(
            `DELETE FROM mensagem
             WHERE "ID_Topico" IN (SELECT "idtopico" FROM topico WHERE "forum_id" = $1)`,
            [id]
        );

        // 2) Apaga os tópicos deste fórum
        await client.query(
            `DELETE FROM topico WHERE "forum_id" = $1`,
            [id]
        );

        // 3) Apaga o fórum em si. Professor (moderador) pode apagar de qualquer usuário;
        //    caso contrário, só se o usuarioId bater com o dono (mesma validação de antes).
        const query = moderador
            ? `DELETE FROM forum WHERE idforum = $1 RETURNING idforum`
            : `DELETE FROM forum WHERE idforum = $1 AND usuario_id = $2 RETURNING idforum`;
        const valores = moderador ? [id] : [id, usuarioId];

        const resultado = await client.query(query, valores);

        if (resultado.rows.length === 0) {
            // Ou o fórum não existe, ou o usuário não é o dono nem professor — desfaz tudo
            await client.query('ROLLBACK');
            return res.status(403).json({ mensagem: 'Ação negada: Você não é o criador deste fórum.' });
        }

        await client.query('COMMIT');
        res.json({ mensagem: 'Fórum e todos os seus tópicos foram excluídos com sucesso!' });

    } catch (error) {
        await client.query('ROLLBACK');
        console.error("Erro ao deletar fórum:", error);
        res.status(500).json({ mensagem: 'Erro ao excluir o fórum.', detalhe: error.message });
    } finally {
        client.release();
    }
});

function formatarData(dataDb) {
    if (!dataDb) return "Agora";
    const data = new Date(dataDb);
    const hoje = new Date();
    
    const diferencaTempo = Math.abs(hoje - data);
    const diferencaDias = Math.ceil(diferencaTempo / (1000 * 60 * 60 * 24));

    if (diferencaDias <= 1) return "Hoje";
    if (diferencaDias === 2) return "Ontem";
    
    return data.toLocaleDateString('pt-BR');
}

module.exports = router;