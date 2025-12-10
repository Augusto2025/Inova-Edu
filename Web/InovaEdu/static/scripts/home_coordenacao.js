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
