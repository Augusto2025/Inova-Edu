const toggleSenha = document.getElementById('toggleSenha');
const inputSenha = document.getElementById('senha');

toggleSenha.addEventListener('click', () => {
    const tipo = inputSenha.getAttribute('type');
    if (tipo === 'password') {
        inputSenha.setAttribute('type', 'text');
        toggleSenha.classList.remove('fa-eye');
        toggleSenha.classList.add('fa-eye-slash');
    } else {
        inputSenha.setAttribute('type', 'password');
        toggleSenha.classList.remove('fa-eye-slash');
        toggleSenha.classList.add('fa-eye');
    }
});
