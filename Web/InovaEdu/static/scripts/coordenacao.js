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

// funcionar o modal de editar

// ====== EDITAR USUÁRIO ======
document.addEventListener("DOMContentLoaded", function () {

    const botoesEditar = document.querySelectorAll(".btn-editar");
    const modalEditar = document.getElementById("modalEditar");
    const fecharEditar = document.getElementById("fecharEditar");
    const cancelarEditar = document.getElementById("cancelarEditar");
    const formEditar = document.getElementById("formEditarUsuario");

botoesEditar.forEach(botao => {
    botao.addEventListener("click", function () {

        const li = this.closest("li");
        const idusuario = li.dataset.id;

        document.getElementById("idusuarioEdit").value = idusuario;
        document.getElementById("nomeEdit").value = li.dataset.nome;
        document.getElementById("SobrenomeEdit").value = li.dataset.sobrenome;
        document.getElementById("EmailEdit").value = li.dataset.email;
        document.getElementById("descricaoEdit").value = li.dataset.descricao;
        document.getElementById("tipoCadastroEdit").value = li.dataset.tipo;

        formEditar.action = `/usuarios/editar/${idusuario}/`;

        modalEditar.style.display = "flex";
    });
});

    fecharEditar.onclick = () => modalEditar.style.display = "none";
    cancelarEditar.onclick = () => modalEditar.style.display = "none";

    window.addEventListener("click", function (e) {
        if (e.target === modalEditar) {
            modalEditar.style.display = "none";
        }
    });
});

// FILTRO DOS TIPOS

