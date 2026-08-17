document.addEventListener("DOMContentLoaded", function () {

    const track = document.getElementById("carrosselTrack");
    const btnAnterior = document.getElementById("btnAnterior");
    const btnProximo = document.getElementById("btnProximo");
    const indicadores = document.getElementById("carrosselIndicadores");

    if (!track) {
        return;
    }


    const cards = Array.from(
        track.querySelectorAll(".curso-card")
    );


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

            const indicador =
                document.createElement("button");


            indicador.type = "button";


            indicador.className = "indicador";


            indicador.setAttribute(
                "aria-label",
                "Ir para a página " + (i + 1)
            );


            indicador.addEventListener(
                "click",
                function () {

                    paginaAtual = i;

                    atualizarCarrossel();

                    reiniciarCarrossel();

                }
            );


            indicadores.appendChild(indicador);
        }

    }


    /* =========================================
       CALCULAR POSIÇÃO
    ========================================= */

    function calcularPosicao() {

        /*
            Pegamos a largura real do primeiro card.
        */

        const card = cards[0];


        const larguraCard =
            card.getBoundingClientRect().width;


        /*
            Pegamos o gap real do carrossel.
        */

        const estilo =
            window.getComputedStyle(track);


        const gap =
            parseFloat(estilo.columnGap) ||
            parseFloat(estilo.gap) ||
            0;


        const visiveis =
            quantidadeVisivel();


        /*
            Cada página anda a quantidade
            de cards que estão aparecendo.

            Desktop:
            2 cards → anda 2 cards

            Celular:
            1 card → anda 1 card
        */

        const deslocamento =
            paginaAtual *
            visiveis *
            (larguraCard + gap);


        return deslocamento;
    }


    /* =========================================
       ATUALIZAR CARROSSEL
    ========================================= */

    function atualizarCarrossel() {

        const totalPaginas =
            quantidadePaginas();


        /*
            Segurança
        */

        if (paginaAtual >= totalPaginas) {
            paginaAtual = 0;
        }


        if (paginaAtual < 0) {
            paginaAtual =
                totalPaginas - 1;
        }


        /*
            Calcula a posição exata em pixels.
        */

        const posicao =
            calcularPosicao();


        track.style.transform =
            `translateX(-${posicao}px)`;


        /*
            Atualizar indicadores
        */

        if (indicadores) {

            const pontos =
                indicadores.querySelectorAll(
                    ".indicador"
                );


            pontos.forEach(
                function (ponto, indice) {

                    ponto.classList.toggle(
                        "ativo",
                        indice === paginaAtual
                    );

                }
            );

        }


        /*
            Mostrar ou esconder botões
        */

        const visiveis =
            quantidadeVisivel();


        if (cards.length <= visiveis) {

            btnAnterior.style.display = "none";

            btnProximo.style.display = "none";

        } else {

            btnAnterior.style.display = "flex";

            btnProximo.style.display = "flex";

        }

    }


    /* =========================================
       PRÓXIMO
    ========================================= */

    function proximo() {

        const totalPaginas =
            quantidadePaginas();


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

        const totalPaginas =
            quantidadePaginas();


        paginaAtual--;


        if (paginaAtual < 0) {

            paginaAtual =
                totalPaginas - 1;

        }


        atualizarCarrossel();

    }


    /* =========================================
       BOTÃO PRÓXIMO
    ========================================= */

    if (btnProximo) {

        btnProximo.addEventListener(
            "click",
            function () {

                proximo();

                reiniciarCarrossel();

            }
        );

    }


    /* =========================================
       BOTÃO ANTERIOR
    ========================================= */

    if (btnAnterior) {

        btnAnterior.addEventListener(
            "click",
            function () {

                anterior();

                reiniciarCarrossel();

            }
        );

    }


    /* =========================================
       CARROSSEL AUTOMÁTICO
    ========================================= */

    function iniciarCarrossel() {

        clearInterval(intervalo);


        intervalo = setInterval(
            function () {

                proximo();

            },
            5000
        );

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

    const carrossel =
        document.querySelector(".carrossel");


    if (carrossel) {

        carrossel.addEventListener(
            "mouseenter",
            function () {

                clearInterval(intervalo);

            }
        );


        carrossel.addEventListener(
            "mouseleave",
            function () {

                iniciarCarrossel();

            }
        );

    }


    /* =========================================
       RESPONSIVIDADE
    ========================================= */

    let larguraAnterior =
        window.innerWidth;


    window.addEventListener(
        "resize",
        function () {

            const larguraAtual =
                window.innerWidth;


            /*
                Quando muda de:

                desktop → celular

                ou

                celular → desktop

                recalculamos tudo.
            */

            const mudouModo =
                (
                    larguraAnterior <= 768 &&
                    larguraAtual > 768
                ) ||
                (
                    larguraAnterior > 768 &&
                    larguraAtual <= 768
                );


            if (mudouModo) {

                paginaAtual = 0;

                criarIndicadores();

                /*
                    Espera o navegador atualizar
                    as dimensões dos cards.
                */

                setTimeout(
                    function () {

                        atualizarCarrossel();

                    },
                    100
                );

            } else {

                /*
                    Mesmo sem mudar de modo,
                    a largura do card pode mudar.
                */

                atualizarCarrossel();

            }


            larguraAnterior =
                larguraAtual;

        }
    );


    /* =========================================
       INICIALIZAÇÃO
    ========================================= */

    criarIndicadores();


    /*
        Pequeno atraso para garantir que
        imagens e CSS já tenham carregado.
    */

    setTimeout(
        function () {

            atualizarCarrossel();

            iniciarCarrossel();

        },
        100
    );

});