const express = require('express');
const router = express.Router();
const db = require('../config/db');
const archiver = require('archiver'); 

// ==========================================
// 🌟 1. ROTA PARA LISTAR PASTAS E ARQUIVOS NA TELA
// ==========================================
router.get('/', async (req, res) => {
    const { projetoId, pastaId } = req.query;

    if (!projetoId) {
        return res.status(400).json({ mensagem: 'ID do projeto é obrigatório.' });
    }

    try {
        let queryPastas, queryArquivos;
        let paramsPastas, paramsArquivos;

        // Se o usuário clicou para entrar em uma pasta
        if (pastaId && pastaId !== 'null') {
            // ⚠️ ATENÇÃO: Se a coluna que liga uma subpasta à pasta pai tiver outro nome 
            // no seu banco (ex: pai_id, ou pasta_pai_id), altere aqui embaixo!
            queryPastas = 'SELECT id, nome FROM pasta WHERE projeto_id = $1 AND pasta_pai_id = $2';
            paramsPastas = [projetoId, pastaId];

            queryArquivos = 'SELECT id, nome, tamanho FROM arquivo WHERE projeto_id = $1 AND pasta_id = $2';
            paramsArquivos = [projetoId, pastaId];
        } else {
            // Se o usuário está na raiz do projeto (fora de qualquer pasta)
            queryPastas = 'SELECT id, nome FROM pasta WHERE projeto_id = $1 AND pasta_pai_id IS NULL';
            paramsPastas = [projetoId];

            queryArquivos = 'SELECT id, nome, tamanho FROM arquivo WHERE projeto_id = $1 AND pasta_id IS NULL';
            paramsArquivos = [projetoId];
        }

        const resPastas = await db.query(queryPastas, paramsPastas);
        const resArquivos = await db.query(queryArquivos, paramsArquivos);

        // Mapeia as pastas para incluir o contador de itens exigido pelo seu frontend
        const pastasFormatadas = resPastas.rows.map(pasta => ({
            id: pasta.id,
            nome: pasta.nome,
            itens: 0 // Opcional: futuramente você pode fazer um COUNT de sub-itens aqui
        }));

        // Retorna exatamente a estrutura que o seu "carregarConteudo" do React Native espera
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
// 🌟 2. ROTA PARA DOWNLOAD DO REPOSITÓRIO EM ZIP
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

        const archive = archiver('zip', { zlib: { level: 9 } }); 
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