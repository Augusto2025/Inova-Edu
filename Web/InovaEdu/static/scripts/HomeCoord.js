document.addEventListener("DOMContentLoaded", function () {
  /* =====================================================
       BANNER - CARROSSEL DE IMAGENS DE TI
    ===================================================== */

  const banner = document.getElementById("bannerCoord");

  if (banner) {
    const imagensBanner = [
      // 1 - Programação
      "https://images.unsplash.com/photo-1461749280684-dccba630e2f6?auto=format&fit=crop&w=1920&q=80",

      // 2 - Tecnologia / computador
      "https://images.unsplash.com/photo-1518770660439-4636190af475?auto=format&fit=crop&w=1920&q=80",

      // 3 - Tecnologia / segurança
      "https://images.unsplash.com/photo-1550751827-4bd374c3f58b?auto=format&fit=crop&w=1920&q=80",

      // 4 - Desenvolvimento / código
      "https://images.unsplash.com/photo-1515879218367-8466d910aaa4?auto=format&fit=crop&w=1920&q=80",
    ];

    let imagemAtual = 0;

    /*
     * Pré-carrega as imagens.
     */

    imagensBanner.forEach(function (url) {
      const img = new Image();

      img.src = url;
    });

    /*
     * Troca a imagem a cada 5 segundos.
     */

    setInterval(function () {
      imagemAtual++;

      /*
       * Quando chegar na última imagem,
       * volta para a primeira.
       */

      if (imagemAtual >= imagensBanner.length) {
        imagemAtual = 0;
      }

      /*
       * Troca o fundo do banner.
       */

      banner.style.backgroundImage = `
                linear-gradient(
                    110deg,
                    rgba(0, 48, 92, 0.88),
                    rgba(0, 74, 141, 0.72)
                ),
                url("${imagensBanner[imagemAtual]}")
            `;
    }, 5000);
  }

  /* =====================================================
       CARROSSEL DOS PROJETOS
    ===================================================== */

  const track = document.getElementById("carrosselTrack");

  const btnAnterior = document.getElementById("btnAnterior");

  const btnProximo = document.getElementById("btnProximo");

  const indicadores = document.getElementById("carrosselIndicadores");

  if (!track) {
    return;
  }

  const cards = Array.from(track.querySelectorAll(".curso-card"));

  if (cards.length === 0) {
    return;
  }

  let paginaAtual = 0;

  let intervalo = null;

  /* =========================================
       QUANTIDADE DE CARDS VISÍVEIS
    ========================================= */

  function quantidadeVisivel() {
    if (window.innerWidth <= 768) {
      return 1;
    }

    return 2;
  }

  /* =========================================
       QUANTIDADE DE PÁGINAS
    ========================================= */

  function quantidadePaginas() {
    const visiveis = quantidadeVisivel();

    return Math.ceil(cards.length / visiveis);
  }

  /* =========================================
       CRIAR INDICADORES
    ========================================= */

  function criarIndicadores() {
    if (!indicadores) {
      return;
    }

    indicadores.innerHTML = "";

    const totalPaginas = quantidadePaginas();

    for (let i = 0; i < totalPaginas; i++) {
      const indicador = document.createElement("button");

      indicador.type = "button";

      indicador.className = "indicador";

      indicador.setAttribute("aria-label", "Ir para a página " + (i + 1));

      indicador.addEventListener("click", function () {
        paginaAtual = i;

        atualizarCarrossel();

        reiniciarCarrossel();
      });

      indicadores.appendChild(indicador);
    }
  }

  /* =========================================
       CALCULAR POSIÇÃO
    ========================================= */

  function calcularPosicao() {
    const card = cards[0];

    const larguraCard = card.getBoundingClientRect().width;

    const estilo = window.getComputedStyle(track);

    const gap = parseFloat(estilo.columnGap) || parseFloat(estilo.gap) || 0;

    const visiveis = quantidadeVisivel();

    const deslocamento = paginaAtual * visiveis * (larguraCard + gap);

    return deslocamento;
  }

  /* =========================================
       ATUALIZAR CARROSSEL
    ========================================= */

  function atualizarCarrossel() {
    const totalPaginas = quantidadePaginas();

    if (paginaAtual >= totalPaginas) {
      paginaAtual = 0;
    }

    if (paginaAtual < 0) {
      paginaAtual = totalPaginas - 1;
    }

    const posicao = calcularPosicao();

    track.style.transform = `translateX(-${posicao}px)`;

    if (indicadores) {
      const pontos = indicadores.querySelectorAll(".indicador");

      pontos.forEach(function (ponto, indice) {
        ponto.classList.toggle("ativo", indice === paginaAtual);
      });
    }

    const visiveis = quantidadeVisivel();

    if (cards.length <= visiveis) {
      if (btnAnterior) {
        btnAnterior.style.display = "none";
      }

      if (btnProximo) {
        btnProximo.style.display = "none";
      }
    } else {
      if (btnAnterior) {
        btnAnterior.style.display = "flex";
      }

      if (btnProximo) {
        btnProximo.style.display = "flex";
      }
    }
  }

  /* =========================================
       PRÓXIMO
    ========================================= */

  function proximo() {
    const totalPaginas = quantidadePaginas();

    paginaAtual++;

    if (paginaAtual >= totalPaginas) {
      paginaAtual = 0;
    }

    atualizarCarrossel();
  }

  /* =========================================
       ANTERIOR
    ========================================= */

  function anterior() {
    const totalPaginas = quantidadePaginas();

    paginaAtual--;

    if (paginaAtual < 0) {
      paginaAtual = totalPaginas - 1;
    }

    atualizarCarrossel();
  }

  /* =========================================
       BOTÃO PRÓXIMO
    ========================================= */

  if (btnProximo) {
    btnProximo.addEventListener("click", function () {
      proximo();

      reiniciarCarrossel();
    });
  }

  /* =========================================
       BOTÃO ANTERIOR
    ========================================= */

  if (btnAnterior) {
    btnAnterior.addEventListener("click", function () {
      anterior();

      reiniciarCarrossel();
    });
  }

  /* =========================================
       CARROSSEL AUTOMÁTICO
    ========================================= */

  function iniciarCarrossel() {
    clearInterval(intervalo);

    intervalo = setInterval(function () {
      proximo();
    }, 5000);
  }

  /* =========================================
       REINICIAR AUTOMÁTICO
    ========================================= */

  function reiniciarCarrossel() {
    clearInterval(intervalo);

    iniciarCarrossel();
  }

  /* =========================================
       PAUSAR AO PASSAR O MOUSE
    ========================================= */

  const carrossel = document.querySelector(".carrossel");

  if (carrossel) {
    carrossel.addEventListener("mouseenter", function () {
      clearInterval(intervalo);
    });

    carrossel.addEventListener("mouseleave", function () {
      iniciarCarrossel();
    });
  }

  /* =========================================
       RESPONSIVIDADE
    ========================================= */

  let larguraAnterior = window.innerWidth;

  window.addEventListener("resize", function () {
    const larguraAtual = window.innerWidth;

    const mudouModo =
      (larguraAnterior <= 768 && larguraAtual > 768) ||
      (larguraAnterior > 768 && larguraAtual <= 768);

    if (mudouModo) {
      paginaAtual = 0;

      criarIndicadores();

      setTimeout(function () {
        atualizarCarrossel();
      }, 100);
    } else {
      atualizarCarrossel();
    }

    larguraAnterior = larguraAtual;
  });

  /* =========================================
       INICIALIZAÇÃO
    ========================================= */

  criarIndicadores();

  setTimeout(function () {
    atualizarCarrossel();

    iniciarCarrossel();
  }, 100);
});
