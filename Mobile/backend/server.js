// server.js
require('dotenv').config(); // SEMPRE PRIMEIRO

const express = require('express');
const cors = require('cors');
const fs = require('fs');
const path = require('path');

const app = express();

// ==========================================
// CONFIGURAÇÕES BÁSICAS
// ==========================================

app.use(cors());

app.use(express.json({ limit: '50mb' }));
app.use(express.urlencoded({
  limit: '50mb',
  extended: true
}));

// ==========================================
// LOG DE REQUISIÇÕES
// ==========================================

app.use((req, res, next) => {
  console.log(`--> ${req.method} ${req.path}`);
  next();
});

// ==========================================
// 📸 PASTA DE UPLOADS
// ==========================================

// Garante que a pasta uploads exista
const uploadsPath = path.join(__dirname, 'uploads');

if (!fs.existsSync(uploadsPath)) {
  fs.mkdirSync(uploadsPath, { recursive: true });
  console.log('📁 Pasta uploads criada:', uploadsPath);
} else {
  console.log('📁 Pasta uploads encontrada:', uploadsPath);
}

// Permite acessar:
// https://seu-backend.com/uploads/nome-da-imagem.jpeg
app.use('/uploads', express.static(uploadsPath));

console.log('📸 Arquivos estáticos configurados em:', uploadsPath);

// ==========================================
// ROTAS
// ==========================================

const authRoutes = require('./routes/login');
const cursosRoutes = require('./routes/cursos');
const turmasRoutes = require('./routes/turmas');
const projetosRoutes = require('./routes/projetos');
const repositorioRoutes = require('./routes/repositorio');
const eventosRoutes = require('./routes/eventos');
const forumRoutes = require('./routes/forum');
const homeRoutes = require('./routes/home');
const professorRoutes = require('./routes/professor');
const topicoRoutes = require('./routes/topico');
const conversaRoutes = require('./routes/conversa');
const perfilRoutes = require('./routes/perfil');
const notificationsRoutes = require('./routes/notifications');

// ==========================================
// REGISTRO DAS ROTAS
// ==========================================

app.use('/login', authRoutes);
app.use('/cursos', cursosRoutes);
app.use('/turmas', turmasRoutes);
app.use('/projetos', projetosRoutes);
app.use('/repositorio', repositorioRoutes);
app.use('/eventos', eventosRoutes);
app.use('/forum', forumRoutes);
app.use('/home', homeRoutes);
app.use('/topico', topicoRoutes);
app.use('/conversa', conversaRoutes);
app.use('/perfil', perfilRoutes);
app.use('/notifications', notificationsRoutes);
app.use('/professor', professorRoutes);

// ==========================================
// ERRO GLOBAL
// ==========================================

app.use((err, req, res, next) => {
  console.error('❌ Erro não tratado:', err.message);
  console.error('📍 Rota:', req.method, req.path);

  res.status(500).json({
    mensagem: 'Erro interno do servidor',
    erro: err.message
  });
});

// ==========================================
// SERVIDOR
// ==========================================

const PORT = process.env.PORT || 3000;

app.listen(PORT, () => {
  console.log(`🚀 Servidor backend rodando na porta ${PORT}`);
});