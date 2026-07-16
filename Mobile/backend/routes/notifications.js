const express = require('express');
const router = express.Router();
const pool = require('../config/db');

async function ensureNotificationsTable() {
  try {
    await pool.query(`
      CREATE TABLE IF NOT EXISTS notifications (
        id SERIAL PRIMARY KEY,
        usuario_id INTEGER NOT NULL,
        tipo TEXT NOT NULL,
        titulo TEXT NOT NULL,
        subtitulo TEXT,
        tela_destino TEXT,
        parametros JSONB,
        entidade_id INTEGER,
        lida BOOLEAN DEFAULT false,
        created_at TIMESTAMP DEFAULT NOW()
      )
    `);
    console.log('✅ Tabela notifications existe ou foi criada com sucesso.');
  } catch (error) {
    console.error('❌ Erro ao criar/verificar tabela notifications:', error.message);
  }
}

ensureNotificationsTable();

router.get('/', async (req, res) => {
  const { usuarioId } = req.query;
  if (!usuarioId) {
    return res.status(400).json({ sucesso: false, mensagem: 'O parâmetro usuarioId é obrigatório.' });
  }

  try {
    const resultado = await pool.query(
      `SELECT id, usuario_id AS "usuarioId", tipo, titulo, subtitulo, tela_destino AS "telaDestino", parametros, entidade_id AS "entidadeId", lida, created_at AS "createdAt"
       FROM notifications
       WHERE usuario_id = $1
       ORDER BY created_at DESC
      `,
      [usuarioId]
    );

    return res.json(resultado.rows);
  } catch (error) {
    console.error('❌ Erro ao buscar notificações:', error.message);
    return res.status(500).json({ sucesso: false, mensagem: 'Erro interno ao buscar notificações.' });
  }
});

router.post('/', async (req, res) => {
  const { usuarioId, tipo, titulo, subtitulo = '', telaDestino = null, parametros = null, entidadeId = null } = req.body;

  if (!usuarioId || !tipo || !titulo) {
    return res.status(400).json({ sucesso: false, mensagem: 'usuarioId, tipo e titulo são obrigatórios.' });
  }

  try {
    const resultado = await pool.query(
      `INSERT INTO notifications (usuario_id, tipo, titulo, subtitulo, tela_destino, parametros, entidade_id)
       VALUES ($1, $2, $3, $4, $5, $6, $7)
       RETURNING id, usuario_id AS "usuarioId", tipo, titulo, subtitulo, tela_destino AS "telaDestino", parametros, entidade_id AS "entidadeId", lida, created_at AS "createdAt"
      `,
      [usuarioId, tipo, titulo, subtitulo, telaDestino, parametros ? JSON.stringify(parametros) : null, entidadeId]
    );

    return res.status(201).json({ sucesso: true, notificacao: resultado.rows[0] });
  } catch (error) {
    console.error('❌ Erro ao criar notificação:', error.message);
    return res.status(500).json({ sucesso: false, mensagem: 'Erro interno ao criar notificação.' });
  }
});

router.patch('/:id/read', async (req, res) => {
  const { id } = req.params;
  const { usuarioId } = req.body;

  if (!usuarioId) {
    return res.status(400).json({ sucesso: false, mensagem: 'O parâmetro usuarioId é obrigatório.' });
  }

  try {
    const resultado = await pool.query(
      `UPDATE notifications SET lida = true WHERE id = $1 AND usuario_id = $2 RETURNING id, lida`,
      [id, usuarioId]
    );

    if (resultado.rowCount === 0) {
      return res.status(404).json({ sucesso: false, mensagem: 'Notificação não encontrada para este usuário.' });
    }

    return res.json({ sucesso: true, mensagem: 'Notificação marcada como lida.' });
  } catch (error) {
    console.error('❌ Erro ao marcar notificação como lida:', error.message);
    return res.status(500).json({ sucesso: false, mensagem: 'Erro interno ao marcar notificação como lida.' });
  }
});

// 🆕 Marca como lidas TODAS as notificações de um tópico específico para o usuário.
// Usado quando o usuário abre a tela de Conversa de um tópico — assim a contagem
// de "não lidas" daquele tópico zera automaticamente.
// URL: /notifications/topico/:topicoId/read
router.patch('/topico/:topicoId/read', async (req, res) => {
  const { topicoId } = req.params;
  const { usuarioId } = req.body;

  if (!usuarioId) {
    return res.status(400).json({ sucesso: false, mensagem: 'O parâmetro usuarioId é obrigatório.' });
  }

  try {
    const resultado = await pool.query(
      `UPDATE notifications 
       SET lida = true 
       WHERE entidade_id = $1 AND usuario_id = $2 AND tipo = 'Forum' AND lida = false
       RETURNING id`,
      [topicoId, usuarioId]
    );

    return res.json({ sucesso: true, marcadas: resultado.rowCount });
  } catch (error) {
    console.error('❌ Erro ao marcar notificações do tópico como lidas:', error.message);
    return res.status(500).json({ sucesso: false, mensagem: 'Erro interno ao marcar notificações do tópico como lidas.' });
  }
});

router.patch('/mark-all-read', async (req, res) => {
  const { usuarioId } = req.body;

  if (!usuarioId) {
    return res.status(400).json({ sucesso: false, mensagem: 'O parâmetro usuarioId é obrigatório.' });
  }

  try {
    await pool.query('UPDATE notifications SET lida = true WHERE usuario_id = $1', [usuarioId]);
    return res.json({ sucesso: true, mensagem: 'Todas as notificações foram marcadas como lidas.' });
  } catch (error) {
    console.error('❌ Erro ao marcar todas as notificações como lidas:', error.message);
    return res.status(500).json({ sucesso: false, mensagem: 'Erro interno ao atualizar notificações.' });
  }
});

module.exports = router;