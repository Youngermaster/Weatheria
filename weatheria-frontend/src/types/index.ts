// API Response Types
export interface MonthlyAverage {
  month: string;
  avg_max: number;
  avg_min: number;
}

export interface ExtremeTemperature {
  category: string;
  count: number;
  avg_temp: number;
}

export interface TemperaturePrecipitation {
  month: string;
  correlation: number;
  avg_temp: number;
  avg_precip: number;
  rainy_days: number;
  total_precip: number;
}

export interface Statistics {
  total_months_analyzed: number;
  max_temperature: number;
  min_temperature: number;
  overall_avg_max: number;
  overall_avg_min: number;
}

export interface HealthCheck {
  status: string;
  version: string;
}

export interface ApiInfo {
  message: string;
  description: string;
  version: string;
  inspiration: string;
  endpoints: Record<string, string>;
  documentation: {
    swagger: string;
    redoc: string;
  };
}
