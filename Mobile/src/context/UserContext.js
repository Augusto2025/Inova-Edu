import React, { createContext, useState, useEffect, useCallback, useMemo } from 'react';
import AsyncStorage from '@react-native-async-storage/async-storage';
import { URL_BASE } from '../config/backend';

export const UserContext = createContext();

export const UserProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [carregando, setCarregando] = useState(true);

  const isValidImageValue = useCallback((value) => {
    return typeof value === 'string' && value.trim() !== '' && value.trim().toLowerCase() !== 'null';
  }, []);

  const normalizeImageUrl = useCallback((value) => {
    if (!isValidImageValue(value)) return null;
    const trimmed = value.trim();
    if (/^https?:\/\//i.test(trimmed)) return trimmed;
    if (/^\/\//.test(trimmed)) return `https:${trimmed}`;
    if (/^\//.test(trimmed)) return `${URL_BASE}${trimmed}`;
    return `https://res.cloudinary.com/dw0pxfap3/${trimmed}`;
  }, [isValidImageValue]);

  const carregarUsuario = useCallback(async () => {
    try {
      setCarregando(true);
      const idSalvo = await AsyncStorage.getItem('idUsuario');

      if (!idSalvo) {
        setUser(null);
        return;
      }

      const response = await fetch(`${URL_BASE}/perfil/${idSalvo}`);
      const textoRaw = await response.text();

      if (!response.ok) {
        throw new Error(`Status ${response.status}`);
      }

      const dados = JSON.parse(textoRaw);

      if (dados.sucesso) {
        const urlCompleta = normalizeImageUrl(dados.usuario.imagem);
        console.log("================================");
        console.log("👤 CARREGAR USUARIO");
        console.log("📦 imagem recebida do backend:", dados.usuario.imagem);
        console.log("🖼️ imagem normalizada:", urlCompleta);
        console.log("================================");

        const novoUser = {
          idUsuario: dados.usuario.idUsuario || idSalvo,
          nome: dados.usuario.nome || "Sem nome",
          sobrenome: dados.usuario.sobrenome || "",
          descricao: dados.usuario.descricao || "Nenhuma descrição informada.",
          imagem: urlCompleta,
          turma: dados.usuario.turma || "Sem Turma Vinculada",
          senha: dados.usuario.senha || ""
        };

        setUser(novoUser);
      } else {
        throw new Error(dados.mensagem || "Erro desconhecido");
      }
    } catch (error) {
      console.error("❌ Erro ao carregar usuário no contexto:", error);
      setUser(null);
    } finally {
      setCarregando(false);
    }
  }, [normalizeImageUrl]);

  // Atualiza dados do usuário após edição
  const atualizarPerfil = useCallback((novosDados) => {
    setUser((prev) => {
      if (!prev) return prev;
      return { ...prev, ...novosDados };
    });
  }, []);
  

  // Atualiza foto especificamente e persiste no estado
  const atualizarFoto = useCallback((urlImagem) => {
    const normalized = normalizeImageUrl(urlImagem);
    setUser((prev) => {
      if (!prev) return prev;
      return { ...prev, imagem: normalized };
    });
  }, [normalizeImageUrl]);

  const value = useMemo(() => ({
    user,
    carregando,
    carregarUsuario,
    atualizarPerfil,
    atualizarFoto
  }), [user, carregando, carregarUsuario, atualizarPerfil, atualizarFoto]);

  useEffect(() => {
    carregarUsuario();
  }, [carregarUsuario]);

  return (
    <UserContext.Provider value={value}>
      {children}
    </UserContext.Provider>
    
  );
};

export const useUser = () => {
  const context = React.useContext(UserContext);
  if (!context) {
    throw new Error('useUser deve ser usado dentro de UserProvider');
  }
  return context;
};
