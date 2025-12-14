document.addEventListener('DOMContentLoaded', () => {
    const chatbotIcon = document.getElementById('chatbotIcon');
    const chatBox = document.getElementById('chatBox');
    const chatBody = document.getElementById('chatBody');
    const sendBtn = document.getElementById('sendBtn');
    const userInput = document.getElementById('userInput');

    userInput.placeholder = "Digite uma mensagem ou um número (ex: 1, ?2)";

    /* ABRIR / FECHAR */
    chatbotIcon.addEventListener('click', () => {
        chatBox.style.display = chatBox.style.display === 'flex' ? 'none' : 'flex';
    });

    /* EVENT DELEGATION (CLIQUE) */
    chatBody.addEventListener('click', e => {
        if (!e.target.classList.contains('chat-option')) return;
        handleOption(e.target);
    });

    /* LIMPAR */
    const clearBtn = document.createElement('button');
    clearBtn.textContent = "Limpar conversa";
    clearBtn.className = "clear-btn";
    chatBox.appendChild(clearBtn);

    clearBtn.addEventListener('click', resetOptions);

    function resetOptions() {
        chatBody.innerHTML = `
            <button class="chat-option" data-index="1">Onde estão os meus PI’s?</button>
            <button class="chat-option" data-index="2">Como usar o Fórum?</button>
            <button class="chat-option" data-index="3">Onde eu vejo o meu repositório?</button>
            <button class="chat-option" data-index="4">Como ver os outros PI’s?</button>
            <button class="chat-option" data-index="5">Como ver os eventos?</button>
            <button class="chat-option" data-index="6">Como achar os meus certificados?</button>
        `;
        localStorage.removeItem('chatHistory');
    }

    /* ENVIAR */
    sendBtn.addEventListener('click', sendMessage);
    userInput.addEventListener('keydown', e => {
        if (e.key === 'Enter') sendMessage();
    });

    function sendMessage() {
        let msg = userInput.value.trim();
        if (!msg) return;

        const num = msg.replace('?', '').replace(/^0+/, '');

        if (/^\d+$/.test(num)) {
            const option = chatBody.querySelector(`.chat-option[data-index="${num}"]`);
            if (option) {
                handleOption(option);
                userInput.value = '';
                return;
            }
        }

        addMessage(msg, 'user');
        userInput.value = '';
        botResponse(msg);
    }

    function handleOption(option) {
        option.classList.add('selected');
        setTimeout(() => option.classList.remove('selected'), 200);

        const text = option.textContent.trim();
        addMessage(text, 'user');
        botResponse(text);
    }

    /* MENSAGENS */
    function addMessage(text, sender) {
        const div = document.createElement('div');
        div.className = 'chat-message';
        div.textContent = text;

        if (sender === 'user') {
            div.style.background = '#d0e6ff';
            div.style.alignSelf = 'flex-end';
        }

        chatBody.appendChild(div);
        chatBody.scrollTop = chatBody.scrollHeight;
        localStorage.setItem('chatHistory', chatBody.innerHTML);
    }

    function botResponse(msg) {
        msg = msg.toLowerCase();
        let resposta = "Desculpe, não entendi.";

        if (msg.includes("pi")) resposta = "Seus PIs estão na seção Repositórios.";
        else if (msg.includes("fórum") || msg.includes("forum")) resposta = "O Fórum fica no menu superior.";
        else if (msg.includes("repositório")) resposta = "Seu repositório fica na tela inicial.";
        else if (msg.includes("evento")) resposta = "Os eventos estão na aba Eventos.";
        else if (msg.includes("certificado")) resposta = "Seus certificados estão no seu perfil.";

        setTimeout(() => addMessage(resposta, 'bot'), 700);
    }
});
