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

    botoesEditar.forEach((botao) => {

        botao.addEventListener("click", function () {

            const idusuario = this.dataset.id;

            document.getElementById("idusuarioEdit").value = idusuario;
            document.getElementById("nomeEdit").value = this.dataset.nome;
            document.getElementById("SobrenomeEdit").value = this.dataset.sobrenome;
            document.getElementById("EmailEdit").value = this.dataset.email;
            // document.getElementById("descricaoEdit").value = this.dataset.descricao;
            document.getElementById("tipoCadastroEdit").value = this.dataset.tipo;

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
// FILTRO DOS USUÁRIOS

document.addEventListener("DOMContentLoaded", function () {

    const pesquisa = document.getElementById("pesquisarUsuario");
    const filtroTipo = document.getElementById("filtroTipo");

    // Se a página não possui os elementos do filtro, não executa o código
    if (!pesquisa || !filtroTipo) {
        return;
    }

    function filtrarUsuarios() {

        const texto = pesquisa.value.toLowerCase().trim();
        const tipo = filtroTipo.value.toLowerCase();

        const linhas = document.querySelectorAll(".tabela-usuarios tbody tr");

        linhas.forEach(function (linha) {

            const nome = linha.cells[1].textContent.toLowerCase();
            const email = linha.cells[2].textContent.toLowerCase();
            const tipoUsuario = linha.cells[3].textContent.toLowerCase().trim();

            const correspondePesquisa =
                nome.includes(texto) ||
                email.includes(texto);

            const correspondeTipo =
                tipo === "" ||
                tipoUsuario === tipo;

            linha.style.display =
                correspondePesquisa && correspondeTipo ? "" : "none";
        });

    }

    pesquisa.addEventListener("input", filtrarUsuarios);
    filtroTipo.addEventListener("change", filtrarUsuarios);

});


// ABRIR A MODAL CADRASTRO DO CURSO

document.addEventListener("DOMContentLoaded", () => {

    const abrirModal = document.getElementById("abrirModalCurso");
    const modal = document.getElementById("modalCadastroCurso");
    const fecharModal = document.getElementById("fecharModalCurso");
    const cancelarModal = document.getElementById("cancelarModalCurso");

    if(abrirModal){

        abrirModal.addEventListener("click", (e)=>{

            e.preventDefault();

            modal.classList.add("abrir");

        });

    }

    if(fecharModal){

        fecharModal.addEventListener("click", ()=>{

            modal.classList.remove("abrir");

        });

    }

    if(cancelarModal){

        cancelarModal.addEventListener("click", ()=>{

            modal.classList.remove("abrir");

        });

    }

    modal.addEventListener("click",(e)=>{

        if(e.target === modal){

            modal.classList.remove("abrir");

        }

    });

});



// EDITAR DO CURSO 
document.addEventListener("DOMContentLoaded", function () {

    const modal = document.getElementById("modalEditarCurso");
    const fechar = document.getElementById("fecharEditarCurso");
    const cancelar = document.getElementById("cancelarEditarCurso");

    document.querySelectorAll(".btn-editar").forEach(botao => {

        botao.addEventListener("click", function () {

            document.getElementById("edit_idcurso").value = this.dataset.id;
            document.getElementById("edit_nome_curso").value = this.dataset.nome;
            document.getElementById("edit_data_inicio").value = this.dataset.inicio;
            document.getElementById("edit_data_final").value = this.dataset.final;
            // document.getElementById("edit_descricao_curso").value = this.dataset.descricao;

            modal.classList.add("active");
        });

    });

    fechar.addEventListener("click", () => {
        modal.classList.remove("active");
    });

    cancelar.addEventListener("click", () => {
        modal.classList.remove("active");
    });

    window.addEventListener("click", function(e){
        if(e.target == modal){
            modal.classList.remove("active");
        }
    });

});



// EXCLUIR BOTÃO USUARIO 

function abrirModalExcluir(id, nome) {
    document.getElementById("textoExcluir").innerHTML =
    `Tem certeza que deseja excluir <strong>${nome}</strong>?`;
    
    document.getElementById("formExcluir").action = `/usuarios/excluir/${id}/`;
    
    document.getElementById("modalExcluir").style.display = "flex";
}

function fecharModalExcluir() {
    document.getElementById("modalExcluir").style.display = "none";
}

window.addEventListener("click", function (e) {
    const modalExcluir = document.getElementById("modalExcluir");
    
    if (e.target === modalExcluir) {
        fecharModalExcluir();
    }
});



// EXCLUIR CURSO

document.addEventListener("DOMContentLoaded", function () {

    const modalExcluir = document.getElementById("modalExcluirCurso");
    const formExcluir = document.getElementById("formExcluirCurso");
    const textoExcluir = document.getElementById("textoExcluirCurso");
    const cancelar = document.getElementById("cancelarExcluirCurso");

    document.querySelectorAll(".abrir-modal-excluir").forEach(botao => {

        botao.addEventListener("click", function () {

            const idCurso = this.dataset.id;
            const nomeCurso = this.dataset.nome;

            textoExcluir.innerHTML =
                `Você tem certeza que deseja excluir o curso <strong>${nomeCurso}</strong>?`;

            formExcluir.action = formExcluir.dataset.url.replace("0", idCurso);

            modalExcluir.style.display = "flex";
        });

    });

    cancelar.addEventListener("click", function () {
        modalExcluir.style.display = "none";
    });

    window.addEventListener("click", function (event) {
        if (event.target === modalExcluir) {
            modalExcluir.style.display = "none";
        }
    });

});