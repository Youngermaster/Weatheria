import { useEffect, useState } from 'react';
import { Card } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Download, AlertTriangle, Snowflake, Sun, Check } from 'lucide-react';
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
  PieChart,
  Pie,
  Cell,
} from 'recharts';
import { weatheriaApi } from '@/services/api';
import type { ExtremeTemperature } from '@/types';

const COLORS = {
  very_hot: '#ef4444',
  hot: '#f59e0b',
  normal: '#10b981',
  cool: '#3b82f6',
  very_cool: '#6366f1',
};

const CATEGORY_INFO = {
  very_hot: {
    icon: Sun,
    label: 'Very Hot',
    description: 'Maximum temperature > 30°C',
    color: 'text-red-600',
  },
  normal: {
    icon: Check,
    label: 'Normal',
    description: 'Temperature within 15-30°C range',
    color: 'text-green-600',
  },
  cool: {
    icon: Snowflake,
    label: 'Cool',
    description: 'Minimum temperature < 15°C',
    color: 'text-blue-600',
  },
  very_cool: {
    icon: AlertTriangle,
    label: 'Very Cool',
    description: 'Minimum temperature < 12°C',
    color: 'text-indigo-600',
  },
};

export function ExtremeAnalysis() {
  const [data, setData] = useState<ExtremeTemperature[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const extreme = await weatheriaApi.getExtremeTemperatures();
        setData(extreme);
      } catch (error) {
        console.error('Error fetching extreme data:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  const handleDownload = async () => {
    try {
      const blob = await weatheriaApi.downloadResults('extreme-temps');
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = 'extreme_temps_results.csv';
      document.body.appendChild(a);
      a.click();
      window.URL.revokeObjectURL(url);
      document.body.removeChild(a);
    } catch (error) {
      console.error('Error downloading file:', error);
    }
  };

  if (loading) {
    return (
      <div className="flex h-full items-center justify-center">
        <div className="text-center">
          <div className="h-12 w-12 animate-spin rounded-full border-4 border-primary border-t-transparent mx-auto" />
          <p className="mt-4 text-muted-foreground">Loading extreme temperature data...</p>
        </div>
      </div>
    );
  }

  const totalDays = data.reduce((sum, item) => sum + item.count, 0);

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-3xl font-bold tracking-tight">Extreme Temperature Analysis</h2>
          <p className="text-muted-foreground">
            Classification of days by temperature extremes
          </p>
        </div>
        <Button onClick={handleDownload} className="gap-2">
          <Download className="h-4 w-4" />
          Download Data
        </Button>
      </div>

      {/* Category Cards */}
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
        {data.map((item) => {
          const info = CATEGORY_INFO[item.category as keyof typeof CATEGORY_INFO];
          if (!info) return null;
          const Icon = info.icon;
          const percentage = ((item.count / totalDays) * 100).toFixed(1);

          return (
            <Card key={item.category} className="p-6">
              <div className="flex items-start justify-between">
                <div className="flex-1">
                  <div className="flex items-center gap-2">
                    <Icon className={`h-5 w-5 ${info.color}`} />
                    <h3 className="font-semibold">{info.label}</h3>
                  </div>
                  <p className="mt-2 text-3xl font-bold">{item.count}</p>
                  <p className="text-sm text-muted-foreground">{percentage}% of days</p>
                  <p className="mt-2 text-xs text-muted-foreground">
                    Avg: {item.avg_temp.toFixed(1)}°C
                  </p>
                </div>
              </div>
            </Card>
          );
        })}
      </div>

      {/* Charts Grid */}
      <div className="grid gap-6 md:grid-cols-2">
        {/* Distribution Bar Chart */}
        <Card className="p-6">
          <h3 className="mb-6 text-lg font-semibold">Day Count by Category</h3>
          <ResponsiveContainer width="100%" height={350}>
            <BarChart data={data}>
              <CartesianGrid strokeDasharray="3 3" className="stroke-muted" />
              <XAxis dataKey="category" className="text-xs" />
              <YAxis className="text-xs" />
              <Tooltip
                contentStyle={{
                  backgroundColor: 'hsl(var(--card))',
                  border: '1px solid hsl(var(--border))',
                  borderRadius: '0.5rem'
                }}
              />
              <Legend />
              <Bar dataKey="count" fill="#3b82f6" name="Number of Days" />
            </BarChart>
          </ResponsiveContainer>
        </Card>

        {/* Distribution Pie Chart */}
        <Card className="p-6">
          <h3 className="mb-6 text-lg font-semibold">Temperature Distribution</h3>
          <ResponsiveContainer width="100%" height={350}>
            <PieChart>
              <Pie
                data={data}
                cx="50%"
                cy="50%"
                labelLine={false}
                label={({ category, count, percent }) => {
                  const info = CATEGORY_INFO[category as keyof typeof CATEGORY_INFO];
                  return `${info?.label || category}: ${count} (${(percent * 100).toFixed(0)}%)`;
                }}
                outerRadius={120}
                fill="#8884d8"
                dataKey="count"
              >
                {data.map((entry) => (
                  <Cell
                    key={`cell-${entry.category}`}
                    fill={COLORS[entry.category as keyof typeof COLORS] || '#8884d8'}
                  />
                ))}
              </Pie>
              <Tooltip
                contentStyle={{
                  backgroundColor: 'hsl(var(--card))',
                  border: '1px solid hsl(var(--border))',
                  borderRadius: '0.5rem'
                }}
              />
            </PieChart>
          </ResponsiveContainer>
        </Card>
      </div>

      {/* Insights */}
      <Card className="p-6">
        <h3 className="mb-4 text-lg font-semibold">Key Insights</h3>
        <div className="space-y-4">
          {data.map((item) => {
            const info = CATEGORY_INFO[item.category as keyof typeof CATEGORY_INFO];
            if (!info) return null;
            const percentage = ((item.count / totalDays) * 100).toFixed(1);

            return (
              <div key={item.category} className="flex items-start gap-4 rounded-lg border p-4">
                <Badge variant={item.category === 'normal' ? 'default' : 'secondary'}>
                  {percentage}%
                </Badge>
                <div className="flex-1">
                  <h4 className="font-semibold">{info.label}</h4>
                  <p className="text-sm text-muted-foreground">{info.description}</p>
                  <p className="mt-2 text-sm">
                    <span className="font-medium">{item.count} days</span> with an average temperature of{' '}
                    <span className="font-medium">{item.avg_temp.toFixed(1)}°C</span>
                  </p>
                </div>
              </div>
            );
          })}
        </div>
      </Card>
    </div>
  );
}
