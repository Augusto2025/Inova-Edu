// ====================================================================
// 📅 NOVO CALENDÁRIO — versão moderna e simplificada
// ====================================================================

// Elementos principais
const daysContainer = document.getElementById("days");
const monthList = document.getElementById("month-list");
const yearDisplay = document.getElementById("year-display");
const eventList = document.getElementById("event-list");
const selectedMonthLabel = document.getElementById("selected-month");

// Modal
const modal = document.getElementById("eventModal");
const modalClose = document.querySelector(".modal-close");

// Dados iniciais
const meses = [
    "Janeiro","Fevereiro","Março","Abril","Maio","Junho",
    "Julho","Agosto","Setembro","Outubro","Novembro","Dezembro"
];

let current = new Date();
let selectedMonth = current.getMonth();
let selectedYear = current.getFullYear();

// ====================================================================
// 🗂️ Criar lista de meses (sidebar)
// ====================================================================
function createMonthList() {
    meses.forEach((mes, index) => {
        const btn = document.createElement("button");
        btn.textContent = mes;
        btn.dataset.mes = index;

        if (index === selectedMonth) btn.classList.add("active");

        btn.addEventListener("click", () => {
            selectedMonth = index;

            document.querySelectorAll(".month-list button")
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
    daysContainer.innerHTML = "";
    selectedMonthLabel.textContent = meses[selectedMonth];

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

        const eventosDoDia = eventos.filter(ev => ev.data === dateStr);

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

            // Criamos as datas para comparação
            const dataEvento = new Date(ev.data);
            const hoje = new Date();

            // Extraímos os componentes para evitar erro de fuso horário
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
// 📝 Renderizar eventos do mês (Ícone de Calendário + Status de Cor)
// ====================================================================
const nomesMesesAbrev = ["JAN", "FEV", "MAR", "ABR", "MAI", "JUN", "JUL", "AGO", "SET", "OUT", "NOV", "DEZ"];

function renderEventsOfMonth() {
    eventList.innerHTML = "";

    const eventosDoMes = eventos.filter(ev => {
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

    // Data atual sem horário
    const hoje = new Date();
    hoje.setHours(0, 0, 0, 0);

    eventosDoMes.forEach(ev => {
        const partesData = ev.data.split('-'); // ["AAAA", "MM", "DD"]
        const ano = parseInt(partesData[0], 10);
        const mes = parseInt(partesData[1], 10) - 1;
        const dia = parseInt(partesData[2], 10);

        const dataEvento = new Date(ano, mes, dia);
        dataEvento.setHours(0, 0, 0, 0);

        // Lógica de cores por status
        let statusClass = "status-green"; // Verde: Agendado

        if (dataEvento.getTime() === hoje.getTime()) {
            statusClass = "status-yellow"; // Amarelo: Hoje
        } else if (dataEvento < hoje) {
            statusClass = "status-red"; // Vermelho: Passou
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
    yearDisplay.textContent = selectedYear;
    renderCalendar();
    renderEventsOfMonth();
}

// Botões de ano
document.getElementById("prev-year").addEventListener("click", () => {
    selectedYear--;
    updateCalendar();
});

document.getElementById("next-year").addEventListener("click", () => {
    selectedYear++;
    updateCalendar();
});

// ====================================================================
// 🔍 Modal de detalhes do evento
// ====================================================================
function openModal(ev) {
    modal.querySelector("#modal-nome").textContent = ev.nome;
    modal.querySelector("#modal-date").textContent = ev.data;
    modal.querySelector("#modal-hour").textContent = ev.hora;
    modal.querySelector("#modal-descricao").textContent = ev.descricao;
    modal.querySelector("#modal-endereco").textContent = ev.endereco;

    const footerBtns = modal.querySelector("#modal-footer-btns");
    const btnExcluir = modal.querySelector("#btn-excluir-evento");
    const btnEditar = modal.querySelector("#btn-editar-evento");

    // 🔒 Verifica se o usuário logado é o dono
    if (ev.dono_email === usuarioLogadoEmail) {
        footerBtns.classList.remove("hidden");
        btnExcluir.href = `/calendario/excluir/${ev.id}/`; // Ajuste sua URL
        
        btnEditar.onclick = () => {
            window.location.href = `/calendario/editar/${ev.id}/`; // Ajuste sua URL
        };
    } else {
        footerBtns.classList.add("hidden");
    }

    modal.classList.remove("hidden");
}

modalClose.addEventListener("click", () => modal.classList.add("hidden"));
modal.addEventListener("click", e => {
    if (e.target === modal) modal.classList.add("hidden");
});

// ====================================================================
// 🚀 Inicialização
// ====================================================================
createMonthList();
updateCalendar();

