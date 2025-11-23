import axios from 'axios';
import type {
  MonthlyAverage,
  ExtremeTemperature,
  TemperaturePrecipitation,
  Statistics,
  HealthCheck,
  ApiInfo,
} from '../types';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

console.log('API Base URL:', API_BASE_URL);

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add request interceptor for debugging
api.interceptors.request.use(
  (config) => {
    console.log('Making API request:', config.method?.toUpperCase(), config.url);
    return config;
  },
  (error) => {
    console.error('Request error:', error);
    return Promise.reject(error);
  }
);

// Add response interceptor for debugging
api.interceptors.response.use(
  (response) => {
    console.log('API response received:', response.status, response.config.url);
    return response;
  },
  (error) => {
    console.error('Response error:', error.message, error.config?.url);
    return Promise.reject(error);
  }
);

export const weatheriaApi = {
  // Get API info
  getInfo: async (): Promise<ApiInfo> => {
    const { data } = await api.get<ApiInfo>('/');
    return data;
  },

  // Health check
  getHealth: async (): Promise<HealthCheck> => {
    const { data } = await api.get<HealthCheck>('/health');
    return data;
  },

  // Get monthly averages
  getMonthlyAverages: async (): Promise<MonthlyAverage[]> => {
    const { data } = await api.get<MonthlyAverage[]>('/monthly-avg');
    return data;
  },

  // Get extreme temperatures
  getExtremeTemperatures: async (): Promise<ExtremeTemperature[]> => {
    const { data } = await api.get<ExtremeTemperature[]>('/extreme-temps');
    return data;
  },

  // Get temperature-precipitation correlation
  getTemperaturePrecipitation: async (): Promise<TemperaturePrecipitation[]> => {
    const { data } = await api.get<TemperaturePrecipitation[]>('/temp-precipitation');
    return data;
  },

  // Get statistics
  getStatistics: async (): Promise<Statistics> => {
    const { data } = await api.get<Statistics>('/stats');
    return data;
  },

  // Download results
  downloadResults: async (resultType: 'monthly-avg' | 'extreme-temps' | 'temp-precipitation'): Promise<Blob> => {
    const { data } = await api.get(`/download/${resultType}`, {
      responseType: 'blob',
    });
    return data;
  },
};

export default api;
