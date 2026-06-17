const express = require('express');
const router = express.Router();
const db = require('../config/db'); 

// ==========================================
// 1. ROTA: LISTAR TODOS OS TÓPICOS (GET) - CORRIGIDA COM SEU MODEL REAL
// ==========================================
router.get('/', async (req, res) => {
    try {
        const query = `
            SELECT 
                f.idforum AS id,
                f.nome AS titulo,
                f.data_criacao,
                u."Nome" AS autor,
                (SELECT COUNT(*) FROM mensagem m WHERE m.forum_id = f.idforum) AS mensagens
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
            mensagens: parseInt(item.mensagens) || 0,
            tempo: formatarData(item.data_criacao),
            autor: item.autor || "Usuário Anônimo",
            cor: "#0e68d6" 
        }));

        res.json(topicosFormatados);

    } catch (error) {
        console.error("Erro ao listar tópicos do fórum:", error);
        res.status(500).json({ mensagem: 'Erro ao carregar dados do fórum.', detalhe: error.message });
    }
});

// ==========================================
// 2. ROTA: CRIAR NOVO TÓPICO (POST)
// ==========================================
router.post('/', async (req, res) => {
    // Removemos a obrigatoriedade da descrição aqui, pois o banco não a guarda
    const { titulo, usuarioId } = req.body;

    if (!titulo || !titulo.trim()) {
        return res.status(400).json({ mensagem: 'O título do tópico é obrigatório.' });
    }

    try {
        // Query ajustada apenas para as colunas reais do seu modelo Django
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
// 3. ROTA: EDITAR UM TÓPICO (PUT)
// ==========================================
router.put('/:id', async (req, res) => {
    const { id } = req.params;
    const { titulo } = req.body; // Altera apenas o título (nome)

    try {
        const query = `
            UPDATE forum 
            SET nome = $1
            WHERE idforum = $2
            RETURNING idforum
        `;
        const resultado = await db.query(query, [titulo, id]);

        if (resultado.rows.length === 0) {
            return res.status(404).json({ mensagem: 'Tópico não encontrado para edição.' });
        }

        res.json({ mensagem: 'Tópico atualizado com sucesso!' });

    } catch (error) {
        console.error("Erro ao editar tópico:", error);
        res.status(500).json({ mensagem: 'Erro ao atualizar o tópico.', detalhe: error.message });
    }
});

// ==========================================
// 4. ROTA: DELETAR UM TÓPICO (DELETE)
// ==========================================
router.delete('/:id', async (req, res) => {
    const { id } = req.params;

    try {
        const query = 'DELETE FROM forum WHERE idforum = $1 RETURNING idforum';
        const resultado = await db.query(query, [id]);

        if (resultado.rows.length === 0) {
            return res.status(404).json({ mensagem: 'Tópico não encontrado para exclusão.' });
        }

        res.json({ message: 'Tópico excluído com sucesso!' });

    } catch (error) {
        console.error("Erro ao deletar tópico:", error);
        res.status(500).json({ mensagem: 'Erro ao excluir o tópico.', detalhe: error.message });
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