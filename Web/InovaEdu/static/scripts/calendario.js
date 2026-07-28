// ====================================================================
// 📅 NOVO CALENDÁRIO — Versão moderna e assíncrona (AJAX)
// ====================================================================

// Funções utilitárias (CSRF Token para Django)
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
const csrftoken = getCookie('csrftoken');

// Elementos principais
const daysContainer = document.getElementById("days");
const monthList = document.getElementById("month-list");
const yearDisplay = document.getElementById("year-display");
const eventList = document.getElementById("event-list");
const selectedMonthLabel = document.getElementById("selected-month");

// Modal de Eventos
const modal = document.getElementById("eventModal");

// Estado do sistema
let current = new Date();
let selectedMonth = current.getMonth();
let selectedYear = current.getFullYear();
let currentEvent = null; // Armazena o evento selecionado no modal

const meses = [
    "Janeiro","Fevereiro","Março","Abril","Maio","Junho",
    "Julho","Agosto","Setembro","Outubro","Novembro","Dezembro"
];

const nomesMesesAbrev = ["JAN", "FEV", "MAR", "ABR", "MAI", "JUN", "JUL", "AGO", "SET", "OUT", "NOV", "DEZ"];

// ====================================================================
// 🗂️ Criar lista de meses (sidebar)
// ====================================================================
function createMonthList() {
    if (!monthList) return;
    monthList.innerHTML = "";

    meses.forEach((mes, index) => {
        const btn = document.createElement("button");
        btn.textContent = mes;
        btn.dataset.mes = index;

        if (index === selectedMonth) btn.classList.add("active");

        btn.addEventListener("click", () => {
            selectedMonth = index;

            document.querySelectorAll("#month-list button")
                .forEach(el => el.classList.remove("active"));

            btn.classList.add("active");
            updateCalendar();
        });

        monthList.appendChild(btn);
    });
}

// ====================================================================
// 🗓️ Renderizar Calendário
// ====================================================================
function renderCalendar() {
    if (!daysContainer) return;
    daysContainer.innerHTML = "";
    if (selectedMonthLabel) selectedMonthLabel.textContent = meses[selectedMonth];

    const firstDay = new Date(selectedYear, selectedMonth, 1).getDay();
    const lastDay = new Date(selectedYear, selectedMonth + 1, 0).getDate();
    const todayStr = new Date().toISOString().split("T")[0];

    // Espaços vazios antes do primeiro dia
    for (let i = 0; i < firstDay; i++) {
        const empty = document.createElement("div");
        daysContainer.appendChild(empty);
    }

    // Dias do mês
    for (let d = 1; d <= lastDay; d++) {
        const date = new Date(selectedYear, selectedMonth, d);
        const dateStr = date.toISOString().split("T")[0];

        // Filtra eventos no array global 'eventos'
        const eventosDoDia = (typeof eventos !== 'undefined' ? eventos : []).filter(ev => ev.data === dateStr);

        const day = document.createElement("div");
        day.classList.add("day-box");

        const number = document.createElement("div");
        number.textContent = d;
        number.classList.add("day-number");

        if (dateStr === todayStr) day.classList.add("today");

        const dots = document.createElement("div");
        dots.classList.add("dots-container");

        eventosDoDia.forEach(ev => {
            const dot = document.createElement("span");
            dot.classList.add("dot");

            const dataEvento = new Date(ev.data);
            const hoje = new Date();

            const mesmoDia = dataEvento.getUTCDate() === hoje.getDate() &&
                            dataEvento.getUTCMonth() === hoje.getMonth() &&
                            dataEvento.getUTCFullYear() === hoje.getFullYear();

            if (mesmoDia) {
                dot.classList.add("yellow");
            } else if (dataEvento < hoje) {
                dot.classList.add("red");
            } else {
                dot.classList.add("green");
            }

            dots.appendChild(dot);
        });

        day.appendChild(number);
        day.appendChild(dots);

        day.addEventListener("click", () => {
            if (eventosDoDia.length > 0) openModal(eventosDoDia[0]);
            renderEventsOfMonth(); 
        });

        daysContainer.appendChild(day);
    }
}

// ====================================================================
// 📝 Renderizar lista de eventos do mês
// ====================================================================
function renderEventsOfMonth() {
    if (!eventList) return;
    eventList.innerHTML = "";

    const listaEventos = typeof eventos !== 'undefined' ? eventos : [];

    const eventosDoMes = listaEventos.filter(ev => {
        const partesData = ev.data.split('-');
        const anoEv = parseInt(partesData[0], 10);
        const mesEv = parseInt(partesData[1], 10) - 1;

        return mesEv === selectedMonth && anoEv === selectedYear;
    });

    if (eventosDoMes.length === 0) {
        eventList.innerHTML = `
            <div class="card-vazio estado-vazio-animado">
                <div class="icone animar-esvaziado">📅</div>
                <p>Nenhum evento agendado para este mês.</p>
            </div>
        `;
        return;
    }

    const hoje = new Date();
    hoje.setHours(0, 0, 0, 0);

    eventosDoMes.forEach(ev => {
        const partesData = ev.data.split('-');
        const ano = parseInt(partesData[0], 10);
        const mes = parseInt(partesData[1], 10) - 1;
        const dia = parseInt(partesData[2], 10);

        const dataEvento = new Date(ano, mes, dia);
        dataEvento.setHours(0, 0, 0, 0);

        let statusClass = "status-green";
        if (dataEvento.getTime() === hoje.getTime()) {
            statusClass = "status-yellow";
        } else if (dataEvento < hoje) {
            statusClass = "status-red";
        }

        const diaFormatado = partesData[2];
        const mesAbrev = nomesMesesAbrev[mes];
        const dataExibicao = `${partesData[2]}/${partesData[1]}/${partesData[0]}`;
        const horaFormatada = ev.hora ? ev.hora.substring(0, 5) : "--:--";

        const card = document.createElement("div");
        card.classList.add("card-evento", statusClass);

        card.innerHTML = `
            <div class="data-evento-icone">
                <div class="topo-calendario">
                    <span class="mes">${mesAbrev}</span>
                </div>
                <div class="corpo-calendario">
                    <span class="dia">${diaFormatado}</span>
                </div>
            </div>
            <div class="info-evento">
                <h3>${ev.nome || 'Evento sem nome'}</h3>
                <p>📅 ${dataExibicao}</p>
                <p>🕒 ${horaFormatada}</p>
                <p class="endereco">📍 ${ev.endereco || 'Local não informado'}</p>
            </div>
        `;

        card.addEventListener("click", () => openModal(ev));
        eventList.appendChild(card);
    });
}

// ====================================================================
// 📆 Atualizar mês/ano
// ====================================================================
function updateCalendar() {
    if (yearDisplay) yearDisplay.textContent = selectedYear;
    renderCalendar();
    renderEventsOfMonth();
}

// Navegação de anos
document.getElementById("prev-year")?.addEventListener("click", () => {
    selectedYear--;
    updateCalendar();
});

document.getElementById("next-year")?.addEventListener("click", () => {
    selectedYear++;
    updateCalendar();
});

// ====================================================================
// 🔍 Gerenciamento do Modal de Detalhes
// ====================================================================
function openModal(ev) {
    if (!modal) return;
    currentEvent = ev;

    modal.querySelector("#modal-nome").textContent = ev.nome || "Evento sem título";
    modal.querySelector("#modal-date").textContent = ev.data || "--";
    modal.querySelector("#modal-hour").textContent = ev.hora || "--:--";
    modal.querySelector("#modal-descricao").textContent = ev.descricao || "Sem descrição";
    modal.querySelector("#modal-endereco").textContent = ev.endereco || "Não informado";

    const footerBtns = modal.querySelector("#modal-footer-btns");

    const emailUsuarioLogado = typeof usuarioLogadoEmail !== 'undefined' ? usuarioLogadoEmail : '';
    if (ev.dono_email === emailUsuarioLogado) {
        footerBtns.classList.remove("hidden");
    } else {
        footerBtns.classList.add("hidden");
    }

    modal.classList.remove("hidden");
}

function closeEventModal() {
    if (modal) modal.classList.add("hidden");
    currentEvent = null;
}

if (modal) {
    modal.addEventListener("click", e => {
        if (e.target === modal) closeEventModal();
    });
}

function openEditEventModal() {
    if (!currentEvent) return;
    const eventoId = currentEvent.ideventos || currentEvent.id;
    window.location.href = `/calendario/editar/${eventoId}/`;
}

async function confirmDeleteEvent() {
    if (!currentEvent) return;

    const eventoId = currentEvent.ideventos || currentEvent.id;

    if (!eventoId) {
        if (typeof showToast === 'function') showToast('Erro: ID do evento não encontrado.', 'error');
        return;
    }

    // 🚫 A caixa de confirmação nativa do navegador foi removida daqui!

    const btnDelete = document.getElementById("btn-excluir-evento");
    if (!btnDelete || btnDelete.disabled) return;

    const originalText = btnDelete.innerHTML;
    btnDelete.disabled = true;
    btnDelete.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Excluindo...';

    try {
        const response = await fetch(`/calendario/excluir/${eventoId}/`, {
            method: 'DELETE',
            headers: {
                'X-CSRFToken': csrftoken,
                'Content-Type': 'application/json'
            }
        });

        let data = {};
        try {
            data = await response.json();
        } catch (e) {
            // Ignora silenciosamente
        }

        if (response.ok) {
            if (typeof eventos !== 'undefined' && Array.isArray(eventos)) {
                const index = eventos.findIndex(e => (e.ideventos || e.id) == eventoId);
                if (index !== -1) {
                    eventos.splice(index, 1);
                }
            }

            if (typeof showToast === 'function') {
                showToast('Evento excluído com sucesso!');
            }

            closeEventModal();
            updateCalendar();
        } else {
            const msg = data.message || `Erro no servidor (Código ${response.status})`;
            if (typeof showToast === 'function') showToast(msg, 'error');
        }
    } catch (error) {
        if (typeof showToast === 'function') showToast('Erro de conexão ou ao atualizar a tela.', 'error');
    } finally {
        btnDelete.disabled = false;
        btnDelete.innerHTML = originalText;
    }
}

// ====================================================================
// 🚀 Inicialização
// ====================================================================
createMonthList();
updateCalendar();