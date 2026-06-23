const express = require('express');
const router = express.Router();
const db = require('../config/db');

router.get('/', async (req, res) => {
    try {
        // Query respeitando estritamente os db_column do seu Model Django
        const query = `
            SELECT 
                "idEventos" AS id, 
                "Nome_do_evento" AS title, 
                "Hora_do_evento" AS time, 
                "Data_do_evento" AS date, 
                "Descricao" AS description, 
                "Endereco" AS local 
            FROM eventos 
            ORDER BY "Data_do_evento" ASC, "Hora_do_evento" ASC
        `;
        
        const resultado = await db.query(query);
        
        // Tratamento simples dos dados (garantindo strings limpas de data e hora)
        const eventos_Formatados = resultado.rows.map(evento => {
            // Se a data vier como objeto Date, converte para YYYY-MM-DD
            const dataIso = new Date(evento.date).toISOString().split('T')[0];
            
            return {
                id: evento.id,
                title: evento.title,
                date: dataIso, // Mantém o padrão 'YYYY-MM-DD' exigido pelo calendário
                time: evento.time.slice(0, 5), // Remove os segundos (Ex: '19:00:00' -> '19:00')
                local: evento.local,
                description: evento.description
            };
        });

        res.json(eventos_Formatados);
    } catch (error) {
        res.status(500).json({ 
            mensagem: 'Erro ao buscar eventos no banco de dados.', 
            detalhe: error.message 
        });
    }
});

router.post('/', async (req, res) => {
    const { title, time, date, description, local, usuario_id } = req.body;

    try {
        const query = `
            INSERT INTO eventos ("Nome_do_evento", "Hora_do_evento", "Data_do_evento", "Descricao", "Endereco", "ID_Usuario")
            VALUES ($1, $2, $3, $4, $5, $6)
            RETURNING *
        `;
        
        await db.query(query, [title, time, date, description, local, usuario_id]);
        
        res.status(201).json({ sucesso: true, mensagem: "Evento criado com sucesso!" });
    } catch (error) {
        console.error("Erro ao salvar:", error);
        res.status(500).json({ mensagem: 'Erro ao criar evento.', detalhe: error.message });
    }
});

router.put('/:id', async (req, res) => {
    const { id } = req.params;
    const { title, time, date, description, local, usuario_id } = req.body;

    try {
        // Verifica se o evento pertence ao usuário antes de atualizar
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

module.exports = router;