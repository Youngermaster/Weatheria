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

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

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
