// perfil.js

// Pegar o token CSRF
const csrftokenElement = document.getElementById('csrf-token');
const csrftoken = csrftokenElement ? csrftokenElement.value : getCookie('csrftoken');

// Configuração padrão para requisições AJAX JSON
const headers = {
    'X-CSRFToken': csrftoken,
    'Content-Type': 'application/json',
};

// Variáveis de controle de Estado da Foto
let removerFotoFlag = false;
let fotoOriginalUrl = '';

// Elementos Globais do DOM
const loadingOverlay = document.getElementById('loading-overlay');
const toast = document.getElementById('toast');
const toastMessage = document.getElementById('toast-message');

// =========================
// FUNÇÕES UTILITÁRIAS
// =========================

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

function setButtonLoading(btn, isLoading, loadingText = 'Salvar') {
    if (!btn) return;
    if (isLoading) {
        btn.dataset.originalHtml = btn.innerHTML;
        btn.disabled = true;
        btn.innerHTML = `<i class="fas fa-spinner fa-spin"></i> ${loadingText}...`;
    } else {
        btn.disabled = false;
        if (btn.dataset.originalHtml) {
            btn.innerHTML = btn.dataset.originalHtml;
        }
    }
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// =========================
// PERFIL & FOTO DE PERFIL
// =========================

function openProfileModal() {
    const modal = document.getElementById('profile-modal');
    const preview = document.getElementById('edit-profile-photo-preview');
    
    if (preview) {
        fotoOriginalUrl = preview.src;
    }
    
    removerFotoFlag = false;
    if (modal) modal.classList.add('active');
}

function closeProfileModal() {
    const modal = document.getElementById('profile-modal');
    const preview = document.getElementById('edit-profile-photo-preview');
    const inputFoto = document.getElementById('edit-foto-input');
    const checkSenha = document.getElementById('toggle-change-password');
    const passwordFields = document.getElementById('password-fields');

    // Restaura preview original e reseta os campos de senha
    if (preview && fotoOriginalUrl) preview.src = fotoOriginalUrl;
    if (inputFoto) inputFoto.value = '';
    if (checkSenha) checkSenha.checked = false;
    if (passwordFields) passwordFields.style.display = 'none';

    const editSenhaAtual = document.getElementById('edit-senha-atual');
    const editNovaSenha = document.getElementById('edit-nova-senha');
    if (editSenhaAtual) editSenhaAtual.value = '';
    if (editNovaSenha) editNovaSenha.value = '';

    removerFotoFlag = false;

    if (modal) modal.classList.remove('active');
}

function togglePasswordFields() {
    const checkbox = document.getElementById('toggle-change-password');
    const fields = document.getElementById('password-fields');
    if (checkbox && fields) {
        fields.style.display = checkbox.checked ? 'block' : 'none';
        if (!checkbox.checked) {
            const editSenhaAtual = document.getElementById('edit-senha-atual');
            const editNovaSenha = document.getElementById('edit-nova-senha');
            if (editSenhaAtual) editSenhaAtual.value = '';
            if (editNovaSenha) editNovaSenha.value = '';
        }
    }
}

// Preview local da imagem selecionada (sem enviar para o backend ainda)
function updateProfilePhoto(event) {
    const fileInput = event.target;
    const file = fileInput.files[0];
    
    if (!file) return;
    
    if (!file.type.startsWith('image/')) {
        showToast('Por favor, selecione uma imagem válida!', 'error');
        fileInput.value = '';
        return;
    }
    
    if (file.size > 5 * 1024 * 1024) {
        showToast('A imagem deve ter no máximo 5MB!', 'error');
        fileInput.value = '';
        return;
    }

    const reader = new FileReader();
    reader.onload = function(e) {
        const editPreview = document.getElementById('edit-profile-photo-preview');
        if (editPreview) editPreview.src = e.target.result;
    };
    reader.readAsDataURL(file);
    
    removerFotoFlag = false;
}

// Marca a foto para remoção e exibe a imagem padrão temporariamente
function removeProfilePhoto() {
    const editPreview = document.getElementById('edit-profile-photo-preview');
    const inputFoto = document.getElementById('edit-foto-input');
    
    if (editPreview) editPreview.src = '/static/img/default_user.png';
    if (inputFoto) inputFoto.value = '';
    
    removerFotoFlag = true;
}

async function saveProfile() {
    const btnSave = document.querySelector('#profile-modal .save-btn');
    if (btnSave && btnSave.disabled) return;

    const email = document.getElementById('edit-email')?.value.trim();
    const bio = document.getElementById('edit-bio')?.value.trim();
    const querTrocarSenha = document.getElementById('toggle-change-password')?.checked;
    const senhaAtual = document.getElementById('edit-senha-atual')?.value;
    const novaSenha = document.getElementById('edit-nova-senha')?.value;
    const fotoInput = document.getElementById('edit-foto-input');

    if (!email) {
        showToast('O e-mail é obrigatório!', 'error');
        return;
    }

    if (querTrocarSenha && (!senhaAtual || !novaSenha)) {
        showToast('Preencha a senha atual e a nova senha.', 'error');
        return;
    }

    const formData = new FormData();
    formData.append('email', email);
    formData.append('bio', bio);

    // Garante o envio dos campos ocultos de nome e sobrenome para validação do backend
    const nomeInput = document.getElementById('edit-nome');
    const sobrenomeInput = document.getElementById('edit-sobrenome');
    if (nomeInput) formData.append('nome', nomeInput.value);
    if (sobrenomeInput) formData.append('sobrenome', sobrenomeInput.value);

    if (querTrocarSenha) {
        formData.append('senha_atual', senhaAtual);
        formData.append('nova_senha', novaSenha);
    }

    if (removerFotoFlag) {
        formData.append('remover_foto', 'true');
    } else if (fotoInput && fotoInput.files[0]) {
        formData.append('foto', fotoInput.files[0]);
    }

    setButtonLoading(btnSave, true, 'Salvando');
    showLoading();

    try {
        const response = await fetch('/api/atualizar-perfil/', {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrftoken
            },
            body: formData
        });

        const data = await response.json();

        if (response.ok) {
            const profileBio = document.getElementById('profile-bio');
            const profilePhoto = document.getElementById('profile-photo');
            
            if (profileBio) profileBio.textContent = data.bio || 'Sem descrição cadastrada.';
            if (profilePhoto && data.foto_url) profilePhoto.src = data.foto_url;
            
            closeProfileModal();
            showToast(data.message || 'Perfil atualizado com sucesso!');
            setTimeout(() => location.reload(), 1000);
        } else {
            showToast(data.message || 'Erro ao salvar perfil', 'error');
        }
    } catch (error) {
        showToast('Erro ao salvar perfil. Tente novamente.', 'error');
    } finally {
        setButtonLoading(btnSave, false);
        hideLoading();
    }
}

// =========================
// CURSOS
// =========================

let currentCursoId = null;

function openCursoModal() {
    currentCursoId = null;
    const modalTitle = document.getElementById('curso-modal-title');
    if (modalTitle) modalTitle.innerHTML = '<i class="fas fa-plus-circle"></i> Adicionar Curso';
    
    if (document.getElementById('curso-nome')) document.getElementById('curso-nome').value = '';
    if (document.getElementById('curso-descricao')) document.getElementById('curso-descricao').value = '';
    if (document.getElementById('curso-data-inicio')) document.getElementById('curso-data-inicio').value = '';
    if (document.getElementById('curso-data-fim')) document.getElementById('curso-data-fim').value = '';
    
    const modal = document.getElementById('curso-modal');
    if (modal) modal.classList.add('active');
}

function openEditCursoModal(id, nome, descricao, dataInicio, dataFim) {
    currentCursoId = id;
    const modalTitle = document.getElementById('curso-modal-title');
    if (modalTitle) modalTitle.innerHTML = '<i class="fas fa-edit"></i> Editar Curso';
    
    if (document.getElementById('curso-nome')) document.getElementById('curso-nome').value = nome || '';
    if (document.getElementById('curso-descricao')) document.getElementById('curso-descricao').value = descricao || '';
    if (document.getElementById('curso-data-inicio')) document.getElementById('curso-data-inicio').value = dataInicio || '';
    if (document.getElementById('curso-data-fim')) document.getElementById('curso-data-fim').value = dataFim || '';
    
    const modal = document.getElementById('curso-modal');
    if (modal) modal.classList.add('active');
}

function closeCursoModal() {
    const modal = document.getElementById('curso-modal');
    if (modal) modal.classList.remove('active');
    currentCursoId = null;
}

async function saveCurso() {
    const btnSave = document.querySelector('#curso-modal .save-btn') || document.querySelector('#curso-modal button[type="submit"]');
    if (btnSave && btnSave.disabled) return;

    const nome = document.getElementById('curso-nome')?.value.trim();
    const descricao = document.getElementById('curso-descricao')?.value.trim();
    const dataInicio = document.getElementById('curso-data-inicio')?.value;
    const dataFim = document.getElementById('curso-data-fim')?.value;

    if (!nome) {
        showToast('Por favor, preencha o nome do curso!', 'error');
        return;
    }

    setButtonLoading(btnSave, true, 'Salvar');
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
                data_final: dataFim || null
            })
        });

        const data = await response.json();

        if (response.ok) {
            showToast(currentCursoId ? 'Curso atualizado com sucesso!' : 'Curso adicionado com sucesso!');
            setTimeout(() => location.reload(), 1200);
        } else {
            showToast(data.message || 'Erro ao salvar curso', 'error');
        }
    } catch (error) {
        showToast('Erro ao salvar curso. Tente novamente.', 'error');
    } finally {
        setButtonLoading(btnSave, false);
        hideLoading();
    }
}

// =========================
// CERTIFICADOS
// =========================

let currentCertificadoId = null;
let certificadoParaExcluir = null;

function openCertificadoModal() {
    currentCertificadoId = null;

    if (document.getElementById("certificado-nome")) document.getElementById("certificado-nome").value = "";
    if (document.getElementById("certificado-descricao")) document.getElementById("certificado-descricao").value = "";
    if (document.getElementById("certificado-data-inicio")) document.getElementById("certificado-data-inicio").value = "";
    if (document.getElementById("certificado-data-fim")) document.getElementById("certificado-data-fim").value = "";

    const titleElem = document.getElementById("certificado-modal-title");
    if (titleElem) {
        titleElem.innerHTML = '<i class="fas fa-plus-circle"></i> Adicionar Certificado';
    }

    const modal = document.getElementById("certificado-modal");
    if (modal) modal.classList.add("active");
}

function closeCertificadoModal() {
    const modal = document.getElementById("certificado-modal");
    if (modal) modal.classList.remove("active");
}

function openEditCertificadoModal(id, nome, descricao, inicio, fim) {
    currentCertificadoId = id;

    if (document.getElementById("certificado-nome")) document.getElementById("certificado-nome").value = nome || "";
    if (document.getElementById("certificado-descricao")) document.getElementById("certificado-descricao").value = descricao || "";
    if (document.getElementById("certificado-data-inicio")) document.getElementById("certificado-data-inicio").value = inicio || "";
    if (document.getElementById("certificado-data-fim")) document.getElementById("certificado-data-fim").value = fim || "";

    const titleElem = document.getElementById("certificado-modal-title");
    if (titleElem) {
        titleElem.innerHTML = '<i class="fas fa-edit"></i> Editar Certificado';
    }

    const modal = document.getElementById("certificado-modal");
    if (modal) modal.classList.add("active");
}

async function saveCertificado() {
    const btnSave = document.querySelector('#certificado-modal .save-btn') || document.querySelector('#certificado-modal button[type="submit"]');
    if (btnSave && btnSave.disabled) return;

    const nome = document.getElementById("certificado-nome")?.value.trim();
    const descricao = document.getElementById("certificado-descricao")?.value.trim();
    const dataInicio = document.getElementById("certificado-data-inicio")?.value;
    const dataFim = document.getElementById("certificado-data-fim")?.value;

    if (!nome) {
        showToast("Digite o nome do certificado", "error");
        return;
    }

    setButtonLoading(btnSave, true, 'Salvando');
    showLoading();

    try {
        const response = await fetch("/api/certificados/", {
            method: "POST",
            headers: headers,
            body: JSON.stringify({
                id: currentCertificadoId,
                nome: nome,
                descricao: descricao,
                data_inicio: dataInicio,
                data_final: dataFim
            })
        });

        const data = await response.json();

        if (response.ok) {
            showToast("Certificado salvo!");
            setTimeout(() => location.reload(), 1200);
        } else {
            showToast(data.message || "Erro ao salvar certificado", "error");
        }

    } catch (error) {
        showToast("Erro ao salvar certificado", "error");
    } finally {
        setButtonLoading(btnSave, false);
        hideLoading();
    }
}

function openDeleteModal(id, nome) {
    certificadoParaExcluir = id;
    const nameElem = document.getElementById("certificado-nome-delete");
    if (nameElem) nameElem.innerText = nome;

    const modal = document.getElementById("confirm-delete-modal");
    if (modal) modal.classList.add("active");
}

function closeDeleteModal() {
    const modal = document.getElementById("confirm-delete-modal");
    if (modal) modal.classList.remove("active");
    certificadoParaExcluir = null;
}

async function confirmDeleteCertificado() {
    if (!certificadoParaExcluir) return;

    const btnDelete = document.querySelector('#confirm-delete-modal .delete-btn') || document.querySelector('#confirm-delete-modal button[type="submit"]');
    if (btnDelete && btnDelete.disabled) return;

    setButtonLoading(btnDelete, true, 'Excluindo');
    showLoading();

    try {
        const response = await fetch("/api/certificados/", {
            method: "DELETE",
            headers: headers,
            body: JSON.stringify({
                id: certificadoParaExcluir
            })
        });

        const data = await response.json();

        if (response.ok) {
            showToast("Certificado excluído!");
            closeDeleteModal();
            setTimeout(() => location.reload(), 1000);
        } else {
            showToast(data.message || "Erro ao excluir", "error");
        }

    } catch (error) {
        showToast("Erro ao excluir certificado", "error");
    } finally {
        setButtonLoading(btnDelete, false);
        hideLoading();
    }
}

// =========================
// EVENT LISTENERS GLOBAIS
// =========================

window.addEventListener('click', function(event) {
    if (event.target.classList.contains('modal')) {
        event.target.classList.remove('active');
    }
});

window.addEventListener('keydown', function(event) {
    if (event.key === 'Escape') {
        document.querySelectorAll('.modal.active').forEach(modal => {
            modal.classList.remove('active');
        });
    }
});