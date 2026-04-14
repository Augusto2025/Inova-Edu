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
            <button class="chat-option" data-index="5">Onde Posso ver os eventos desse mês?</button>
            <button class="chat-option" data-index="6">Como achar as minhas informações de usuário?</button>
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

        if (msg.includes("pi")) resposta = "Caminho para seus PI’s: Seu Cursos > Sua Turmas > Seu Projeto Integrador.\nAqui você pode acessar os detalhes, enviar arquivos e acompanhar o progresso do seu projeto.";
        else if (msg.includes("fórum") || msg.includes("forum")) resposta = "Primeiro, acesse a aba Fórum. Lá, você pode escolher entre os diferentes fóruns disponíveis para cada curso ou turma. Para participar, basta clicar no fórum desejado, ler as regras de participação e começar a interagir com os outros alunos e instrutores. Você pode criar novos tópicos, responder a perguntas existentes e compartilhar recursos relacionados ao curso.";
        else if (msg.includes("repositório")) resposta = "Assim como para acessar seus PI’s, vá para Seu Cursos > Sua Turmas > Seu Projeto Integrador. Dentro do seu projeto, você encontrará uma seção dedicada ao repositório, onde pode acessar os PIs dos outros alunos.";
        else if (msg.includes("evento")) resposta = "Para ver os eventos do mês, vá para a aba Eventos. Lá, você encontrará uma lista de eventos programados, como webinars, workshops e sessões de Q&A. Você pode clicar em cada evento para obter mais detalhes, como data, hora e descrição. Se estiver interessado em participar, basta ir a coordenação para se inscrever ou obter o link de acesso.";
        else if (msg.includes("certificado")) resposta = "As suas informações de usuário, incluindo certificados, estão na aba Perfil. Lá, você pode acessar seus certificados de conclusão, histórico de cursos e outras informações pessoais relacionadas à sua conta.";

        setTimeout(() => addMessage(resposta, 'bot'), 700);
    }
});
