import Constants from 'expo-constants';

const envBackend = process.env.EXPO_PUBLIC_URL_BACKEND;
const defaultBackendUrl = 'https://inova-edu-api.onrender.com';

const isLocalBackend = /localhost|127\.0\.0\.1|10\.0\.2\.2|192\.168\./i.test(envBackend || '');

const RAW_BACKEND_URL = isLocalBackend ? defaultBackendUrl : (envBackend || defaultBackendUrl);
const URL_BASE = RAW_BACKEND_URL.replace(/\/login$/, '').replace(/\/$/, '');

export { RAW_BACKEND_URL, URL_BASE };
