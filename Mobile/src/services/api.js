import axios from 'axios';

// 1. Define a URL base limpando o '/login' se necessário
const BASE_URL = process.env.EXPO_PUBLIC_URL_BACKEND.replace('/login', '');

// 2. Cria a instância do Axios que você usa para fazer o .get(), .post(), etc.
export const api = axios.create({
  baseURL: BASE_URL,
});

// 3. Mantém os seus endpoints mapeados que você já usa no app
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

// 4. A LINHA MÁGICA QUE FALTAVA: Exporta a instância do axios como padrão
export default api;