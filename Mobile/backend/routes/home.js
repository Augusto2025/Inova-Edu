// backend/routes/home.js
const express = require('express');
const router = express.Router();

// A rota deve ser '/' aqui, pois o prefixo '/home' já é definido no server.js
router.get('/', async (req, res) => {
  try {
    // 💡 Estrutura mockada com os campos exatos que a sua HomeScreen.js espera receber do banco.
    // Substitua os arrays vazios pelos seus selects do PostgreSQL quando for integrar o banco de dados.
    const dadosHome = {
      eventos: [
        {
          id: "1",
          title: "Apresentação de TCC - Engenharia",
          date: "2026-06-20", // Formato ISO para o cálculo de status de cores funcionar
          day: "20",
          month: "JUN",
          time: "14:00",
          local: "Auditório Bloco A"
        },
        {
          id: "2",
          title: "Workshop de React Native & Node.js",
          date: "2026-06-25",
          day: "25",
          month: "JUN",
          time: "09:00",
          local: "Laboratório 3"
        }
      ],
      categoriasCursos: [
        {
          idCurso: "c1",
          nomeCurso: "Análise e Desenvolvimento de Sistemas",
          turma: "ADS 2026",
          projetos: [
            {
              id: "p1",
              titulo: "InovaEdu - Repositório Acadêmico",
              imagem: "https://via.placeholder.com/150"
            }
          ]
        }
      ],
      recentesAcessados: [
        {
          id: "p1",
          titulo: "InovaEdu - Repositório Acadêmico",
          imagem: "https://via.placeholder.com/150"
        }
      ]
    };

    // Envia os dados de volta para o aplicativo Mobile
    res.json(dadosHome);

  } catch (error) {
    console.error("❌ Erro na rota /home:", error.message);
    res.status(500).json({ error: 'Erro interno ao carregar os dados da Home' });
  }
});

module.exports = router;