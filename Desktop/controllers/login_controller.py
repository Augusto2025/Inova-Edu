from models.login_model import LoginUsuario
import traceback

def autenticar(user, senha, tipo):
    print(f"[CONTROLLER] Autenticando {user}")
    try:
        print("[CONTROLLER] Buscando usuarios...")
        usuarios = LoginUsuario().exibir_usuarios()
        print(f"[CONTROLLER] {len(usuarios)} usuarios carregados")
    except Exception as e:
        print(f"[CONTROLLER ERRO] {str(e)}")
        return (f"Erro ao acessar banco: {str(e)}", False)
    
    try:
        for email_user, senha_user, tipo_user in usuarios:
            if user == email_user:
                if senha == senha_user:
                    print(f"[CONTROLLER] Sucesso para {user}")
                    return (tipo_user, True)
                else:
                    print(f"[CONTROLLER] Senha errada para {user}")
                    return ("Senha incorreta.", False)
        
        print(f"[CONTROLLER] Email nao encontrado: {user}")
        return ("Email nao encontrado.", False)
    except Exception as e:
        print(f"[CONTROLLER ERRO] {str(e)}")
        return (f"Erro: {str(e)}", False)