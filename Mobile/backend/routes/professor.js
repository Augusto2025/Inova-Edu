const express = require('express');
const router = express.Router();
const pool = require('../config/db');

// GET /professor/painel?professorId=X
// Monta todos os dados do painel do professor usando dados reais do banco.
router.get('/painel', async (req, res) => {
    const { professorId } = req.query;

    if (!professorId) {
        return res.status(400).json({ sucesso: false, mensagem: 'professorId é obrigatório.' });
    }

    try {
        // 1. Dados básicos do professor
        const profRes = await pool.query(
            'SELECT "Nome" AS nome, "Sobrenome" AS sobrenome, imagem_usuario AS imagem FROM usuario WHERE "idUsuario" = $1',
            [professorId]
        );
        const professor = profRes.rows[0] || { nome: 'Professor', sobrenome: '' };

        // 2. Turmas do professor, com contagem de alunos e projetos por turma
        const turmasRes = await pool.query(`
            SELECT
                t."idTurma" AS id,
                t."Codigo_Turma" AS nome,
                COALESCE(alunos.total, 0) AS alunos,
                COALESCE(projetos.total, 0) AS projetos
            FROM turma t
            LEFT JOIN (
                SELECT "ID_Turma", COUNT(*) AS total
                FROM usuario_da_turma
                GROUP BY "ID_Turma"
            ) alunos ON alunos."ID_Turma" = t."idTurma"
            LEFT JOIN (
                SELECT "ID_Turma", COUNT(*) AS total
                FROM projeto
                GROUP BY "ID_Turma"
            ) projetos ON projetos."ID_Turma" = t."idTurma"
            WHERE t.professor_id = $1
            ORDER BY t."idTurma" DESC
        `, [professorId]);

        const turmas = turmasRes.rows.map(t => ({
            id: t.id,
            nome: t.nome,
            alunos: parseInt(t.alunos, 10),
            projetos: parseInt(t.projetos, 10)
        }));

        const idsTurmas = turmas.map(t => t.id);
        const totalAlunos = turmas.reduce((acc, t) => acc + t.alunos, 0);
        const totalProjetos = turmas.reduce((acc, t) => acc + t.projetos, 0);

        // 3. Total de tópicos criados pelo professor
        const topicosRes = await pool.query(
            `SELECT COUNT(*) AS total FROM topico WHERE usuario_id = $1`,
            [professorId]
        );
        const totalTopicos = parseInt(topicosRes.rows[0]?.total || 0, 10);

        // 4. Eventos de hoje (pro card de totais) e próximos eventos (pra lista, hoje + futuros)
        const totalEventosHojeRes = await pool.query(`
            SELECT COUNT(*) AS total FROM eventos WHERE "Data_do_evento" = CURRENT_DATE
        `);
        const totalEventosHoje = parseInt(totalEventosHojeRes.rows[0]?.total || 0, 10);

        const eventosProximosRes = await pool.query(`
            SELECT "idEventos" AS id, "Nome_do_evento" AS titulo, "Hora_do_evento" AS hora, 
                   "Data_do_evento" AS data, "Endereco" AS local
            FROM eventos 
            WHERE "Data_do_evento" >= CURRENT_DATE
            ORDER BY "Data_do_evento" ASC, "Hora_do_evento" ASC
            LIMIT 5
        `);
        const eventosProximos = eventosProximosRes.rows;

        // 5. Mensagens de outros usuários nos fóruns criados pelo professor
        const mensagensNovasRes = await pool.query(`
            SELECT
                t.idtopico AS id,
                t.titulo,
                t.forum_id,
                f.nome AS forum_nome,
                COUNT(m.id) FILTER (WHERE m."ID_Usuario" <> $1) AS total_mensagens
            FROM topico t
            JOIN forum f ON f.idforum = t.forum_id
            LEFT JOIN mensagem m ON m."ID_Topico" = t.idtopico AND m.excluida = false
            WHERE f.usuario_id = $1
            GROUP BY t.idtopico, t.titulo, t.forum_id, f.nome
            HAVING COUNT(m.id) FILTER (WHERE m."ID_Usuario" <> $1) > 0
            ORDER BY MAX(m."Data_criacao") DESC NULLS LAST
        `, [professorId]);

        const totalMensagensNovas = mensagensNovasRes.rows.reduce(
            (total, topico) => total + parseInt(topico.total_mensagens || 0, 10),
            0
        );

        // 6. Últimos fóruns criados (visão geral, com autor e total de tópicos)
        const ultimosForunsRes = await pool.query(`
            SELECT 
                f.idforum AS id,
                f.nome,
                f.data_criacao,
                u."Nome" AS autor,
                (SELECT COUNT(*) FROM topico t WHERE t.forum_id = f.idforum) AS total_topicos
            FROM forum f
            LEFT JOIN usuario u ON u."idUsuario" = f.usuario_id
            ORDER BY f.idforum DESC
            LIMIT 5
        `);
        const ultimosForuns = ultimosForunsRes.rows;

        // 7. Últimos projetos enviados nas turmas do professor
        let ultimosProjetos = [];
        if (idsTurmas.length > 0) {
            const projRes = await pool.query(`
                SELECT 
                    p."idProjeto" AS id,
                    p."Nome_projeto" AS nome,
                    p.data_de_criacao AS data,
                    t."Codigo_Turma" AS turma
                FROM projeto p
                JOIN turma t ON t."idTurma" = p."ID_Turma"
                WHERE p."ID_Turma" = ANY($1::int[])
                ORDER BY p.data_de_criacao DESC
                LIMIT 5
            `, [idsTurmas]);
            ultimosProjetos = projRes.rows;
        }

        return res.json({
            sucesso: true,
            professor: {
                nome: professor.nome,
                sobrenome: professor.sobrenome,
                imagem: professor.imagem
            },
            totais: {
                turmas: turmas.length,
                alunos: totalAlunos,
                projetos: totalProjetos,
                topicos: totalTopicos,
                eventosHoje: totalEventosHoje
            },
            turmas,
            eventosProximos,
            topicosComMensagens: mensagensNovasRes.rows,
            totalMensagensNovas,
            ultimosForuns,
            ultimosProjetos
        });

    } catch (err) {
        console.error('❌ Erro ao montar painel do professor:', err.message);
        return res.status(500).json({
            sucesso: false,
            mensagem: 'Erro interno ao montar painel do professor.',
            detalhe: err.message
        });
    }
});

module.exports = router;