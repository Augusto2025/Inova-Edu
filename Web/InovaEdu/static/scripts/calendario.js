// ===============================
// 📅 CALENDÁRIO MÁXIMO (desktop)
// ===============================
const daysContainerMax = document.getElementById("days");
const monthSelectMax = document.getElementById("month-select");
const yearDisplayMax = document.getElementById("year-display");

const meses = [
  "Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho",
  "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro",
];

const currentDate = new Date();
let selectedMonth = currentDate.getMonth();
let selectedYear = currentDate.getFullYear();

function populateSelectsMax() {
  meses.forEach((mes, index) => {
    const button = document.createElement("button");
    button.value = index;
    button.textContent = mes;

    if (index === selectedMonth) {
      button.classList.add("ativo");
    }

    button.addEventListener("click", () => {
      selectedMonth = index;

      document.querySelectorAll("#month-select button")
        .forEach(btn => btn.classList.remove("ativo"));
      button.classList.add("ativo");

      renderCalendarMax(selectedMonth, selectedYear);
    });

    monthSelectMax.appendChild(button);
  });

  yearDisplayMax.textContent = selectedYear;
}

function updateYearDisplayMax() {
  yearDisplayMax.textContent = selectedYear;
}

function decrementYearMax() {
  selectedYear--;
  updateYearDisplayMax();
  renderCalendarMax(selectedMonth, selectedYear);
}

function incrementYearMax() {
  selectedYear++;
  updateYearDisplayMax();
  renderCalendarMax(selectedMonth, selectedYear);
}

document.getElementById("prev-year").addEventListener("click", decrementYearMax);
document.getElementById("next-year").addEventListener("click", incrementYearMax);

function renderEventsOfMonthMax(month, year) {
  const eventsMonthContainer = document.querySelector(".events_mouth");
  eventsMonthContainer.innerHTML = "";

  const eventosDoMes = eventos.filter(ev => {
    const dataEv = new Date(ev.data);
    return dataEv.getMonth() === month && dataEv.getFullYear() === year;
  });

  if (eventosDoMes.length === 0) {
    eventsMonthContainer.innerHTML = "<p>Sem eventos este mês.</p>";
    return;
  }

  eventosDoMes.forEach(ev => {
    const evDiv = document.createElement("div");
    evDiv.classList.add("evento-mes");

    const nomeEl = document.createElement("strong");
    nomeEl.textContent = ev.nome;

    const descEl = document.createElement("p");
    descEl.textContent = ev.descricao;

    const horaEl = document.createElement("p");
    horaEl.textContent = ev.hora;

    evDiv.appendChild(nomeEl);
    evDiv.appendChild(descEl);
    evDiv.appendChild(horaEl);

    eventsMonthContainer.appendChild(evDiv);
  });
}

function renderCalendarMax(month, year) {
  daysContainerMax.innerHTML = "";

  const firstDay = new Date(year, month, 1);
  const lastDay = new Date(year, month + 1, 0);
  const firstDayIndex = firstDay.getDay();
  const lastDate = lastDay.getDate();

  const today = new Date();
  const todayStr = today.toISOString().split('T')[0];

  for (let i = 0; i < firstDayIndex; i++) {
    const emptyDiv = document.createElement('div');
    daysContainerMax.appendChild(emptyDiv);
  }

  for (let d = 1; d <= lastDate; d++) {
    const currentDate = new Date(year, month, d);
    const dateStr = currentDate.toISOString().split('T')[0];
    const eventosDoDia = eventos.filter(ev => ev.data === dateStr);

    const dayBox = document.createElement("div");
    dayBox.classList.add("day-box");

    const dayNumber = document.createElement("div");
    dayNumber.classList.add("day-number");
    dayNumber.textContent = d;
    dayBox.appendChild(dayNumber);

    if (eventosDoDia.length > 0) {
      const dotsContainer = document.createElement("div");
      dotsContainer.classList.add("dots-container");

      eventosDoDia.forEach(ev => {
        const dot = document.createElement("span");
        dot.classList.add("event-dot");

        const dataEvento = new Date(ev.data);
        if (dateStr === todayStr) dot.classList.add("amarelo");
        else if (dataEvento > today) dot.classList.add("verde");
        else dot.classList.add("vermelho");

        dot.title = ev.nome;
        dotsContainer.appendChild(dot);
      });

      dayBox.appendChild(dotsContainer);
    }

    dayBox.addEventListener("click", () => {
      if (eventosDoDia.length > 0) openModal(eventosDoDia[0]);
    });

    daysContainerMax.appendChild(dayBox);
  }

  renderEventsOfMonthMax(month, year);
}

// Modal
function openModal(evento) {
  document.getElementById("modal-nome").textContent = evento.nome;
  document.getElementById("modal-date").textContent = evento.data;
  document.getElementById("modal-hour").textContent = evento.hora;
  document.getElementById("modal-descricao").textContent = evento.descricao;
  document.getElementById("eventModal").style.display = "flex";
}

function closeModal() {
  document.getElementById("eventModal").style.display = "none";
}

document.addEventListener("DOMContentLoaded", () => {
  document.querySelector(".modal-close").addEventListener("click", closeModal);
  document.getElementById("eventModal").addEventListener("click", (e) => {
    if (e.target.id === "eventModal") closeModal();
  });
});

populateSelectsMax();
renderCalendarMax(selectedMonth, selectedYear);


// ===============================
// 📱 CALENDÁRIO MÍNIMO (mobile)
// ===============================
document.addEventListener("DOMContentLoaded", () => {
  const monthSelectMin = document.getElementById("month-select-min");
  const yearSelectMin = document.getElementById("year-select-min");
  const daysContainerMin = document.getElementById("days-min");

  if (!monthSelectMin || !yearSelectMin || !daysContainerMin) return;

  const months = [
    "Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho",
    "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"
  ];

  // Preenche o select de meses
  months.forEach((m, i) => {
    const opt = document.createElement("option");
    opt.value = i;
    opt.textContent = m;
    monthSelectMin.appendChild(opt);
  });

  const currentYear = new Date().getFullYear();

  // Preenche o select de anos
  for (let y = currentYear - 5; y <= currentYear + 5; y++) {
    const opt = document.createElement("option");
    opt.value = y;
    opt.textContent = y;
    if (y === currentYear) opt.selected = true;
    yearSelectMin.appendChild(opt);
  }

  monthSelectMin.value = new Date().getMonth();

  function renderCalendarMin() {
    const month = parseInt(monthSelectMin.value);
    const year = parseInt(yearSelectMin.value);

    daysContainerMin.innerHTML = "";

    const firstDay = new Date(year, month, 1).getDay();
    const totalDays = new Date(year, month + 1, 0).getDate();

    const today = new Date();
    const todayStr = today.toISOString().split("T")[0];

    // Espaços vazios antes do primeiro dia
    for (let i = 0; i < firstDay; i++) {
      const empty = document.createElement("div");
      empty.classList.add("empty");
      daysContainerMin.appendChild(empty);
    }

    // Preenche os dias com as bolinhas de evento
    for (let d = 1; d <= totalDays; d++) {
      const date = new Date(year, month, d);
      const dateStr = date.toISOString().split("T")[0];

      const eventosDoDia = typeof eventos !== "undefined"
        ? eventos.filter(ev => ev.data === dateStr)
        : [];

      const dayBox = document.createElement("div");
      dayBox.classList.add("day-box");

      const dayNumber = document.createElement("div");
      dayNumber.classList.add("day-number");
      dayNumber.textContent = d;

      const dotsContainer = document.createElement("div");
      dotsContainer.classList.add("dots-container");

      eventosDoDia.forEach(ev => {
        const dot = document.createElement("span");
        dot.classList.add("event-dot");
        const dataEvento = new Date(ev.data);

        if (dateStr === todayStr) dot.classList.add("amarelo");
        else if (dataEvento > today) dot.classList.add("verde");
        else dot.classList.add("vermelho");

        dotsContainer.appendChild(dot);
      });

      dayBox.appendChild(dayNumber);
      dayBox.appendChild(dotsContainer);

      // Clique para abrir modal do evento (se existir)
      dayBox.addEventListener("click", () => {
        if (eventosDoDia.length > 0 && typeof openModal === "function") {
          openModal(eventosDoDia[0]);
        }
      });

      daysContainerMin.appendChild(dayBox);
    }
  }

  // Atualiza o calendário quando muda mês ou ano
  monthSelectMin.addEventListener("change", renderCalendarMin);
  yearSelectMin.addEventListener("change", renderCalendarMin);

  // Renderização inicial
  renderCalendarMin();
});



