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
const homeRoutes = require('./routes/home'); // 💻 Corrigido: alterado de 'home' para 'homeRoutes'

const topicoRoutes = require('./routes/topico');
const conversaRoutes = require('./routes/conversa');
const perfilRoutes = require('./routes/perfil');
const notificationsRoutes = require('./routes/notifications');
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
app.use('/home', homeRoutes); // 💻 Agora a variável existe e aponta corretamente!
app.use('/topico', topicoRoutes);
app.use('/conversa', conversaRoutes);
app.use('/perfil', perfilRoutes);
app.use('/notifications', notificationsRoutes);

// Middleware global de erro para garantir que nenhuma rota retorna erro sem tratamento
app.use((err, req, res, next) => {
    console.error('❌ Erro não tratado:', err.message);
    console.error('   Rota:', req.method, req.path);
    
    // Retorna sempre 500 com mensagem genérica, nunca deixa erro sem tratamento chegar ao frontend
    res.status(500).json({ 
        mensagem: 'Erro interno do servidor',
        erro: err.message 
    });
});

// Alterado para 3000 para alinhar com o padrão do seu frontend
const PORT = process.env.PORT || 3000; 
app.listen(PORT, () => {
  console.log(`🚀 Servidor backend rodando na porta ${PORT}`);
});