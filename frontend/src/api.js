import axios from 'axios';

const api = axios.create({
  baseURL: '/api'
});

export async function fetchMetric(path) {
  const { data } = await api.get(`/metrics/${path}`);
  return data;
}

export async function askAi(question) {
  const { data } = await api.post('/ai/ask', { question });
  return data;
}
