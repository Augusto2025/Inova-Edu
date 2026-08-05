require('dotenv').config();
const { Pool } = require('pg');

console.log("🔍 Verificando URL do banco:", process.env.DATABASE_URL ? "URL encontrada!" : "⚠️ URL ESTÁ INDEFINIDA (UNDEFINED)!");

const pool = new Pool({
  connectionString: process.env.DATABASE_URL,
  ssl: { rejectUnauthorized: false }
});

async function testarConexao() {
  try {
    console.log("⏳ Tentando conectar ao PostgreSQL no Render...");
    const res = await pool.query("SELECT NOW();");
    console.log("✅ CONEXÃO ESTABELECIDA COM SUCESSO!");
    console.log("🕒 Hora no banco de dados:", res.rows[0].now);
  } catch (err) {
    console.error("❌ ERRO CRÍTICO NA CONEXÃO:");
    console.error(err);
  } finally {
    await pool.end();
  }
}

testarConexao();