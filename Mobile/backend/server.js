// server.js (Solto na raiz do backend)
require('dotenv').config(); // ISSO AQUI DEVE SER SEMPRE A LINHA 1!

const express = require('express');
const cors = require('cors');

// 1. Importa os arquivos de lógica que estão dentro da pasta routes
const authRoutes = require('./routes/login');
const cursosRoutes = require('./routes/cursos');
const turmasRoutes = require('./routes/turmas');
const projetosRoutes = require('./routes/projetos');
const repositorioRoutes = require('./routes/repositorio');
const eventosRoutes = require('./routes/eventos');
const forumRoutes = require('./routes/forum');
const topicoRoutes = require('./routes/topico');
const conversaRoutes = require('./routes/conversa');
const app = express();
app.use(express.json());
app.use(cors());

// 2. Encaminha as chamadas para os arquivos certos
app.use('/login', authRoutes);
app.use('/cursos', cursosRoutes); 
app.use('/turmas', turmasRoutes);
app.use('/projetos', projetosRoutes); 
app.use('/repositorio', repositorioRoutes); 
app.use('/eventos', eventosRoutes);
app.use('/forum', forumRoutes);
app.use('/topico', topicoRoutes);
app.use('/mensagem', conversaRoutes);

const PORT = process.env.PORT || 8081;
app.listen(PORT, () => {
  console.log(`Servidor backend rodando na porta ${PORT}`);
});