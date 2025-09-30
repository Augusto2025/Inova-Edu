const daysContainer = document.getElementById("days");
const monthSelect = document.getElementById("month-select");
const yearSelect = document.getElementById("year-select");

const meses = [
  "Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho",
  "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro",
];

const currentDate = new Date();
let selectedMonth = currentDate.getMonth();
let selectedYear = currentDate.getFullYear();

// Web Desktop
function populateSelects() {
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

      console.log("Mês selecionado:", mes);
      renderCalendar(selectedMonth, selectedYear);
    });

    monthSelect.appendChild(button);
  });

  for (let year = 1900; year <= 2100; year++) {
    const option = document.createElement("option");
    option.value = year;
    option.textContent = year;
    if (year === selectedYear) option.selected = true;
    yearSelect.appendChild(option);
  }
}

function renderEventsOfMonth(month, year) {
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

function renderCalendar(month, year) {
  const firstDay = new Date(year, month, 1);
  const lastDay = new Date(year, month + 1, 0);
  const firstDayIndex = firstDay.getDay();
  const lastDate = lastDay.getDate();

  daysContainer.innerHTML = '';

  const today = new Date();
  const todayDateStr = today.toISOString().split('T')[0];

  for (let i = 0; i < firstDayIndex; i++) {
    const emptyDiv = document.createElement('div');
    daysContainer.appendChild(emptyDiv);
  }

  for (let day = 1; day <= lastDate; day++) {
    const currentDate = new Date(year, month, day);
    const currentDateStr = currentDate.toISOString().split('T')[0];
    const eventosDoDia = eventos.filter(ev => ev.data === currentDateStr);

    const dayDiv = document.createElement('div');
    dayDiv.classList.add('day-box');

    const dayNumber = document.createElement('div');
    dayNumber.textContent = day;
    dayNumber.classList.add('day-number');
    dayDiv.appendChild(dayNumber);

    if (eventosDoDia.length > 0) {
      const dotsContainer = document.createElement('div');
      dotsContainer.classList.add('dots-container');

      eventosDoDia.forEach(ev => {
        const dot = document.createElement('span');
        dot.classList.add('event-dot');

        const dataEvento = new Date(ev.data);

        // 🔹 lógica de cor das bolinhas
        if (currentDateStr === todayDateStr) {
          dot.classList.add('amarelo');   // evento de hoje
        } else if (dataEvento > today) {
          dot.classList.add('verde');     // evento futuro
        } else {
          dot.classList.add('vermelho');  // evento passado
        }

        dot.title = ev.nome;
        dotsContainer.appendChild(dot);
      });

      dayDiv.appendChild(dotsContainer);
    }

    // 👇 Clique no dia → abre só o primeiro evento (lógica antiga)
    dayDiv.addEventListener('click', () => {
      if (eventosDoDia.length > 0) {
        openModal(eventosDoDia[0]); // só o primeiro evento
      }
    });

    daysContainer.appendChild(dayDiv);
  }

  // 👇 além do calendário, renderiza a lista de eventos do mês
  renderEventsOfMonth(month, year);
}

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

// Listeners de selects
monthSelect.addEventListener("change", () => {
  selectedMonth = parseInt(monthSelect.value);
  renderCalendar(selectedMonth, selectedYear);
});

yearSelect.addEventListener("change", () => {
  selectedYear = parseInt(yearSelect.value);
  renderCalendar(selectedMonth, selectedYear);
});

// Fechar modal
document.addEventListener("DOMContentLoaded", () => {
  document.querySelector(".modal-close").addEventListener("click", closeModal);
  document.getElementById("eventModal").addEventListener("click", (e) => {
    if (e.target.id === "eventModal") closeModal();
  });
});

populateSelects();
renderCalendar(selectedMonth, selectedYear);