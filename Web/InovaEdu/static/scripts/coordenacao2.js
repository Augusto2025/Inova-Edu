// MODAL DE CADASTRO DE TURMA



document.addEventListener("DOMContentLoaded", function () {

    const modal = document.getElementById("modalCadastroTurma");
    const abrir = document.getElementById("abrirModalTurma");
    const fechar = document.getElementById("fecharModalTurma");
    const cancelar = document.getElementById("cancelarModalTurma");

    console.log(abrir);
    console.log(modal);

    if (abrir) {
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

});


// EDITAR DA TURMA
document.addEventListener("DOMContentLoaded", function () {

    const modalEditar = document.getElementById("modalEditarTurma");
    const fecharEditar = document.getElementById("fecharEditarTurma");
    const cancelarEditar = document.getElementById("cancelarEditarTurma");

    document.querySelectorAll(".btn-editar-turma").forEach(botao => {

        botao.addEventListener("click", function () {

            // Dados da turma
            document.getElementById("idTurmaEdit").value = this.dataset.id;
            document.getElementById("codigoTurmaEdit").value = this.dataset.codigo;
            document.getElementById("turnoEdit").value = this.dataset.turno;
            document.getElementById("anoEdit").value = this.dataset.ano;
            document.getElementById("cursoEdit").value = this.dataset.curso;

            // Professor da turma
            document.getElementById("professorEdit").value = this.dataset.professor;

            // Abre o modal
            modalEditar.style.display = "flex";
        });

    });

    // Fechar no X
    fecharEditar.addEventListener("click", function () {
        modalEditar.style.display = "none";
    });

    // Fechar no botão Cancelar
    cancelarEditar.addEventListener("click", function () {
        modalEditar.style.display = "none";
    });

    // Fechar clicando fora
    window.addEventListener("click", function (e) {
        if (e.target === modalEditar) {
            modalEditar.style.display = "none";
        }
    });

});


// MENSAGEM
setTimeout(function () {
    const mensagem = document.querySelector(".mensagem-sucesso");

    if (mensagem) {
        mensagem.style.transition = "0.5s";
        mensagem.style.opacity = "0";

        setTimeout(() => {
            mensagem.remove();
        }, 500);
    }
}, 3000);


// BOTÃO EXCLUIR 
document.addEventListener("DOMContentLoaded", function () {

    const modal = document.getElementById("modalExcluirTurma");
    const texto = document.getElementById("textoExcluirTurma");
    const form = document.getElementById("formExcluirTurma");
    const cancelar = document.getElementById("cancelarExcluirTurma");

    console.log("Botões:", document.querySelectorAll(".abrir-modal-excluir-turma"));

    document.querySelectorAll(".abrir-modal-excluir-turma").forEach(botao => {

        botao.addEventListener("click", function () {

            // alert("Clique funcionou!");

            const id = this.dataset.id;
            const codigo = this.dataset.codigo;

            texto.innerHTML =
                `Tem certeza que deseja excluir a turma <strong>${codigo}</strong>?`;

            form.action = form.dataset.url.replace("0", id);

            modal.style.display = "flex";

        });

    });

    if (cancelar) {
        cancelar.addEventListener("click", function () {
            modal.style.display = "none";
        });
    }

});