const express = require('express');
const router = express.Router();
const db = require('../config/db');
const archiver = require('archiver'); // Importa o compactador

// ROTA PARA DOWNLOAD DO REPOSITÓRIO EM ZIP
router.get('/download-zip', async (req, res) => {
    const { projetoId } = req.query;

    if (!projetoId) {
        return res.status(400).json({ mensagem: 'ID do projeto é obrigatório.' });
    }

    try {
        // 1. Busca todas as pastas do projeto para recriar a estrutura de diretórios
        const queryPastas = 'SELECT id, nome FROM pasta WHERE projeto_id = $1';
        const resPastas = await db.query(queryPastas, [projetoId]);
        const pastas = resPastas.rows;

        // 2. Busca todos os arquivos do projeto (e descobre a qual pasta eles pertencem)
        const queryArquivos = 'SELECT nome, pasta_id FROM arquivo WHERE projeto_id = $1';
        const resArquivos = await db.query(queryArquivos, [projetoId]);
        const arquivos = resArquivos.rows;

        // Configura os headers HTTP para forçar o navegador/celular a baixar um arquivo
        res.attachment(`repositorio_projeto_${projetoId}.zip`);
        res.setHeader('Content-Type', 'application/zip');

        // Cria o objeto do arquivo zip que vai direto para a resposta HTTP (Stream)
        const archive = archiver('zip', { zlib: { level: 9 } }); // Nível 9 = compressão máxima
        archive.pipe(res);

        // 3. Adiciona as pastas e arquivos na estrutura do ZIP
        arquivos.forEach(arquivo => {
            let caminhoNoZip = '';

            // Se o arquivo pertence a uma pasta, descobrimos o nome dela para criar a subpasta no ZIP
            if (arquivo.pasta_id) {
                const pastaDono = pastas.find(p => p.id === arquivo.pasta_id);
                caminhoNoZip = pastaDono ? `${pastaDono.nome}/${arquivo.nome}` : arquivo.nome;
            } else {
                caminhoNoZip = arquivo.nome; // Arquivo na raiz do repositório
            }

            /* 💡 NOTA IMPORTANTE: 
              Como seus arquivos atuais estão apenas salvos como texto/registro no banco de dados,
              vamos gerar um arquivo de texto simulado dentro do ZIP com o nome correto. 
              Quando você implementar o upload real (Blob/S3), basta trocar o "Conteúdo..." pelo binário do arquivo.
            */
            archive.append(`Conteúdo do arquivo simulado: ${arquivo.nome}`, { name: caminhoNoZip });
        });

        // Se o projeto estiver completamente vazio, adiciona um arquivo explicativo para o ZIP não ir corrompido
        if (arquivos.length === 0) {
            archive.append('Este repositório não possui arquivos cadastrados.', { name: 'README.txt' });
        }

        // Finaliza o arquivo e fecha a conexão de envio
        await archive.finalize();

    } catch (error) {
        console.error(error);
        if (!res.headersSent) {
            res.status(500).json({ mensagem: 'Erro ao gerar o arquivo ZIP.', detalhe: error.message });
        }
    }
});

module.exports = router;