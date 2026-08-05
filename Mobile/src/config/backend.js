import Constants from 'expo-constants';

const envBackend = process.env.EXPO_PUBLIC_URL_BACKEND;

function getDevHost() {
  const manifest = Constants.manifest || Constants.expoConfig || {};
  const debuggerHost = manifest.debuggerHost || manifest.hostUri;
  let host = 'localhost';

  if (debuggerHost) {
    host = debuggerHost.split(':')[0];
  }

  const isAndroid = Constants.platform?.android;
  if (host === 'localhost' && isAndroid) {
    return '10.0.2.2';
  }

  return host;
}

const useLocalBackend = process.env.EXPO_USE_LOCAL_BACKEND === 'true';
const devBackendUrl = `http://${getDevHost()}:3000`;
const defaultBackendUrl = __DEV__ ? devBackendUrl : 'https://inova-edu-api.onrender.com';

const RAW_BACKEND_URL = useLocalBackend
  ? devBackendUrl
  : envBackend || defaultBackendUrl;

const URL_BASE = RAW_BACKEND_URL.replace(/\/login$/, '').replace(/\/$/, '');

export { RAW_BACKEND_URL, URL_BASE };
