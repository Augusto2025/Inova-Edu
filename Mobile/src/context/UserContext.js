import React, { createContext, useState, useEffect } from 'react';
import AsyncStorage from '@react-native-async-storage/async-storage';

export const UserContext = createContext();

const RAW_BACKEND_URL = process.env.EXPO_PUBLIC_URL_BACKEND || 'https://inova-edu-api.onrender.com';
const URL_BASE = RAW_BACKEND_URL.replace(/\/login$/, '').replace(/\/$/, '');

export const UserProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [carregando, setCarregando] = useState(true);

  // Carrega dados do usuário na primeira vez
  useEffect(() => {
    carregarUsuario();
  }, []);

  const carregarUsuario = async () => {
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
        let urlCompleta = dados.usuario.imagem;

        if (urlCompleta && !urlCompleta.startsWith('http')) {
          urlCompleta = `https://res.cloudinary.com/dw0pxfap3/${urlCompleta}`;
        }

        const novoUser = {
          idUsuario: dados.usuario.idUsuario || idSalvo,
          nome: dados.usuario.nome || "Sem nome",
          sobrenome: dados.usuario.sobrenome || "",
          descricao: dados.usuario.descricao || "Nenhuma descrição informada.",
          imagem: urlCompleta || null,
          turma: dados.usuario.turma || "Sem Turma Vinculada"
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
  };

  // Atualiza dados do usuário após edição
  const atualizarPerfil = (novosDados) => {
    setUser((prev) => {
      if (!prev) return prev;
      return { ...prev, ...novosDados };
    });
  };

  // Atualiza foto especificamente e persiste no estado
  const atualizarFoto = (urlImagem) => {
    setUser((prev) => {
      if (!prev) return prev;
      return { ...prev, imagem: urlImagem };
    });
  };

  const value = {
    user,
    carregando,
    carregarUsuario,
    atualizarPerfil,
    atualizarFoto
  };

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
