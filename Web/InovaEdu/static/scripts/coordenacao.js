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
            document.getElementById("descricaoEdit").value = this.dataset.descricao;
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

            if (correspondePesquisa && correspondeTipo) {
                linha.style.display = "";
            } else {
                linha.style.display = "none";
            }

        });

    }

    pesquisa.addEventListener("input", filtrarUsuarios);
    filtroTipo.addEventListener("change", filtrarUsuarios);

});

