document.addEventListener('DOMContentLoaded', () => {
    const chatbotIcon = document.getElementById('chatbotIcon');
    const chatBox = document.getElementById('chatBox');
    const sendBtn = document.getElementById('sendBtn');
    const userInput = document.getElementById('userInput');
    const chatBody = document.getElementById('chatBody');

    if (!chatBody) return;

    const initialPredefined = Array.from(chatBody.querySelectorAll('.chat-message'));
    initialPredefined.forEach((el, i) => {
        if (!el.dataset.predefined) {
            el.textContent = `${i + 1}. ${el.textContent.trim()}`;
            el.dataset.predefined = 'true';
        }
    });

    let predefinedMsgs = Array.from(chatBody.querySelectorAll('.chat-message[data-predefined="true"]'));
    let predefinedTexts = [];

    const addClickToPredefined = () => {
        predefinedMsgs = Array.from(chatBody.querySelectorAll('.chat-message[data-predefined="true"]'));
        predefinedTexts = predefinedMsgs.map(el => el.textContent.replace(/^\d+\.\s*/, '').trim());

        predefinedMsgs.forEach((msgEl, idx) => {
            if (msgEl.dataset.listener) return;
            msgEl.style.cursor = 'pointer';
            msgEl.addEventListener('click', () => {
                const msg = predefinedTexts[idx];
                addMessage(msg, 'user');
                botResponse(msg);
            });
            msgEl.dataset.listener = '1';
        });
    };
    addClickToPredefined();

    const clearBtn = document.createElement('button');
    clearBtn.textContent = "Limpar conversa";
    clearBtn.classList.add('clear-btn');
    chatBox.appendChild(clearBtn);

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

    if (chatbotIcon) {
        chatbotIcon.addEventListener('click', () => {
            chatBox.style.display = chatBox.style.display === 'flex' ? 'none' : 'flex';
        });
    }

    window.addEventListener('load', () => {
        const savedChat = localStorage.getItem('chatHistory');
        if (savedChat) {
            chatBody.innerHTML = savedChat;
            // re-numera e reativa cliques nas pré-definidas
            Array.from(chatBody.querySelectorAll('.chat-message')).forEach((el, i) => {
                if (!el.dataset.predefined) {
                    el.textContent = `${i + 1}. ${el.textContent.trim()}`;
                    el.dataset.predefined = 'true';
                }
            });
            addClickToPredefined();
        }
    });

    const sendMessage = () => {
        if (!userInput) return;
        let msg = userInput.value.trim();
        if (!msg) return;

        // se for número puro, mapear para a pergunta pré-definida
        if (/^\d+$/.test(msg)) {
            const idx = parseInt(msg, 10) - 1;
            if (predefinedTexts[idx]) {
                msg = predefinedTexts[idx];
            }
        }

        addMessage(msg, 'user');
        userInput.value = '';
        botResponse(msg);
    };

    if (sendBtn) {
        sendBtn.addEventListener('click', sendMessage);
    }

    if (userInput) {
        userInput.addEventListener('keydown', (e) => {
            if (e.key === 'Enter') {
                e.preventDefault();
                sendMessage();
            }
        });
    }

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
        localStorage.setItem('chatHistory', chatBody.innerHTML);
    }

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

    function removeTyping() {
        const typing = document.getElementById('typing');
        if (typing) typing.remove();
    }

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
            resposta = "Olá! Sou o assistente da Inova Edu. Posso te ajudar a encontrar seus PIs, certificados, eventos ou fórum.";
        }

        showTyping();

        setTimeout(() => {
            removeTyping();
            addMessage(resposta, 'bot');
        }, 1200);
    }

    clearBtn.addEventListener('click', () => {
        const mensagemFixas = Array.from(chatBody.querySelectorAll('.chat-message[data-predefined="true"]'))
            .map(el => el.outerHTML).join('');
        chatBody.innerHTML = mensagemFixas;
        localStorage.removeItem('chatHistory');
        addClickToPredefined();
    });
});