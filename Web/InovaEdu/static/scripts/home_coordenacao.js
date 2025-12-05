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
    // Esconder todas as listas
    document.querySelectorAll('.lista_conteudo').forEach(l => l.style.display = 'none');

    // Mostrar a lista clicada
    const lista = document.getElementById(id);
    if(lista){
        lista.style.display = 'block';
    }
}


// cadastro usuario ================
