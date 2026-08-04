import axios from 'axios';
import { URL_BASE } from '../config/backend';

export const api = axios.create({
  baseURL: URL_BASE,
});

export const API_ENDPOINTS = {
  login: `${URL_BASE}/login`,
  cursos: `${URL_BASE}/cursos`,
  eventos: `${URL_BASE}/eventos`,
  forum: `${URL_BASE}/forum`,
  perfil: `${URL_BASE}/perfil`,
  turmas: `${URL_BASE}/turmas`,
  projetos: `${URL_BASE}/projetos`,
  repositorio: `${URL_BASE}/repositorio`,
  repositorioSearch: `${URL_BASE}/repositorio/search`,
  home: `${URL_BASE}/home`,
};

export default api;