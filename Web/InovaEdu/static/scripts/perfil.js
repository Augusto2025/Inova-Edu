// perfil.js
console.log('Script do perfil carregado!');

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
    if (loadingOverlay) loadingOverlay.classList.add('active');
}

function hideLoading() {
    if (loadingOverlay) loadingOverlay.classList.remove('active');
}

function showToast(message, type = 'success') {
    if (!toast || !toastMessage) return;
    
    toastMessage.textContent = message;
    const toastIcon = toast.querySelector('.toast-icon');
    if (toastIcon) {
        toastIcon.className = `toast-icon ${type}`;
    }
    toast.classList.add('show');
    
    setTimeout(() => {
        toast.classList.remove('show');
    }, 3000);
}

// Funções do Perfil
function openProfileModal() {
    console.log('Abrindo modal de perfil');
    const modal = document.getElementById('profile-modal');
    if (modal) {
        modal.classList.add('active');
    } else {
        console.error('Modal de perfil não encontrado');
    }
}

function closeProfileModal() {
    const modal = document.getElementById('profile-modal');
    if (modal) modal.classList.remove('active');
}

async function saveProfile() {
    console.log('=== saveProfile iniciado ===');
    
    const nome = document.getElementById('edit-nome')?.value.trim();
    const sobrenome = document.getElementById('edit-sobrenome')?.value.trim();
    const bio = document.getElementById('edit-bio')?.value.trim();

    console.log('Dados do formulário:', { nome, sobrenome, bio });

    if (!nome || !sobrenome) {
        console.log('Erro: nome ou sobrenome vazio');
        showToast('Nome e sobrenome são obrigatórios!', 'error');
        return;
    }

    showLoading();

    try {
        const url = '/api/atualizar-perfil/';
        console.log('Fazendo POST para:', url);
        console.log('Headers:', headers);
        console.log('Body:', JSON.stringify({ nome, sobrenome, bio }));
        
        const response = await fetch(url, {
            method: 'POST',
            headers: headers,
            body: JSON.stringify({
                nome: nome,
                sobrenome: sobrenome,
                bio: bio
            })
        });

        console.log('Resposta status:', response.status);
        console.log('Resposta headers:', response.headers);
        
        const responseText = await response.text();
        console.log('Resposta texto:', responseText);
        
        let data;
        try {
            data = JSON.parse(responseText);
        } catch (e) {
            console.error('Erro ao parsear JSON:', e);
            console.log('Resposta não é JSON válido');
            showToast('Erro no servidor. Verifique o console.', 'error');
            hideLoading();
            return;
        }

        console.log('Resposta data:', data);

        if (response.ok) {
            const profileName = document.getElementById('profile-name');
            const profileBio = document.getElementById('profile-bio');
            
            if (profileName) profileName.textContent = nome + ' ' + sobrenome;
            if (profileBio) profileBio.textContent = bio || 'Sem descrição cadastrada.';
            
            closeProfileModal();
            showToast('Perfil atualizado com sucesso!');
        } else {
            showToast(data.message || 'Erro ao salvar perfil', 'error');
        }
    } catch (error) {
        console.error('Erro detalhado:', error);
        console.log('Tipo do erro:', error.name);
        console.log('Mensagem:', error.message);
        showToast('Erro ao salvar perfil. Tente novamente.', 'error');
    } finally {
        hideLoading();
    }
}

async function updateProfilePhoto(event) {
    console.log('=== updateProfilePhoto iniciado ===');
    
    const file = event.target.files[0];
    
    if (!file) {
        console.log('Nenhum arquivo selecionado');
        return;
    }
    
    console.log('Arquivo selecionado:', {
        nome: file.name,
        tipo: file.type,
        tamanho: file.size + ' bytes'
    });
    
    if (!file.type.startsWith('image/')) {
        console.log('Tipo de arquivo inválido:', file.type);
        showToast('Por favor, selecione uma imagem válida!', 'error');
        return;
    }
    
    if (file.size > 5 * 1024 * 1024) {
        console.log('Arquivo muito grande:', file.size);
        showToast('A imagem deve ter no máximo 5MB!', 'error');
        return;
    }

    const formData = new FormData();
    formData.append('foto', file);

    console.log('FormData criado');
    for (let pair of formData.entries()) {
        console.log(pair[0] + ': ' + pair[1]);
    }

    showLoading();

    try {
        const url = '/api/upload-foto/';
        console.log('Fazendo POST para:', url);
        
        const response = await fetch(url, {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrftoken
            },
            body: formData
        });

        console.log('Resposta status:', response.status);
        console.log('Resposta headers:', response.headers);
        
        const responseText = await response.text();
        console.log('Resposta texto:', responseText);
        
        let data;
        try {
            data = JSON.parse(responseText);
        } catch (e) {
            console.error('Erro ao parsear JSON:', e);
            showToast('Erro no servidor. Verifique o console.', 'error');
            hideLoading();
            return;
        }

        console.log('Resposta data:', data);

        if (response.ok) {
            const profilePhoto = document.getElementById('profile-photo');
            if (profilePhoto) profilePhoto.src = data.foto_url;
            showToast('Foto atualizada com sucesso!');
            
            // Limpar o input para poder selecionar o mesmo arquivo novamente
            event.target.value = '';
        } else {
            showToast(data.message || 'Erro ao fazer upload da foto', 'error');
        }
    } catch (error) {
        console.error('Erro detalhado:', error);
        showToast('Erro ao fazer upload da foto. Tente novamente.', 'error');
    } finally {
        hideLoading();
    }
}


// Funções de Cursos
let currentCursoId = null;

function openCursoModal() {
    console.log('Abrindo modal de curso');
    currentCursoId = null;
    const modalTitle = document.getElementById('curso-modal-title');
    if (modalTitle) modalTitle.innerHTML = '<i class="fas fa-plus-circle"></i> Adicionar Curso';
    
    document.getElementById('curso-nome').value = '';
    document.getElementById('curso-descricao').value = '';
    document.getElementById('curso-data-inicio').value = '';
    document.getElementById('curso-data-fim').value = '';
    
    const modal = document.getElementById('curso-modal');
    if (modal) modal.classList.add('active');
}

function openEditCursoModal(id, nome, descricao, dataInicio, dataFim) {
    console.log('Abrindo modal de edição de curso:', id);
    currentCursoId = id;
    const modalTitle = document.getElementById('curso-modal-title');
    if (modalTitle) modalTitle.innerHTML = '<i class="fas fa-edit"></i> Editar Curso';
    
    document.getElementById('curso-nome').value = nome || '';
    document.getElementById('curso-descricao').value = descricao || '';
    document.getElementById('curso-data-inicio').value = dataInicio || '';
    document.getElementById('curso-data-fim').value = dataFim || '';
    
    const modal = document.getElementById('curso-modal');
    if (modal) modal.classList.add('active');
}

function closeCursoModal() {
    const modal = document.getElementById('curso-modal');
    if (modal) modal.classList.remove('active');
    currentCursoId = null;
}

async function saveCurso() {
    const nome = document.getElementById('curso-nome')?.value.trim();
    const descricao = document.getElementById('curso-descricao')?.value.trim();
    const dataInicio = document.getElementById('curso-data-inicio')?.value;
    const dataFim = document.getElementById('curso-data-fim')?.value;

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
    console.log('CSRF Token encontrado?', csrftoken ? 'Sim' : 'Não');
    console.log('Modal de perfil:', document.getElementById('profile-modal'));
    console.log('Modal de curso:', document.getElementById('curso-modal'));
});