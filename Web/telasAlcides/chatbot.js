const chatbotIcon = document.getElementById('chatbotIcon');
const chatBox = document.getElementById('chatBox');
const sendBtn = document.getElementById('sendBtn');
const userInput = document.getElementById('userInput');
const chatBody = document.querySelector('.chat-body');
const predefinedMsgs = document.querySelectorAll('.chat-message');

// cria botão "limpar"
const clearBtn = document.createElement('button');
clearBtn.textContent = "🧹 Limpar conversa";
clearBtn.classList.add('clear-btn');
chatBox.appendChild(clearBtn);

// estilo inline pro botão
clearBtn.style.border = "none";
clearBtn.style.background = "#f3f6fa";
clearBtn.style.cursor = "pointer";
clearBtn.style.color = "#0a66c2";
clearBtn.style.padding = "8px";
clearBtn.style.fontWeight = "bold";
clearBtn.style.borderTop = "1px solid #ddd";
clearBtn.style.transition = "background 0.2s";

clearBtn.addEventListener("mouseover", () => clearBtn.style.background = "#e7edf5");
clearBtn.addEventListener("mouseout", () => clearBtn.style.background = "#f3f6fa");

// --- FUNÇÕES PRINCIPAIS ---

// abrir / fechar chat
chatbotIcon.addEventListener('click', () => {
    chatBox.style.display = chatBox.style.display === 'flex' ? 'none' : 'flex';
});

// carregar histórico ao abrir
window.addEventListener('load', () => {
    const savedChat = localStorage.getItem('chatHistory');
    if (savedChat) {
        chatBody.innerHTML = savedChat;
    }
});

// enviar mensagem digitada
sendBtn.addEventListener('click', () => {
    const msg = userInput.value.trim();
    if (msg) {
        addMessage(msg, 'user');
        userInput.value = '';
        botResponse(msg);
    }
});

// clicar em mensagem pré-definida
predefinedMsgs.forEach(msgEl => {
    msgEl.addEventListener('click', () => {
        const msg = msgEl.textContent;
        addMessage(msg, 'user');
        botResponse(msg);
    });
});

// adicionar mensagem ao chat
function addMessage(text, sender = 'bot') {
    const messageDiv = document.createElement('div');
    messageDiv.classList.add('chat-message');

    if (sender === 'user') {
        messageDiv.style.background = '#d0e6ff';
        messageDiv.style.alignSelf = 'flex-end';
    }

    messageDiv.textContent = text;
    chatBody.appendChild(messageDiv);
    chatBody.scrollTop = chatBody.scrollHeight;

    // salvar histórico
    localStorage.setItem('chatHistory', chatBody.innerHTML);
}

// mostrar efeito "digitando..."
function showTyping() {
    const typingDiv = document.createElement('div');
    typingDiv.classList.add('chat-message');
    typingDiv.textContent = "Digitando...";
    typingDiv.style.fontStyle = 'italic';
    typingDiv.style.opacity = '0.7';
    typingDiv.id = "typing";
    chatBody.appendChild(typingDiv);
    chatBody.scrollTop = chatBody.scrollHeight;
}

// remover efeito "digitando..."
function removeTyping() {
    const typing = document.getElementById('typing');
    if (typing) typing.remove();
}

// respostas automáticas do bot
function botResponse(msg) {
    msg = msg.toLowerCase();
    let resposta = "Desculpe, não entendi. Pode reformular sua pergunta?";

    if (msg.includes("pi")) {
        resposta = "Seus PIs estão na seção 'Repositórios'. Lá você pode ver todos os projetos integradores disponíveis.";
    } else if (msg.includes("fórum") || msg.includes("forum")) {
        resposta = "Para acessar o Fórum, clique na aba 'Fórum' no topo da página. Lá você pode interagir com outros alunos.";
    } else if (msg.includes("repositório")) {
        resposta = "Você pode ver seu repositório principal em 'Seu Repositório Atual' na tela inicial.";
    } else if (msg.includes("evento")) {
        resposta = "Os eventos estão disponíveis na aba 'Eventos'.";
    } else if (msg.includes("certificado")) {
        resposta = "Seus certificados ficam disponíveis no seu perfil, na aba 'Certificados'.";
    } else if (msg.includes("ajuda") || msg.includes("suporte")) {
        resposta = "Olá! Sou o assistente da Inova Edu 🤖. Posso te ajudar a encontrar seus PIs, certificados, eventos ou fórum.";
    }

    // mostra "digitando..."
    showTyping();

    // simula tempo de digitação
    setTimeout(() => {
        removeTyping();
        addMessage(resposta, 'bot');
    }, 1200);
}

// botão para limpar conversa
clearBtn.addEventListener('click', () => {
    const mensagemFixas = Array.from(predefinedMsgs).map(el => el.outerHTML).join('');
    chatBody.innerHTML = mensagemFixas;
    localStorage.removeItem('chatHistory');

    // reativar cliques nas perguntas rápidas
    const novasMsgs = chatBody.querySelectorAll('.chat-message');
    novasMsgs.forEach(msgEl => {
        msgEl.addEventListener('click', () => {
            const msg = msgEl.textContent;
            addMessage(msg, 'user');
            botResponse(msg);
        });
    });
});
