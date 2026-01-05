document.addEventListener("DOMContentLoaded", function () {

    const modal = document.getElementById("modalDescricao");
    const texto = document.getElementById("textoDescricao");
    const fechar = document.querySelector(".fechar-descricao");

    document.querySelectorAll(".icon-descricao").forEach(icon => {
        icon.addEventListener("click", function () {
            const descricao = this.dataset.descricao;

            if (!descricao || descricao.trim() === "") {
                texto.textContent = "Sem descrição cadastrada.";
            } else {
                texto.textContent = descricao;
            }

            modal.style.display = "flex";
        });
    });

    fechar.addEventListener("click", () => {
        modal.style.display = "none";
    });

    modal.addEventListener("click", (e) => {
        if (e.target === modal) {
            modal.style.display = "none";
        }
    });

});

// PESQUISAR

