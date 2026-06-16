const express = require('express');
const router = express.Router();
const db = require('../config/db'); // Usa a mesma conexão com o banco de dados

// ==========================================
// 1. ROTA: LISTAR TODOS OS TÓPICOS (GET)
// ==========================================
router.get('/', async (req, res) => {
    try {
        // SQL com LEFT JOIN para buscar o nome do usuário (autor)
        // Nota: No Django, a FK 'usuario' vira a coluna 'usuario_id' no banco SQL.
        const query = `
            SELECT 
                f.idforum AS id,
                f.nome AS titulo,
                f.descricao,
                f.categoria,
                f.data_criacao,
                u.nome AS autor,
                (SELECT COUNT(*) FROM mensagem m WHERE m.forum_id = f.idforum) AS mensagens
            FROM forum f
            LEFT JOIN usuario u ON f.usuario_id = u.id
            ORDER BY f.idforum DESC
        `;
        
        const resultado = await db.query(query);

        // Mapeia os dados para o formato exato que o seu React Native espera
        const topicosFormatados = resultado.rows.map(item => ({
            id: item.id,
            titulo: item.titulo,
            descricao: item.descricao || "Sem descrição informada.",
            categoria: item.categoria || "Geral",
            mensagens: parseInt(item.mensagens) || 0,
            tempo: formatarData(item.data_criacao),
            autor: item.autor || "Usuário Anônimo",
            cor: "#0e68d6" // Cor padrão definida no seu App
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
    const { titulo, descricao, categoria, usuarioId } = req.body;

    // Validação básica igual à do seu frontend
    if (!titulo || !titulo.trim() || !descricao || !descricao.trim()) {
        return res.status(400).json({ mensagem: 'Título e descrição são obrigatórios.' });
    }

    try {
        const query = `
            INSERT INTO forum (nome, descricao, categoria, usuario_id, data_criacao)
            VALUES ($1, $2, $3, $4, CURRENT_DATE)
            RETURNING idforum
        `;
        const valores = [titulo, descricao, categoria || 'React Native', usuarioId];
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
    const { titulo, descricao } = req.body;

    try {
        const query = `
            UPDATE forum 
            SET nome = $1, descricao = $2 
            WHERE idforum = $3
            RETURNING idforum
        `;
        const resultado = await db.query(query, [titulo, descricao, id]);

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

        res.json({ mensagem: 'Tópico excluído com sucesso!' });

    } catch (error) {
        console.error("Erro ao deletar tópico:", error);
        res.status(500).json({ mensagem: 'Erro ao excluir o tópico.', detalhe: error.message });
    }
});

// FUNÇÃO AUXILIAR: Transforma a data do banco em texto amigável (ex: "Ontem" ou "15/06/2026")
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