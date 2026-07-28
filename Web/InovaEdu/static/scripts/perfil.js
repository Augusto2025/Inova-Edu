// perfil.js
console.log('Script do perfil carregado!');

// Pegar o token CSRF
const csrftokenElement = document.getElementById('csrf-token');
const csrftoken = csrftokenElement ? csrftokenElement.value : '';

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

// Helper para travar/destravar botões durante requisições AJAX
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

// =========================
// PERFIL
// =========================

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
    
    const btnSave = document.querySelector('#profile-modal .save-btn') || document.querySelector('#profile-modal button[type="submit"]');
    if (btnSave && btnSave.disabled) return; // Evita duplo clique

    const nome = document.getElementById('edit-nome')?.value.trim();
    const sobrenome = document.getElementById('edit-sobrenome')?.value.trim();
    const bio = document.getElementById('edit-bio')?.value.trim();

    if (!nome || !sobrenome) {
        showToast('Nome e sobrenome são obrigatórios!', 'error');
        return;
    }

    setButtonLoading(btnSave, true, 'Salvando');
    showLoading();

    try {
        const url = '/api/atualizar-perfil/';
        
        const response = await fetch(url, {
            method: 'POST',
            headers: headers,
            body: JSON.stringify({
                nome: nome,
                sobrenome: sobrenome,
                bio: bio
            })
        });

        const responseText = await response.text();
        
        let data;
        try {
            data = JSON.parse(responseText);
        } catch (e) {
            console.error('Erro ao parsear JSON:', e);
            showToast('Erro no servidor. Verifique o console.', 'error');
            return;
        }

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
        showToast('Erro ao salvar perfil. Tente novamente.', 'error');
    } finally {
        setButtonLoading(btnSave, false);
        hideLoading();
    }
}

async function updateProfilePhoto(event) {
    console.log('=== updateProfilePhoto iniciado ===');
    
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

    const formData = new FormData();
    formData.append('foto', file);

    fileInput.disabled = true;
    showLoading();

    try {
        const response = await fetch('/api/upload-foto/', {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrftoken
            },
            body: formData
        });

        const responseText = await response.text();
        let data;
        try {
            data = JSON.parse(responseText);
        } catch (e) {
            console.error('Erro ao parsear JSON:', e);
            showToast('Erro no servidor. Verifique o console.', 'error');
            return;
        }

        if (response.ok) {
            const profilePhoto = document.getElementById('profile-photo');
            if (profilePhoto) profilePhoto.src = data.foto_url;
            showToast('Foto atualizada com sucesso!');
        } else {
            showToast(data.message || 'Erro ao fazer upload da foto', 'error');
        }
    } catch (error) {
        console.error('Erro detalhado:', error);
        showToast('Erro ao fazer upload da foto. Tente novamente.', 'error');
    } finally {
        fileInput.disabled = false;
        fileInput.value = ''; // Limpar input para poder re-selecionar o mesmo arquivo se quiser
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
                nome: nome,
                descricao: descricao,
                data_inicio: dataInicio || null,
                data_final: dataFim || null
            })
        });

        const data = await response.json();

        if (response.ok) {
            showToast(currentCursoId ? 'Curso atualizado com sucesso!' : 'Curso adicionado com sucesso!');
            setTimeout(() => {
                location.reload();
            }, 1200);
        } else {
            showToast(data.message || 'Erro ao salvar curso', 'error');
        }
    } catch (error) {
        console.error('Erro:', error);
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
        console.error(error);
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
    if (modal) modal.style.display = "flex";
}

function closeDeleteModal() {
    const modal = document.getElementById("confirm-delete-modal");
    if (modal) modal.style.display = "none";
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
        console.error(error);
        showToast("Erro ao excluir certificado", "error");
    } finally {
        setButtonLoading(btnDelete, false);
        hideLoading();
    }
}