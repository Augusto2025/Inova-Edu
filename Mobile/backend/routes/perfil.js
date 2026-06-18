const express = require('express');
const router = express.Router();
const pool = require('../config/db'); // Conexão com o Postgres

// =================================================================
// 1. GET: Buscar todos os dados do perfil de um usuário específico
// =================================================================
// URL: /perfil/:usuarioId
router.get('/:usuarioId', async (req, res) => {
    const { usuarioId } = req.params;

    try {
        // 1. Busca dados do usuário (AJUSTADO PARA imagem_usuario) + Monta a string da Turma
        const userQuery = `
            SELECT 
                u."idUsuario", 
                u."Nome" as nome, 
                u."Sobrenome" as sobrenome, 
                u."Descricao" as descricao,
                u.imagem_usuario as imagem,
                CONCAT(t."Codigo_Turma", ' - ', t."Ano", ' (', t."Turno", ')') as turma
            FROM usuario u
            LEFT JOIN usuario_da_turma ut ON u."idUsuario" = ut."ID_Usuario"
            LEFT JOIN turma t ON ut."ID_Turma" = t."idTurma"
            WHERE u."idUsuario" = $1
        `;
        
        // 2. Busca os certificados do usuário
        const certQuery = `
            SELECT "idCertificado" as id, "nome", "descricao"
            FROM certificado
            WHERE "usuario_id" = $1
        `;

        // 3. Busca os projetos do aluno
        const projQuery = `
            SELECT DISTINCT 
                p."idProjeto" as id, 
                p."Nome_projeto" as nome, 
                p."Descricao" as descricao
            FROM projeto p
            LEFT JOIN projeto_alunos pa ON p."idProjeto" = pa."projeto_id"
            LEFT JOIN usuario_da_turma ut ON p."ID_Turma" = ut."ID_Turma"
            WHERE pa."usuario_id" = $1 OR ut."ID_Usuario" = $1
        `;

        // Executa todas as consultas em paralelo para máxima performance
        const [userRes, certRes, projRes] = await Promise.all([
            pool.query(userQuery, [usuarioId]),
            pool.query(certQuery, [usuarioId]),
            pool.query(projQuery, [usuarioId])
        ]);

        if (userRes.rows.length === 0) {
            return res.status(404).json({ sucesso: false, mensagem: "Usuário não encontrado." });
        }

        // Retorna o objeto completo estruturado para o Frontend
        return res.json({
            sucesso: true,
            usuario: userRes.rows[0],
            certificados: certRes.rows,
            projetos: projRes.rows
        });

    } catch (err) {
        console.error("❌ Erro ao buscar perfil completo:", err.message);
        return res.status(500).json({ sucesso: false, mensagem: "Erro interno no servidor." });
    }
});

// =================================================================
// 2. PUT: Atualizar apenas a foto de perfil (URL do Cloudinary)
// =================================================================
// URL: /perfil/atualizar-foto
router.put('/atualizar-foto', async (req, res) => {
    const { idUsuario, imagem } = req.body; 

    if (!idUsuario) {
        return res.status(400).json({ sucesso: false, mensagem: "ID do usuário é obrigatório." });
    }

    try {
        // ✅ CORRIGIDO: Faz o UPDATE usando a coluna imagem_usuario
        const query = `
            UPDATE usuario
            SET imagem_usuario = $1
            WHERE "idUsuario" = $2
        `;
        
        const resultado = await pool.query(query, [imagem, idUsuario]);

        if (resultado.rowCount === 0) {
            return res.status(404).json({ sucesso: false, mensagem: "Usuário não encontrado para atualizar." });
        }

        return res.json({
            sucesso: true,
            mensagem: "Foto de perfil atualizada com sucesso!",
            novaUrl: imagem
        });

    } catch (err) {
        console.error("❌ Erro ao atualizar foto no banco:", err.message);
        return res.status(500).json({ sucesso: false, message: "Erro interno ao salvar imagem." });
    }
});

module.exports = router;