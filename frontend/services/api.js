import axios from 'axios';
import AsyncStorage from '@react-native-async-storage/async-storage';

const API_BASE = 'http://localhost:4000/api'; // change to your backend host

const client = axios.create({ baseURL: API_BASE });

async function getToken() {
  return await AsyncStorage.getItem('rf_token');
}

// request interceptor to add token
client.interceptors.request.use(async (config) => {
  const token = await getToken();
  if (token) config.headers.Authorization = `Bearer ${token}`;
  return config;
}, (error) => Promise.reject(error));

async function setToken(token) {
  if (token) await AsyncStorage.setItem('rf_token', token);
  else await AsyncStorage.removeItem('rf_token');
}

export default client;
export { setToken, getToken };
