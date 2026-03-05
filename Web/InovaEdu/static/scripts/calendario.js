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
// 📝 Renderizar eventos do mês
// ====================================================================
function renderEventsOfMonth() {
    eventList.innerHTML = "";

    const eventosDoMes = eventos.filter(ev => {
        const dataEv = new Date(ev.data);
        return dataEv.getMonth() === selectedMonth && dataEv.getFullYear() === selectedYear;
    });

    if (eventosDoMes.length === 0) {
        eventList.innerHTML = "<p>Nenhum evento neste mês.</p>";
        return;
    }

    eventosDoMes.forEach(ev => {
        const div = document.createElement("div");
        div.classList.add("event-item");

        div.innerHTML = `
            <p><strong>${ev.nome}</strong></p>
            <p>${ev.descricao}</p>
            <p>${ev.hora}</p>
            <hr>
        `;

        div.addEventListener("click", () => openModal(ev));

        eventList.appendChild(div);
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

