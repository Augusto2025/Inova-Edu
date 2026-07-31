import axios from 'axios';

// Adiciona um valor padrão '|| ""' para evitar chamar .replace em undefined
const rawUrl = process.env.EXPO_PUBLIC_URL_BACKEND || "https://inova-edu-api.onrender.com";
const BASE_URL = rawUrl.replace('/login', '');

export const api = axios.create({
  baseURL: BASE_URL,
});

export const API_ENDPOINTS = {
  login: `${BASE_URL}/login`,
  cursos: `${BASE_URL}/cursos`,
  eventos: `${BASE_URL}/eventos`,
  forum: `${BASE_URL}/forum`,
  perfil: `${BASE_URL}/perfil`,
  turmas: `${BASE_URL}/turmas`,
  projetos: `${BASE_URL}/projetos`,
  repositorio: `${BASE_URL}/repositorio`,
  repositorioSearch: `${BASE_URL}/repositorio/search`,
  home: `${BASE_URL}/home`,
};

export default api;