function salvarSenha(event) {
    event.preventDefault(); // impede o form de recarregar

    const nova = document.getElementById("senha1").value;
    const confirmar = document.getElementById("senha2").value;
    const msg = document.getElementById("mensagem");

    if (nova === "" || confirmar === "") {
        msg.style.display = "block";
        msg.style.color = "red";
        msg.textContent = "❗ Preencha as duas senhas";
        return false;
    }

    if (nova === confirmar) {
        msg.textContent = "✅ Senha salva";
        msg.style.color = "green";
        msg.style.display = "block";
        return true;
    } else {
        msg.textContent = "❌ As senhas não coincidem";
        msg.style.color = "red";
        msg.style.display = "block";
        return false;
    }
}
console.log("JS carregado!");
