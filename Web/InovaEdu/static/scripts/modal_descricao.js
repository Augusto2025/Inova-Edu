document.addEventListener("DOMContentLoaded", function () {
  const modal = document.getElementById("modalDescricao");
  const texto = document.getElementById("textoDescricao");
  const fechar = document.querySelector(".fechar-descricao");

  document.querySelectorAll(".icon-descricao").forEach((icon) => {
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

// PESQUISAR USUARIO

document.addEventListener("DOMContentLoaded", function () {
  const input = document.getElementById("pesquisarUsuario");
  const lista = document.querySelectorAll(".lista-completa ul li");

  input.addEventListener("keyup", function () {
    const valor = input.value.toLowerCase();

    lista.forEach((item, index) => {
      // pula o cabeçalho
      if (item.classList.contains("cabecalho")) return;

      const spans = item.querySelectorAll("span");

      // segurança caso algo mude
      if (spans.length < 3) return;

      const nome = spans[0].textContent.toLowerCase();
      const sobrenome = spans[1].textContent.toLowerCase();
      const email = spans[2].textContent.toLowerCase();

      if (
        nome.includes(valor) ||
        sobrenome.includes(valor) ||
        email.includes(valor)
      ) {
        item.style.display = "";
      } else {
        item.style.display = "none";
      }
    });
  });
});

// PESQUISAR CURSO

document.addEventListener("DOMContentLoaded", function () {
  const inputCurso = document.getElementById("pesquisarCurso");

  if (inputCurso) {
    const listaCursos = document.querySelectorAll(".lista-completa ul li");

    inputCurso.addEventListener("keyup", function () {
      const valor = inputCurso.value.toLowerCase();

      listaCursos.forEach((item) => {
        // ignora o cabeçalho
        if (item.classList.contains("cabecalho")) return;

        const spans = item.querySelectorAll("span");

        // segurança
        if (spans.length < 3) return;

        const nomeCurso = spans[0].textContent.toLowerCase();
        const dataInicio = spans[1].textContent.toLowerCase();
        const dataFinal = spans[2].textContent.toLowerCase();

        if (
          nomeCurso.includes(valor) ||
          dataInicio.includes(valor) ||
          dataFinal.includes(valor)
        ) {
          item.style.display = "";
        } else {
          item.style.display = "none";
        }
      });
    });
  }
});

// PESQUISAR TURMA

document.addEventListener('DOMContentLoaded', function () {


    const inputTurma = document.getElementById('pesquisarTurma');

    if (inputTurma) {
        const listaTurmas = document.querySelectorAll('.lista-completa ul li');

        inputTurma.addEventListener('keyup', function () {
            const valor = inputTurma.value.toLowerCase();

            listaTurmas.forEach(item => {
                // ignora o cabeçalho
                if (item.classList.contains('cabecalho')) return;

                const spans = item.querySelectorAll('span');

                // segurança
                if (spans.length < 4) return;

                const codigo = spans[0].textContent.toLowerCase();
                const turno  = spans[1].textContent.toLowerCase();
                const ano    = spans[2].textContent.toLowerCase();
                const curso  = spans[3].textContent.toLowerCase();

                if (
                    codigo.includes(valor) ||
                    turno.includes(valor) ||
                    ano.includes(valor) ||
                    curso.includes(valor)
                ) {
                    item.style.display = '';
                } else {
                    item.style.display = 'none';
                }
            });
        });
    }

});

// IMG PERFIL

