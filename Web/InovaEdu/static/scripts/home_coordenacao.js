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
}

// ====== EDITAR ======
const botoesEditar = document.querySelectorAll('.botao-editar');
const modalEditar = document.getElementById('modalEditar');
const fecharEditar = document.getElementById('fecharEditar');
const cancelarEditar = document.getElementById('cancelarEditar');
const formEditar = document.getElementById('formEditarUsuario');

botoesEditar.forEach(botao => {
    botao.addEventListener('click', () => {
        modalEditar.style.display = 'flex';

        const li = botao.closest('li');
        const idusuario = li.dataset.id; // vamos usar um atributo data-id no <li>
        
        document.getElementById('idusuarioEdit').value = idusuario;
        document.getElementById('nomeEdit').value = li.children[0].textContent;
        document.getElementById('SobrenomeEdit').value = li.children[1].textContent;
        document.getElementById('EmailEdit').value = li.children[2].textContent;
        document.getElementById('descricaoEdit').value = li.children[4].textContent;
        document.getElementById('tipoCadastroEdit').value = li.children[6].textContent.toLowerCase();

        // Atualiza a action do form para a URL de edição
        formEditar.action = `/usuarios/editar/${idusuario}/`;
    });
});

fecharEditar.addEventListener('click', () => modalEditar.style.display = 'none');
cancelarEditar.addEventListener('click', () => modalEditar.style.display = 'none');

window.addEventListener('click', (e) => {
    if(e.target == modalEditar) modalEditar.style.display = 'none';
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
