const express = require('express');
const router = express.Router();
const db = require('../config/db');

// ROTA GET (Busca)
router.get('/', async (req, res) => {
    try {
        const query = `
            SELECT 
                "idEventos" AS id, 
                "Nome_do_evento" AS title, 
                "Hora_do_evento" AS time, 
                "Data_do_evento" AS date, 
                "Descricao" AS description, 
                "Endereco" AS local,
                "ID_Usuario" AS usuario_id 
            FROM eventos 
            ORDER BY "Data_do_evento" ASC, "Hora_do_evento" ASC
        `;
        
        const resultado = await db.query(query);
        
        const eventos_Formatados = resultado.rows.map(evento => {
            const dataIso = new Date(evento.date).toISOString().split('T')[0];
            
            return {
                id: evento.id,
                title: evento.title,
                date: dataIso,
                time: evento.time.slice(0, 5),
                local: evento.local,
                description: evento.description,
                usuario_id: evento.usuario_id
            };
        });

        res.json(eventos_Formatados);
    } catch (error) {
        console.error("⚠️ Erro na busca de eventos:", error.message);
        // Retorna array vazio em vez de erro 500 para permitir fallback no frontend
        res.json([]);
    }
});

// ROTA POST (Cadastro) - ESTA ERA A QUE FALTAVA
router.post('/', async (req, res) => {
    const { title, time, date, description, local, usuario_id } = req.body;

    try {
        const query = `
            INSERT INTO eventos ("Nome_do_evento", "Hora_do_evento", "Data_do_evento", "Descricao", "Endereco", "ID_Usuario")
            VALUES ($1, $2, $3, $4, $5, $6)
            RETURNING *
        `;
        
        const resultado = await db.query(query, [title, time, date, description, local, usuario_id]);
        const eventoCriado = resultado.rows[0];

        // Cria notificações para todos os usuários, exceto quem criou o evento
        await db.query(
            `INSERT INTO notifications (usuario_id, tipo, titulo, subtitulo, tela_destino, parametros, entidade_id)
             SELECT "idUsuario", $1, $2, $3, $4, $5, $6
             FROM usuario
             WHERE "idUsuario" <> $7
            `,
            [
                'Eventos',
                `Novo evento: ${title}`,
                `${date} ${time}`,
                'Eventos',
                JSON.stringify({ eventoId: eventoCriado.idEventos }),
                eventoCriado.idEventos,
                usuario_id
            ]
        );

        res.status(201).json({ sucesso: true, mensagem: "Evento criado com sucesso!" });
    } catch (error) {
        console.error("Erro ao salvar:", error);
        res.status(500).json({ mensagem: 'Erro ao criar evento.', detalhe: error.message });
    }
});

// ROTA PUT (Editar)
router.put('/:id', async (req, res) => {
    const { id } = req.params;
    const { title, time, date, description, local, usuario_id } = req.body;

    try {
        const query = `
            UPDATE eventos 
            SET "Nome_do_evento" = $1, "Hora_do_evento" = $2, "Data_do_evento" = $3, 
                "Descricao" = $4, "Endereco" = $5
            WHERE "idEventos" = $6 AND "ID_Usuario" = $7
            RETURNING *
        `;
        const resultado = await db.query(query, [title, time, date, description, local, id, usuario_id]);

        if (resultado.rowCount === 0) {
            return res.status(403).json({ mensagem: "Você não tem permissão ou o evento não existe." });
        }

        res.json({ sucesso: true, mensagem: "Evento atualizado!" });
    } catch (error) {
        res.status(500).json({ mensagem: 'Erro ao atualizar.', detalhe: error.message });
    }
});

// ROTA DELETE (Excluir)
router.delete('/:id', async (req, res) => {
    const { id } = req.params;
    const { usuario_id } = req.body;

    try {
        const query = 'DELETE FROM eventos WHERE "idEventos" = $1 AND "ID_Usuario" = $2';
        const result = await db.query(query, [id, usuario_id]);

        if (result.rowCount === 0) return res.status(403).json({ mensagem: "Ação não permitida." });
        res.json({ sucesso: true });
    } catch (error) {
        res.status(500).json({ mensagem: 'Erro ao excluir.' });
    }
});

module.exports = router;