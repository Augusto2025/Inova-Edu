const express = require('express');
const router = express.Router();
const db = require('../config/db');

// IMPORTAÇÃO DETECTIVE: Captura o módulo do archiver
const archiverModule = require('archiver'); 

// FUNÇÃO AUXILIAR: Tenta todas as formas possíveis de criar o ZIP
function criarInstanciaZip(format, options) {
    // 1. Se for o padrão CommonJS (função direta)
    if (typeof archiverModule === 'function') {
        return archiverModule(format, options);
    }
    // 2. Se for interop de ES Modules (dentro de .default)
    if (archiverModule.default && typeof archiverModule.default === 'function') {
        return archiverModule.default(format, options);
    }
    // 3. Se o módulo expuser o método nativo .create
    if (typeof archiverModule.create === 'function') {
        return archiverModule.create(format, options);
    }
    // 4. Se o método .create estiver dentro do .default
    if (archiverModule.default && typeof archiverModule.default.create === 'function') {
        return archiverModule.default.create(format, options);
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

        // ALTERADO AQUI: Agora usamos a nossa função inteligente de criação
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

module.exports = router;