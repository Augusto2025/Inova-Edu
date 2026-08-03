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

// ===============================
// PESQUISAR TURMAS
// ===============================

document.addEventListener("DOMContentLoaded", function () {

    const pesquisa = document.getElementById("pesquisarTurma");

    if (!pesquisa) return;

    pesquisa.addEventListener("keyup", function () {

        const texto = this.value.toLowerCase().trim();

        const linhas = document.querySelectorAll(".tabela-turmas tbody tr");

        linhas.forEach(function (linha) {

            const codigo = linha.cells[0].textContent.toLowerCase();
            const turno = linha.cells[1].textContent.toLowerCase();
            const ano = linha.cells[2].textContent.toLowerCase();
            const curso = linha.cells[3].textContent.toLowerCase();
            const professor = linha.cells[4].textContent.toLowerCase();

            if (
                codigo.includes(texto) ||
                turno.includes(texto) ||
                ano.includes(texto) ||
                curso.includes(texto) ||
                professor.includes(texto)
            ) {
                linha.style.display = "";
            } else {
                linha.style.display = "none";
            }

        });

    });

});



// ABRIR O USUARIO DA TURMA
document.addEventListener("DOMContentLoaded", function () {

    const modalUsuarios = document.getElementById("modalUsuariosTurma");
    const btnCancelar = document.getElementById("cancelarUsuariosTurma");

    // Todos os botões de usuários
    document.querySelectorAll(".btn-ver-usuarios").forEach(btn => {

        btn.addEventListener("click", function () {

            // ID da turma clicada
            const turmaId = this.dataset.turma;

            // Usuários da turma (caso queira usar depois)
            let usuarios = [];
            try {
                usuarios = JSON.parse(this.dataset.usuarios);
            } catch (e) {
                console.log("Nenhum usuário encontrado.");
            }

            console.log("Turma:", turmaId);
            console.log("Usuários:", usuarios);

            // Abre a modal
            modalUsuarios.style.display = "flex";
        });

    });

    // Fechar ao clicar em Cancelar
    btnCancelar.addEventListener("click", function () {
        modalUsuarios.style.display = "none";
    });

    // Fechar clicando fora da modal
    window.addEventListener("click", function (e) {
        if (e.target === modalUsuarios) {
            modalUsuarios.style.display = "none";
        }
    });

});

// SELECIONAR OS USUARIOS DA TURMA
let alunosSelecionados = [];

document.querySelectorAll(".btn-add-aluno").forEach(botao => {
    botao.addEventListener("click", function () {

        const li = this.closest("li");
        const id = li.dataset.id;
        const nome = li.querySelector("span").innerText;

        // evita repetir
        if (alunosSelecionados.find(a => a.id == id)) {
            return;
        }

        alunosSelecionados.push({
            id: id,
            nome: nome
        });

        atualizarListaSelecionados();
    });
});

function atualizarListaSelecionados() {

    const lista = document.getElementById("listaSelecionados");
    lista.innerHTML = "";

    alunosSelecionados.forEach((aluno, index) => {

        lista.innerHTML += `
            <li>
                <span>${aluno.nome}</span>

                <button type="button"
                        class="btn-remover"
                        onclick="removerAluno(${index})">
                    <i class="fa-solid fa-xmark"></i>
                </button>
            </li>
        `;
    });

}

function removerAluno(index){
    alunosSelecionados.splice(index,1);
    atualizarListaSelecionados();
}

// ===============================
// SALVAR ALUNOS DA TURMA
// ===============================

document.getElementById("btnSalvar").addEventListener("click", function () {

    const turma = document.getElementById("idTurmaAtual").value;

    fetch("/turma/salvar-alunos/", {

        method:"POST",

        headers:{

            "Content-Type":"application/json",

            "X-CSRFToken":document.querySelector(
                "[name=csrfmiddlewaretoken]"
            ).value

        },

        body:JSON.stringify({

            turma:turma,

            usuarios:alunosSelecionados.map(a=>a.id)

        })

    })

    .then(response=>response.json())

    .then(data=>{

        if(data.status=="ok"){

            document.getElementById("mensagemSucesso").style.display="block";

            setTimeout(()=>{

                document.getElementById("mensagemSucesso").style.display="none";

                document.getElementById("modalUsuariosTurma").style.display="none";

            },1000);

        }

    });

});







// SALVAR OS USUARIOS DA TURMA
// ===============================
// ABRIR MODAL DE USUÁRIOS
// ===============================

document.addEventListener("DOMContentLoaded", function () {

    const modalUsuarios = document.getElementById("modalUsuariosTurma");
    const btnCancelar = document.getElementById("cancelarUsuariosTurma");

    document.querySelectorAll(".btn-ver-usuarios").forEach(btn => {

        btn.addEventListener("click", function () {

            const turmaId = this.dataset.turma;

            // guarda a turma atual
            document.getElementById("idTurmaAtual").value = turmaId;

            // limpa a lista
            alunosSelecionados = [];

            atualizarListaSelecionados();

            // busca os alunos já cadastrados
            fetch(`/turma/listar-alunos/${turmaId}/`)
            .then(response => response.json())
            .then(data => {

                data.alunos.forEach(idAluno => {

                    const li = document.querySelector(
                        `#listaAlunosBanco li[data-id="${idAluno}"]`
                    );

                    if(li){

                        alunosSelecionados.push({
                            id:idAluno,
                            nome:li.querySelector("span").innerText
                        });

                    }

                });

                atualizarListaSelecionados();

            });

            modalUsuarios.style.display = "flex";

        });

    });

    btnCancelar.addEventListener("click",function(){

        modalUsuarios.style.display="none";

    });

    window.addEventListener("click",function(e){

        if(e.target===modalUsuarios){

            modalUsuarios.style.display="none";

        }

    });

});

