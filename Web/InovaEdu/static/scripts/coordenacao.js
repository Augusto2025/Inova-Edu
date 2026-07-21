document.addEventListener("DOMContentLoaded", function () {

    const menuToggle = document.getElementById("menuToggle");
    const navMenu = document.getElementById("navMenu");

    menuToggle.addEventListener("click", function () {
        navMenu.classList.toggle("active");
    });

});


// funcionar o modal de cadastro
document.addEventListener("DOMContentLoaded", function () {

    const abrir = document.getElementById("abrirModal");
    const modal = document.getElementById("modalCadastro");
    const fechar = document.getElementById("fecharModal");
    const cancelar = document.getElementById("cancelarModal");

    if (abrir && modal) {
        abrir.addEventListener("click", function (e) {
            e.preventDefault();
            modal.style.display = "flex";
        });
    }

    if (fechar) {
        fechar.addEventListener("click", function () {
            modal.style.display = "none";
        });
    }

    if (cancelar) {
        cancelar.addEventListener("click", function () {
            modal.style.display = "none";
        });
    }

    window.addEventListener("click", function (e) {
        if (e.target === modal) {
            modal.style.display = "none";
        }
    });

});