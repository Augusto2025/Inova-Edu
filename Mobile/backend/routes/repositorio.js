const express = require('express');
const router = express.Router();
const db = require('../config/db');

// Importa o módulo do archiver
const archiverModule = require('archiver'); 

// FUNÇÃO AUXILIAR ATUALIZADA COM INSTANCIAÇÃO DIRETA DE CLASSE
function criarInstanciaZip(format, options) {
    // 1. Se for o padrão CommonJS (função direta)
    if (typeof archiverModule === 'function') {
        return archiverModule(format, options);
    }
    // 2. Se for interop de ES Modules tradicional (dentro de .default)
    if (archiverModule && typeof archiverModule.default === 'function') {
        return archiverModule.default(format, options);
    }
    // 3. Se o módulo expuser o método nativo .create
    if (archiverModule && typeof archiverModule.create === 'function') {
        return archiverModule.create(format, options);
    }
    
    // 🌟 4. SOLUÇÃO PARA O RENDER: Instancia a classe correspondente direto do protótipo do módulo
    if (archiverModule) {
        if (format === 'zip' && typeof archiverModule.ZipArchive === 'function') {
            return new archiverModule.ZipArchive(options);
        }
        if (format === 'tar' && typeof archiverModule.TarArchive === 'function') {
            return new archiverModule.TarArchive(options);
        }
    }

    // 5. Caso a classe estivesse dentro de um .default
    if (archiverModule && archiverModule.default) {
        if (format === 'zip' && typeof archiverModule.default.ZipArchive === 'function') {
            return new archiverModule.default.ZipArchive(options);
        }
    }
    
    throw new Error("Não foi possível encontrar uma estrutura válida para o 'archiver'.");
}

// ==========================================
// 1. ROTA PARA LISTAR PASTAS E ARQUIVOS NA TELA
// ==========================================
router.get('/', async (req, res) => {
    const { projetoId, pastaId } = req.query;

    if (!projetoId) {
        return res.status(400).json({ mensagem: 'ID do projeto é obrigatório.' });
    }

    try {
        let queryPastas, queryArquivos;
        let paramsPastas, paramsArquivos;

        if (pastaId && pastaId !== 'null') {
            queryPastas = 'SELECT id, nome FROM pasta WHERE projeto_id = $1 AND pasta_pai_id = $2';
            paramsPastas = [projetoId, pastaId];

            queryArquivos = 'SELECT id, nome FROM arquivo WHERE projeto_id = $1 AND pasta_id = $2';
            paramsArquivos = [projetoId, pastaId];
        } else {
            queryPastas = 'SELECT id, nome FROM pasta WHERE projeto_id = $1 AND pasta_pai_id IS NULL';
            paramsPastas = [projetoId];

            queryArquivos = 'SELECT id, nome FROM arquivo WHERE projeto_id = $1 AND pasta_id IS NULL';
            paramsArquivos = [projetoId];
        }

        const resPastas = await db.query(queryPastas, paramsPastas);
        const resArquivos = await db.query(queryArquivos, paramsArquivos);

        const pastasFormatadas = resPastas.rows.map(pasta => ({
            id: pasta.id,
            nome: pasta.nome,
            itens: 0 
        }));

        res.json({
            pastas: pastasFormatadas,
            arquivos: resArquivos.rows
        });

    } catch (error) {
        console.error("Erro ao listar repositório:", error);
        res.status(500).json({ mensagem: 'Erro ao carregar dados do repositório.', detalhe: error.message });
    }
});


// ==========================================
// 2. ROTA PARA DOWNLOAD DO REPOSITÓRIO EM ZIP
// ==========================================
router.get('/download-zip', async (req, res) => {
    const { projetoId } = req.query;

    if (!projetoId) {
        return res.status(400).json({ mensagem: 'ID do projeto é obrigatório.' });
    }

    try {
        const queryPastas = 'SELECT id, nome FROM pasta WHERE projeto_id = $1';
        const resPastas = await db.query(queryPastas, [projetoId]);
        const pastas = resPastas.rows;

        const queryArquivos = 'SELECT nome, pasta_id FROM arquivo WHERE projeto_id = $1';
        const resArquivos = await db.query(queryArquivos, [projetoId]);
        const arquivos = resArquivos.rows;

        res.attachment(`repositorio_projeto_${projetoId}.zip`);
        res.setHeader('Content-Type', 'application/zip');

        // Chama a função assistente que vai disparar os logs de diagnóstico
        const archive = criarInstanciaZip('zip', { zlib: { level: 9 } }); 
        archive.pipe(res);

        arquivos.forEach(arquivo => {
            let caminhoNoZip = '';

            if (arquivo.pasta_id) {
                const pastaDono = pastas.find(p => p.id === arquivo.pasta_id);
                caminhoNoZip = pastaDono ? `${pastaDono.nome}/${arquivo.nome}` : arquivo.nome;
            } else {
                caminhoNoZip = arquivo.nome; 
            }

            archive.append(`Conteúdo do arquivo simulado: ${arquivo.nome}`, { name: caminhoNoZip });
        });

        if (arquivos.length === 0) {
            archive.append('Este repositório não possui arquivos cadastrados.', { name: 'README.txt' });
        }

        await archive.finalize();

    } catch (error) {
        console.error("Erro ao gerar ZIP:", error);
        if (!res.headersSent) {
            res.status(500).json({ mensagem: 'Erro ao gerar o arquivo ZIP.', detalhe: error.message });
        }
    }
});

// ROTA ADICIONAL: BUSCA DE REPOSITÓRIOS/PROJETOS POR CURSO, TURMA OU NOME DO PROJETO
router.get('/search', async (req, res) => {
    try {
        const { q, cursoId, turmaId, page = 1, limit = 20 } = req.query;
        const params = [];
        const conditions = [];

        if (q && q.trim() !== '') {
            const termo = `%${q.trim()}%`;
            params.push(termo, termo, termo);
            conditions.push(
                '(p."Nome_projeto" ILIKE $' + (params.length - 2) +
                ' OR t."Codigo_Turma" ILIKE $' + (params.length - 1) +
                ' OR c."Nome_curso" ILIKE $' + params.length + ')'
            );
        }

        if (cursoId) {
            params.push(cursoId);
            conditions.push('c."idCurso" = $' + params.length);
        }

        if (turmaId) {
            params.push(turmaId);
            conditions.push('t."idTurma" = $' + params.length);
        }

        let whereClause = '';
        if (conditions.length > 0) {
            whereClause = 'WHERE ' + conditions.join(' AND ');
        }

        const offset = (parseInt(page, 10) - 1) * parseInt(limit, 10);
        params.push(limit);
        params.push(offset);

        const query = `
            SELECT
                p."idProjeto" AS id,
                p."Nome_projeto" AS nome_projeto,
                p."Descricao" AS descricao,
                p."Imagem" AS imagem,
                t."idTurma" AS id_turma,
                COALESCE(t."Codigo_Turma", '') AS nome_turma,
                c."idCurso" AS id_curso,
                COALESCE(c."Nome_curso", '') AS nome_curso
            FROM projeto p
            LEFT JOIN turma t ON p."ID_Turma" = t."idTurma"
            LEFT JOIN curso c ON t."ID_Curso" = c."idCurso"
            ${whereClause}
            ORDER BY p."idProjeto" DESC
            LIMIT $${params.length - 1}
            OFFSET $${params.length}
        `;

        const resultado = await db.query(query, params);
        res.json({
            pagina: parseInt(page, 10),
            limite: parseInt(limit, 10),
            resultados: resultado.rows
        });
    } catch (error) {
        console.error('Erro na busca de repositórios:', error);
        res.status(500).json({ mensagem: 'Erro ao buscar repositórios.', detalhe: error.message });
    }
});

module.exports = router;