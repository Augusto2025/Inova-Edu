// ====== MODAL USUÁRIO ======
const abrir = document.getElementById("abrirModal");
const modal = document.getElementById("modalCadastro");
const fechar = document.getElementById("fecharModal");
const cancelar = document.getElementById("cancelarModal");

// Abrir modal
abrir.onclick = function(e) {
    e.preventDefault();
    modal.style.display = "flex";
};

// Fechar modal
fechar.onclick = function() {
    modal.style.display = "none";
};
cancelar.onclick = function() {
    modal.style.display = "none";
};

// Fechar clicando fora do modal
window.onclick = function(e) {
    if (e.target === modal) {
        modal.style.display = "none";
    }
};

// ====== TROCA DE LISTAS ======
function mostrarLista(id) {

    // Esconde todas as listas
    document.querySelectorAll('.lista_conteudo').forEach(lista => {
        lista.style.display = 'none';
    });

    // Mostra a lista clicada
    document.getElementById(id).style.display = 'block';

    // Esconde a imagem inicial
    document.getElementById("painelImagem").style.display = "none";

    const elemento = document.getElementById(id);
    if (elemento) {
        elemento.style.display = 'block';
    }




}

// ====== EDITAR ======
document.addEventListener("DOMContentLoaded", function () {

    const botoesEditar = document.querySelectorAll('.btn-editar');
    const modalEditar = document.getElementById('modalEditar');
    const fecharEditar = document.getElementById('fecharEditar');
    const cancelarEditar = document.getElementById('cancelarEditar');
    const formEditar = document.getElementById('formEditarUsuario');

    botoesEditar.forEach(botao => {
        botao.addEventListener('click', function () {

            modalEditar.style.display = 'flex';

            const li = botao.closest('li');
            if (!li) return;

            const idusuario = li.dataset.id;

            document.getElementById('idusuarioEdit').value = idusuario;
            document.getElementById('nomeEdit').value = li.children[0].textContent;
            document.getElementById('SobrenomeEdit').value = li.children[1].textContent;
            document.getElementById('EmailEdit').value = li.children[2].textContent;

            // descrição via data-descricao (mais seguro)
            const desc = li.querySelector('.icon-descricao');
            document.getElementById('descricaoEdit').value =
                desc ? desc.dataset.descricao : '';

            document.getElementById('tipoCadastroEdit').value =
                li.children[5].textContent.trim();

            formEditar.action = `/usuarios/editar/${idusuario}/`;
        });
    });

    fecharEditar.onclick = () => modalEditar.style.display = 'none';
    cancelarEditar.onclick = () => modalEditar.style.display = 'none';

    window.addEventListener('click', (e) => {
        if (e.target === modalEditar) modalEditar.style.display = 'none';
    });

});



// ===== MODAL CADASTRO CURSO =====
const abrirModalCurso = document.getElementById('abrirModalCurso');
const modalCurso = document.getElementById('modalCadastroCurso');
const fecharModalCurso = document.getElementById('fecharModalCurso');
const cancelarModalCurso = document.getElementById('cancelarModalCurso');

abrirModalCurso.addEventListener('click', function(e) {
    e.preventDefault();
    modalCurso.style.display = 'flex';
});

fecharModalCurso.addEventListener('click', () => {
    modalCurso.style.display = 'none';
});

cancelarModalCurso.addEventListener('click', () => {
    modalCurso.style.display = 'none';
});

window.addEventListener('click', (e) => {
    if (e.target === modalCurso) {
        modalCurso.style.display = 'none';
    }
});

// ===== MODAL EDITAR CURSO =====

document.addEventListener("DOMContentLoaded", function () {

    const modalEditarCurso = document.getElementById("modalEditarCurso");
    const fecharEditarCurso = document.getElementById("fecharEditarCurso");
    const cancelarEditarCurso = document.getElementById("cancelarEditarCurso");

    document.querySelectorAll(".btn-editar-curso").forEach(botao => {
        botao.addEventListener("click", function () {

            document.getElementById("edit_idcurso").value = this.dataset.id;
            document.getElementById("edit_nome_curso").value = this.dataset.nome;
            document.getElementById("edit_data_inicio").value = this.dataset.inicio || "";
            document.getElementById("edit_data_final").value = this.dataset.final || "";
            document.getElementById("edit_descricao_curso").value = this.dataset.descricao || "";

            modalEditarCurso.style.display = "flex";
        });
    });

    fecharEditarCurso.onclick = () => modalEditarCurso.style.display = "none";
    cancelarEditarCurso.onclick = () => modalEditarCurso.style.display = "none";

});



// ===== MODAL TURMA =====
const abrirTurma = document.getElementById("abrirModalTurma");
const modalTurma = document.getElementById("modalCadastroTurma");
const fecharTurma = document.getElementById("fecharModalTurma");
const cancelarTurma = document.getElementById("cancelarModalTurma");

abrirTurma.onclick = function (e) {
    e.preventDefault();
    modalTurma.style.display = "flex";
};

fecharTurma.onclick = function () {
    modalTurma.style.display = "none";
};

cancelarTurma.onclick = function () {
    modalTurma.style.display = "none";
};

window.addEventListener("click", function (e) {
    if (e.target === modalTurma) {
        modalTurma.style.display = "none";
    }
});

// ===== MODAL EDITAR TURMA =====

document.addEventListener("DOMContentLoaded", function () {

    const modal = document.getElementById("modalEditarTurma");
    const fechar = document.getElementById("fecharEditarTurma");
    const cancelar = document.getElementById("cancelarEditarTurma");

    document.querySelectorAll(".btn-editar-turma").forEach(btn => {
        btn.addEventListener("click", function () {

            document.getElementById("idTurmaEdit").value = this.dataset.id;
            document.getElementById("codigoTurmaEdit").value = this.dataset.codigo;
            document.getElementById("turnoEdit").value = this.dataset.turno;
            document.getElementById("anoEdit").value = this.dataset.ano;
            document.getElementById("cursoEdit").value = this.dataset.curso;

            modal.style.display = "flex";
        });
    });

    fechar.onclick = () => modal.style.display = "none";
    cancelar.onclick = () => modal.style.display = "none";

    window.onclick = (e) => {
        if (e.target === modal) modal.style.display = "none";
    };
});




// ===== MODAL USUÁRIOS DA TURMA =====
document.addEventListener("DOMContentLoaded", function () {

    const modal = document.getElementById("modalUsuariosTurma")
    const fechar = document.getElementById("fecharUsuariosTurma")

    const listaBanco = document.getElementById("listaAlunosBanco")
    const listaSelecionados = document.getElementById("listaSelecionados")
    const busca = document.getElementById("buscarAlunoModal")
    const btnSalvar = document.querySelector(".btn-salvar-alunos")

    let alunosSelecionados = []
    let alunosBanco = []
    let turmaAtual = null

    // 🔹 ABRIR MODAL
    document.querySelectorAll(".btn-ver-usuarios").forEach(botao => {
        botao.addEventListener("click", function () {

            turmaAtual = this.dataset.turma

            alunosSelecionados = []
            listaSelecionados.innerHTML = ""

            modal.style.display = "flex"

            carregarAlunos()
        })
    })

    // 🔹 FECHAR MODAL
    fechar.addEventListener("click", () => {
        modal.style.display = "none"
    })

    // 🔹 CARREGAR ALUNOS
    function carregarAlunos() {
        fetch("/listar-alunos/")
            .then(res => res.json())
            .then(data => {
                alunosBanco = data
                renderListaBanco(data)
            })
    }

    // 🔹 LISTA DO BANCO
    function renderListaBanco(alunos) {
        listaBanco.innerHTML = ""

        alunos.forEach(aluno => {

            const li = document.createElement("li")

            li.innerHTML = `
                ${aluno.nome} ${aluno.sobrenome}
                <button class="btn-add"><i class="fa-solid fa-plus"></i></button>
            `

            li.querySelector(".btn-add").addEventListener("click", () => {
                adicionarAluno(aluno.id)
            })

            listaBanco.appendChild(li)
        })
    }

    // 🔹 ADICIONAR
    function adicionarAluno(id) {
        if (!alunosSelecionados.includes(id)) {
            alunosSelecionados.push(id)
            renderSelecionados()
        }
    }

    // 🔹 REMOVER
    function removerAluno(id) {
        alunosSelecionados = alunosSelecionados.filter(a => a !== id)
        renderSelecionados()
    }

    // 🔹 LISTA SELECIONADOS
    function renderSelecionados() {
        listaSelecionados.innerHTML = ""

        alunosSelecionados.forEach(id => {

            const aluno = alunosBanco.find(a => a.id === id)

            const li = document.createElement("li")

            li.innerHTML = `
                ${aluno.nome} ${aluno.sobrenome}
                <button class="btn-remove"><i class="fa-regular fa-trash-can"></i></button>
            `

            li.querySelector(".btn-remove").addEventListener("click", () => {
                removerAluno(id)
            })

            listaSelecionados.appendChild(li)
        })
    }

    // 🔹 BUSCA
    busca.addEventListener("input", function () {

        const valor = this.value.toLowerCase()

        const filtrados = alunosBanco.filter(a =>
            (a.nome + " " + a.sobrenome).toLowerCase().includes(valor)
        )

        renderListaBanco(filtrados)
    })

    // 🔹 SALVAR
    btnSalvar.addEventListener("click", function () {

        console.log("IDs enviados:", alunosSelecionados) // 👈 TESTE

        function getCSRFToken() {
            return document.querySelector('[name=csrfmiddlewaretoken]').value
        }
        fetch("/salvar-alunos-turma/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": getCSRFToken()
            },
            body: JSON.stringify({
                turma: turmaAtual,
                alunos: alunosSelecionados
            })
        })
        .then(res => res.json())
        .then(data => {
            if (data.status === "ok") {
                alert("Alunos salvos com sucesso!")
            } else {
                alert("Erro: " + data.msg)
            }
        })
        .catch(err => {
            console.error("Erro:", err)
        })
    })

})







// ===== MODAL GLOBAL EXCLUIR =====

let formExcluirAtual = null;

const modalExcluir = document.getElementById("modalExcluir");
const confirmarExcluir = document.getElementById("confirmarExcluir");
const cancelarExcluir = document.getElementById("cancelarExcluir");

document.querySelectorAll(".abrir-modal-excluir").forEach(botao => {

    botao.addEventListener("click", function () {

        formExcluirAtual = this.closest("form");

        modalExcluir.style.display = "flex";

    });

});

cancelarExcluir.onclick = function () {
    modalExcluir.style.display = "none";
};

confirmarExcluir.onclick = function () {

    if (formExcluirAtual) {
        formExcluirAtual.submit();
    }

};

window.addEventListener("click", function(e){
    if(e.target === modalExcluir){
        modalExcluir.style.display = "none";
    }
});