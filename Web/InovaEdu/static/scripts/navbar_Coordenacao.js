document.addEventListener("DOMContentLoaded", function () {

    /* ==========================================
       ELEMENTOS
    ========================================== */

    const menuToggle = document.getElementById("menuToggle");
    const mobileMenu = document.getElementById("mobileMenu");
    const closeMenu = document.getElementById("closeMenu");
    const menuOverlay = document.getElementById("menuOverlay");


    /* ==========================================
       ABRIR MENU
    ========================================== */

    function abrirMenu() {

        mobileMenu.classList.add("active");

        menuOverlay.classList.add("active");

        document.body.style.overflow = "hidden";

        menuToggle.setAttribute(
            "aria-label",
            "Fechar menu"
        );

    }


    /* ==========================================
       FECHAR MENU
    ========================================== */

    function fecharMenu() {

        mobileMenu.classList.remove("active");

        menuOverlay.classList.remove("active");

        document.body.style.overflow = "";

        menuToggle.setAttribute(
            "aria-label",
            "Abrir menu"
        );

    }


    /* ==========================================
       BOTÃO ☰
    ========================================== */

    menuToggle.addEventListener("click", function () {

        if (mobileMenu.classList.contains("active")) {

            fecharMenu();

        } else {

            abrirMenu();

        }

    });


    /* ==========================================
       BOTÃO X
    ========================================== */

    closeMenu.addEventListener("click", function () {

        fecharMenu();

    });


    /* ==========================================
       CLICAR NO FUNDO ESCURO
    ========================================== */

    menuOverlay.addEventListener("click", function () {

        fecharMenu();

    });


    /* ==========================================
       TECLA ESC
    ========================================== */

    document.addEventListener("keydown", function (event) {

        if (event.key === "Escape") {

            if (mobileMenu.classList.contains("active")) {

                fecharMenu();

            }

        }

    });


    /* ==========================================
       LINKS DO MENU MOBILE
       
       Ao clicar no link, o navegador vai
       normalmente para a URL Django.
    ========================================== */

    const mobileLinks =
        document.querySelectorAll(".mobile-nav-menu a");


    mobileLinks.forEach(function (link) {

        link.addEventListener("click", function () {

            fecharMenu();

        });

    });


    /* ==========================================
       LINK SAIR
    ========================================== */

    const sairLink =
        document.querySelector(".mobile-sair a");


    if (sairLink) {

        sairLink.addEventListener("click", function () {

            fecharMenu();

        });

    }

});