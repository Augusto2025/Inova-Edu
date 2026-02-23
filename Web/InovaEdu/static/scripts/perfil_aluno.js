// Pegar o token CSRF
const csrftoken = document.getElementById('csrf-token').value;

// Configuração para requisições AJAX
const headers = {
    'X-CSRFToken': csrftoken,
    'Content-Type': 'application/json',
};

// Elementos do DOM
const loadingOverlay = document.getElementById('loading-overlay');
const toast = document.getElementById('toast');
const toastMessage = document.getElementById('toast-message');

// Funções de utilidade
function showLoading() {
    loadingOverlay.classList.add('active');
}

function hideLoading() {
    loadingOverlay.classList.remove('active');
}

function showToast(message, type = 'success') {
    toastMessage.textContent = message;
    toast.querySelector('.toast-icon').className = `toast-icon ${type}`;
    toast.classList.add('show');
    
    setTimeout(() => {
        toast.classList.remove('show');
    }, 3000);
}

// Funções do Perfil
function openProfileModal() {
    document.getElementById('profile-modal').classList.add('active');
}

function closeProfileModal() {
    document.getElementById('profile-modal').classList.remove('active');
}

async function saveProfile() {
    const nome = document.getElementById('edit-nome').value.trim();
    const sobrenome = document.getElementById('edit-sobrenome').value.trim();
    const bio = document.getElementById('edit-bio').value.trim();

    if (!nome || !sobrenome) {
        showToast('Nome e sobrenome são obrigatórios!', 'error');
        return;
    }

    showLoading();

    try {
        const response = await fetch('/api/atualizar-perfil/', {
            method: 'POST',
            headers: headers,
            body: JSON.stringify({
                nome: nome,
                sobrenome: sobrenome,
                bio: bio
            })
        });

        const data = await response.json();

        if (response.ok) {
            document.getElementById('profile-name').textContent = nome + ' ' + sobrenome;
            document.getElementById('profile-bio').textContent = bio || 'Sem descrição cadastrada.';
            closeProfileModal();
            showToast('Perfil atualizado com sucesso!');
        } else {
            showToast(data.message || 'Erro ao salvar perfil', 'error');
        }
    } catch (error) {
        console.error('Erro:', error);
        showToast('Erro ao salvar perfil. Tente novamente.', 'error');
    } finally {
        hideLoading();
    }
}

async function updateProfilePhoto(event) {
    const file = event.target.files[0];
    
    if (!file) return;
    
    // Validar tipo de arquivo
    if (!file.type.startsWith('image/')) {
        showToast('Por favor, selecione uma imagem válida!', 'error');
        return;
    }
    
    // Validar tamanho (máximo 5MB)
    if (file.size > 5 * 1024 * 1024) {
        showToast('A imagem deve ter no máximo 5MB!', 'error');
        return;
    }

    const formData = new FormData();
    formData.append('foto', file);

    showLoading();

    try {
        const response = await fetch('/api/upload-foto/', {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrftoken
            },
            body: formData
        });

        const data = await response.json();

        if (response.ok) {
            document.getElementById('profile-photo').src = data.foto_url;
            showToast('Foto atualizada com sucesso!');
        } else {
            showToast(data.message || 'Erro ao fazer upload da foto', 'error');
        }
    } catch (error) {
        console.error('Erro:', error);
        showToast('Erro ao fazer upload da foto. Tente novamente.', 'error');
    } finally {
        hideLoading();
    }
}

// Funções de Cursos
let currentCursoId = null;

function openCursoModal() {
    currentCursoId = null;
    document.getElementById('curso-modal-title').innerHTML = '<i class="fas fa-plus-circle"></i> Adicionar Curso';
    document.getElementById('curso-nome').value = '';
    document.getElementById('curso-descricao').value = '';
    document.getElementById('curso-data-inicio').value = '';
    document.getElementById('curso-data-fim').value = '';
    document.getElementById('curso-modal').classList.add('active');
}

function openEditCursoModal(id, nome, descricao, dataInicio, dataFim) {
    currentCursoId = id;
    document.getElementById('curso-modal-title').innerHTML = '<i class="fas fa-edit"></i> Editar Curso';
    document.getElementById('curso-nome').value = nome;
    document.getElementById('curso-descricao').value = descricao;
    document.getElementById('curso-data-inicio').value = dataInicio || '';
    document.getElementById('curso-data-fim').value = dataFim || '';
    document.getElementById('curso-modal').classList.add('active');
}

function closeCursoModal() {
    document.getElementById('curso-modal').classList.remove('active');
    currentCursoId = null;
}

async function saveCurso() {
    const nome = document.getElementById('curso-nome').value.trim();
    const descricao = document.getElementById('curso-descricao').value.trim();
    const dataInicio = document.getElementById('curso-data-inicio').value;
    const dataFim = document.getElementById('curso-data-fim').value;

    if (!nome) {
        showToast('Por favor, preencha o nome do curso!', 'error');
        return;
    }

    showLoading();

    try {
        const method = currentCursoId ? 'PUT' : 'POST';
        
        const response = await fetch('/api/cursos/', {
            method: method,
            headers: headers,
            body: JSON.stringify({
                id: currentCursoId,
                nome: nome,
                descricao: descricao,
                data_inicio: dataInicio || null,
                data_fim: dataFim || null
            })
        });

        const data = await response.json();

        if (response.ok) {
            showToast(currentCursoId ? 'Curso atualizado com sucesso!' : 'Curso adicionado com sucesso!');
            setTimeout(() => {
                location.reload();
            }, 1500);
        } else {
            showToast(data.message || 'Erro ao salvar curso', 'error');
            hideLoading();
        }
    } catch (error) {
        console.error('Erro:', error);
        showToast('Erro ao salvar curso. Tente novamente.', 'error');
        hideLoading();
    }
}

async function deleteCurso(id) {
    if (!confirm('Tem certeza que deseja excluir este curso?')) {
        return;
    }

    showLoading();

    try {
        const response = await fetch('/api/cursos/', {
            method: 'DELETE',
            headers: headers,
            body: JSON.stringify({ id: id })
        });

        const data = await response.json();

        if (response.ok) {
            showToast('Curso excluído com sucesso!');
            setTimeout(() => {
                location.reload();
            }, 1500);
        } else {
            showToast(data.message || 'Erro ao deletar curso', 'error');
            hideLoading();
        }
    } catch (error) {
        console.error('Erro:', error);
        showToast('Erro ao deletar curso. Tente novamente.', 'error');
        hideLoading();
    }
}

// Funções de Projetos (para atualização dinâmica se necessário)
async function loadProjetos() {
    try {
        const response = await fetch('/api/projetos/');
        const projetos = await response.json();
        renderProjetos(projetos);
    } catch (error) {
        console.error('Erro ao carregar projetos:', error);
    }
}

function renderProjetos(projetos) {
    const grid = document.getElementById('projetos-grid');
    
    if (projetos.length === 0) {
        grid.innerHTML = `
            <div class="no-items">
                <i class="fas fa-folder-open"></i>
                <p>Nenhum projeto encontrado.</p>
            </div>
        `;
        return;
    }
    
    grid.innerHTML = projetos.map(projeto => `
        <div class="repo-card">
            <div class="repo-icon">
                <i class="fas fa-code-branch"></i>
            </div>
            <h3>${projeto.nome}</h3>
            <p class="repo-turma"><i class="fas fa-users"></i> ${projeto.turma}</p>
            <p class="repo-date"><i class="far fa-calendar-alt"></i> Criado em: ${new Date(projeto.data_criacao).toLocaleDateString('pt-BR')}</p>
        </div>
    `).join('');
}

// Fechar modais ao clicar fora
window.addEventListener('click', function(event) {
    const modals = document.querySelectorAll('.modal');
    modals.forEach(modal => {
        if (event.target === modal) {
            modal.classList.remove('active');
        }
    });
});

// Fechar modais com tecla ESC
document.addEventListener('keydown', function(event) {
    if (event.key === 'Escape') {
        const modals = document.querySelectorAll('.modal.active');
        modals.forEach(modal => {
            modal.classList.remove('active');
        });
    }
});

// Inicialização
document.addEventListener('DOMContentLoaded', function() {
    console.log('Perfil carregado com sucesso!');
});