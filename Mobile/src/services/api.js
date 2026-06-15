const BASE_URL = process.env.EXPO_PUBLIC_URL_BACKEND.replace('/login', '');

export const API_ENDPOINTS = {
  login: `${BASE_URL}/login`,
  cursos: `${BASE_URL}/cursos`,
  eventos: `${BASE_URL}/eventos`,
  forum: `${BASE_URL}/forum`,
  perfil: `${BASE_URL}/perfil`,
  turmas: `${BASE_URL}/turmas`,
  projetos: `${BASE_URL}/projetos`,
  repositorio: `${BASE_URL}/repositorio`,
};