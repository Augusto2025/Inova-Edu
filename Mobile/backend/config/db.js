// config/db.js
require('dotenv').config(); 
const { Pool } = require('pg');

// O 'pg' lê a URL inteira e faz toda a mágica sozinho por trás dos panos
const pool = new Pool({
  connectionString: process.env.DATABASE_URL,
  ssl: {
    rejectUnauthorized: false // Permite conexões seguras sem precisar de certificados locais
  }
});

// Testa a conexão ao iniciar o servidor
pool.query('SELECT NOW()')
  .then(() => console.log('🚀 Conectado ao PostgreSQL com sucesso usando a DATABASE_URL!'))
  .catch(err => console.error('❌ Erro de conexão com o banco:', err.message));

module.exports = pool;