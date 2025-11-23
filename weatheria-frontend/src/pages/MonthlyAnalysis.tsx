import { useEffect, useState } from 'react';
import { Card } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Download } from 'lucide-react';
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
  AreaChart,
  Area,
} from 'recharts';
import { weatheriaApi } from '@/services/api';
import type { MonthlyAverage } from '@/types';

export function MonthlyAnalysis() {
  const [data, setData] = useState<MonthlyAverage[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const monthly = await weatheriaApi.getMonthlyAverages();
        setData(monthly);
      } catch (error) {
        console.error('Error fetching monthly data:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  const handleDownload = async () => {
    try {
      const blob = await weatheriaApi.downloadResults('monthly-avg');
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = 'monthly_avg_results.csv';
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
          <p className="mt-4 text-muted-foreground">Loading monthly analysis...</p>
        </div>
      </div>
    );
  }

  const hottestMonth = data.reduce((max, item) =>
    item.avg_max > max.avg_max ? item : max, data[0]
  );
  const coolestMonth = data.reduce((min, item) =>
    item.avg_min < min.avg_min ? item : min, data[0]
  );

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-3xl font-bold tracking-tight">Monthly Temperature Analysis</h2>
          <p className="text-muted-foreground">
            Detailed monthly temperature trends across 36 months
          </p>
        </div>
        <Button onClick={handleDownload} className="gap-2">
          <Download className="h-4 w-4" />
          Download Data
        </Button>
      </div>

      {/* Summary Cards */}
      <div className="grid gap-4 md:grid-cols-2">
        <Card className="p-6">
          <h3 className="text-sm font-medium text-muted-foreground">Hottest Month</h3>
          <p className="mt-2 text-3xl font-bold">{hottestMonth?.month}</p>
          <p className="text-sm text-muted-foreground">
            Max: {hottestMonth?.avg_max.toFixed(1)}°C | Min: {hottestMonth?.avg_min.toFixed(1)}°C
          </p>
        </Card>
        <Card className="p-6">
          <h3 className="text-sm font-medium text-muted-foreground">Coolest Month</h3>
          <p className="mt-2 text-3xl font-bold">{coolestMonth?.month}</p>
          <p className="text-sm text-muted-foreground">
            Max: {coolestMonth?.avg_max.toFixed(1)}°C | Min: {coolestMonth?.avg_min.toFixed(1)}°C
          </p>
        </Card>
      </div>

      {/* Temperature Trends Chart */}
      <Card className="p-6">
        <h3 className="mb-6 text-lg font-semibold">Temperature Trends Over Time</h3>
        <ResponsiveContainer width="100%" height={400}>
          <AreaChart data={data}>
            <defs>
              <linearGradient id="colorMax" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor="#ef4444" stopOpacity={0.8} />
                <stop offset="95%" stopColor="#ef4444" stopOpacity={0.1} />
              </linearGradient>
              <linearGradient id="colorMin" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor="#3b82f6" stopOpacity={0.8} />
                <stop offset="95%" stopColor="#3b82f6" stopOpacity={0.1} />
              </linearGradient>
            </defs>
            <CartesianGrid strokeDasharray="3 3" className="stroke-muted" />
            <XAxis
              dataKey="month"
              className="text-xs"
            />
            <YAxis className="text-xs" label={{ value: 'Temperature (°C)', angle: -90, position: 'insideLeft' }} />
            <Tooltip
              contentStyle={{
                backgroundColor: 'hsl(var(--card))',
                border: '1px solid hsl(var(--border))',
                borderRadius: '0.5rem'
              }}
            />
            <Legend />
            <Area
              type="monotone"
              dataKey="avg_max"
              stroke="#ef4444"
              fillOpacity={1}
              fill="url(#colorMax)"
              name="Maximum Temperature (°C)"
            />
            <Area
              type="monotone"
              dataKey="avg_min"
              stroke="#3b82f6"
              fillOpacity={1}
              fill="url(#colorMin)"
              name="Minimum Temperature (°C)"
            />
          </AreaChart>
        </ResponsiveContainer>
      </Card>

      {/* Data Table */}
      <Card className="p-6">
        <h3 className="mb-4 text-lg font-semibold">Monthly Data Table</h3>
        <div className="overflow-x-auto">
          <table className="w-full text-sm">
            <thead>
              <tr className="border-b">
                <th className="p-3 text-left font-medium">Month</th>
                <th className="p-3 text-right font-medium">Avg Max (°C)</th>
                <th className="p-3 text-right font-medium">Avg Min (°C)</th>
                <th className="p-3 text-right font-medium">Range (°C)</th>
              </tr>
            </thead>
            <tbody>
              {data.map((item) => (
                <tr key={item.month} className="border-b hover:bg-muted/50">
                  <td className="p-3">{item.month}</td>
                  <td className="p-3 text-right">{item.avg_max.toFixed(2)}</td>
                  <td className="p-3 text-right">{item.avg_min.toFixed(2)}</td>
                  <td className="p-3 text-right">{(item.avg_max - item.avg_min).toFixed(2)}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </Card>
    </div>
  );
}
