const express = require('express');
const router = express.Router();
const pool = require('../config/db'); // Conexão com o Postgres

// GET: Buscar todos os dados do perfil de um usuário específico
// URL: /perfil/:usuarioId
router.get('/:usuarioId', async (req, res) => {
    const { usuarioId } = req.params;

    try {
        // 1. Busca dados do usuário + Nome da Turma (fazendo JOIN com as tabelas intermediárias)
        // Nota: Assumi que a tabela 'turma' possui uma coluna 'nome' ou 'codigo'. Ajuste se necessário!
        const userQuery = `
            SELECT 
                u."idUsuario", u."Nome" as nome, u."Sobrenome" as sobrenome, u."Descricao" as descricao,
                t."Nome" as turma
            FROM usuario u
            LEFT JOIN usuario_da_turma ut ON u."idUsuario" = ut."ID_Usuario"
            LEFT JOIN turma t ON ut."ID_Turma" = t."idTurma"
            WHERE u."idUsuario" = $1
        `;
        
        // 2. Busca os certificados do usuário
        // No Django, a FK gera a coluna 'usuario_id' automaticamente por padrão se não mapeada explicitamente
        const certQuery = `
            SELECT "idCertificado" as id, "nome", "descricao"
            FROM certificado
            WHERE "usuario_id" = $1
        `;

        // 3. Busca os projetos onde o aluno está vinculado (Relação ManyToMany do Django)
        // O Django cria a tabela intermediária com o padrão 'nome_tabela_nome_m2m' -> 'projeto_alunos'
        const projQuery = `
            SELECT p."idProjeto" as id, p."Nome_projeto" as nome, p."Descricao" as descricao
            FROM projeto p
            INNER JOIN projeto_alunos pa ON p."idProjeto" = pa."projeto_id"
            WHERE pa."usuario_id" = $1
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

module.exports = router;