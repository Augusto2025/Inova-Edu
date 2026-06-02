// server.js (Solto na raiz do backend)
require('dotenv').config(); // 🌟 ISSO AQUI DEVE SER SEMPRE A LINHA 1!

const express = require('express');
const cors = require('cors');

// 1. Importa os arquivos de lógica que estão dentro da pasta routes
const authRoutes = require('./routes/login');

const app = express();
app.use(express.json());
app.use(cors());

// 2. Encaminha as chamadas para os arquivos certos
app.use('/login', authRoutes);   // Tudo sobre login

const PORT = process.env.PORT || 8081;
app.listen(PORT, () => {
  console.log(`Servidor backend rodando na porta ${PORT}`);
});