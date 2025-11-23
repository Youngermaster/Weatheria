import { useEffect, useState } from 'react';
import { Card } from '@/components/ui/card';
import { StatCard } from '@/components/StatCard';
import { Thermometer, TrendingUp, Droplets, Calendar, AlertTriangle } from 'lucide-react';
import {
  LineChart,
  Line,
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
import type { MonthlyAverage, ExtremeTemperature, TemperaturePrecipitation } from '@/types';

const COLORS = ['#3b82f6', '#10b981', '#f59e0b', '#ef4444'];

export function Dashboard() {
  const [monthlyData, setMonthlyData] = useState<MonthlyAverage[]>([]);
  const [extremeData, setExtremeData] = useState<ExtremeTemperature[]>([]);
  const [precipData, setPrecipData] = useState<TemperaturePrecipitation[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [monthly, extreme, precip] = await Promise.all([
          weatheriaApi.getMonthlyAverages(),
          weatheriaApi.getExtremeTemperatures(),
          weatheriaApi.getTemperaturePrecipitation(),
        ]);

        setMonthlyData(monthly);
        setExtremeData(extreme);
        setPrecipData(precip);
      } catch (error) {
        console.error('Error fetching data:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  if (loading) {
    return (
      <div className="flex h-full items-center justify-center">
        <div className="text-center">
          <div className="h-12 w-12 animate-spin rounded-full border-4 border-primary border-t-transparent mx-auto" />
          <p className="mt-4 text-muted-foreground">Loading climate data...</p>
        </div>
      </div>
    );
  }

  // Calculate statistics
  const temps = monthlyData.map(d => ({ max: d.avg_max, min: d.avg_min }));
  const avgMaxTemp = temps.length > 0
    ? (temps.reduce((sum, t) => sum + t.max, 0) / temps.length).toFixed(1)
    : '0';
  const avgMinTemp = temps.length > 0
    ? (temps.reduce((sum, t) => sum + t.min, 0) / temps.length).toFixed(1)
    : '0';
  const maxTemp = temps.length > 0 ? Math.max(...temps.map(t => t.max)).toFixed(1) : '0';
  const minTemp = temps.length > 0 ? Math.min(...temps.map(t => t.min)).toFixed(1) : '0';

  // Calculate warming trend
  const firstYear = monthlyData.slice(0, 12);
  const lastYear = monthlyData.slice(-12);
  const firstYearAvg = firstYear.length > 0
    ? firstYear.reduce((sum, d) => sum + d.avg_max, 0) / firstYear.length
    : 0;
  const lastYearAvg = lastYear.length > 0
    ? lastYear.reduce((sum, d) => sum + d.avg_max, 0) / lastYear.length
    : 0;
  const warmingTrend = (lastYearAvg - firstYearAvg).toFixed(1);

  const totalPrecipitation = precipData.reduce((sum, d) => sum + d.total_precip, 0).toFixed(0);
  const extremeDays = extremeData.reduce((sum, d) => sum + d.count, 0);
  const veryHotDays = extremeData.find(d => d.category === 'very_hot')?.count || 0;

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h2 className="text-3xl font-bold tracking-tight">Climate Overview</h2>
        <p className="text-muted-foreground">
          Comprehensive analysis of Medellín's climate patterns (2022-2024)
        </p>
      </div>

      {/* Stats Grid */}
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
        <StatCard
          title="Average Temperature"
          value={`${avgMaxTemp}°C`}
          description={`Min: ${avgMinTemp}°C`}
          icon={Thermometer}
        />
        <StatCard
          title="Warming Trend"
          value={`${warmingTrend}°C`}
          description="2022 to 2024 change"
          icon={TrendingUp}
          trend={{ value: Number(warmingTrend), label: 'since 2022' }}
        />
        <StatCard
          title="Total Precipitation"
          value={`${totalPrecipitation} mm`}
          description="Over 36 months"
          icon={Droplets}
        />
        <StatCard
          title="Extreme Hot Days"
          value={veryHotDays}
          description="> 30°C maximum temp"
          icon={AlertTriangle}
        />
      </div>

      {/* Charts Grid */}
      <div className="grid gap-6 md:grid-cols-2">
        {/* Temperature Trend */}
        <Card className="p-6">
          <h3 className="mb-4 text-lg font-semibold">Temperature Trends</h3>
          <ResponsiveContainer width="100%" height={300}>
            <LineChart data={monthlyData}>
              <CartesianGrid strokeDasharray="3 3" className="stroke-muted" />
              <XAxis
                dataKey="month"
                className="text-xs"
                tickFormatter={(value) => value.slice(5)}
              />
              <YAxis className="text-xs" />
              <Tooltip
                contentStyle={{
                  backgroundColor: 'hsl(var(--card))',
                  border: '1px solid hsl(var(--border))',
                  borderRadius: '0.5rem'
                }}
              />
              <Legend />
              <Line
                type="monotone"
                dataKey="avg_max"
                stroke="#ef4444"
                name="Max Temp (°C)"
                strokeWidth={2}
              />
              <Line
                type="monotone"
                dataKey="avg_min"
                stroke="#3b82f6"
                name="Min Temp (°C)"
                strokeWidth={2}
              />
            </LineChart>
          </ResponsiveContainer>
        </Card>

        {/* Extreme Temperature Distribution */}
        <Card className="p-6">
          <h3 className="mb-4 text-lg font-semibold">Temperature Distribution</h3>
          <ResponsiveContainer width="100%" height={300}>
            <PieChart>
              <Pie
                data={extremeData}
                cx="50%"
                cy="50%"
                labelLine={false}
                label={({ category, count, percent }) =>
                  `${category}: ${count} (${(percent * 100).toFixed(0)}%)`
                }
                outerRadius={100}
                fill="#8884d8"
                dataKey="count"
              >
                {extremeData.map((_, index) => (
                  <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
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

        {/* Monthly Precipitation */}
        <Card className="p-6">
          <h3 className="mb-4 text-lg font-semibold">Monthly Precipitation</h3>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={precipData.slice(0, 12)}>
              <CartesianGrid strokeDasharray="3 3" className="stroke-muted" />
              <XAxis
                dataKey="month"
                className="text-xs"
                tickFormatter={(value) => value.slice(5)}
              />
              <YAxis className="text-xs" />
              <Tooltip
                contentStyle={{
                  backgroundColor: 'hsl(var(--card))',
                  border: '1px solid hsl(var(--border))',
                  borderRadius: '0.5rem'
                }}
              />
              <Legend />
              <Bar dataKey="total_precip" fill="#3b82f6" name="Precipitation (mm)" />
            </BarChart>
          </ResponsiveContainer>
        </Card>

        {/* Temperature-Precipitation Correlation */}
        <Card className="p-6">
          <h3 className="mb-4 text-lg font-semibold">Temperature vs Precipitation</h3>
          <ResponsiveContainer width="100%" height={300}>
            <LineChart data={precipData.slice(0, 12)}>
              <CartesianGrid strokeDasharray="3 3" className="stroke-muted" />
              <XAxis
                dataKey="month"
                className="text-xs"
                tickFormatter={(value) => value.slice(5)}
              />
              <YAxis yAxisId="left" className="text-xs" />
              <YAxis yAxisId="right" orientation="right" className="text-xs" />
              <Tooltip
                contentStyle={{
                  backgroundColor: 'hsl(var(--card))',
                  border: '1px solid hsl(var(--border))',
                  borderRadius: '0.5rem'
                }}
              />
              <Legend />
              <Line
                yAxisId="left"
                type="monotone"
                dataKey="avg_temp"
                stroke="#ef4444"
                name="Avg Temp (°C)"
                strokeWidth={2}
              />
              <Line
                yAxisId="right"
                type="monotone"
                dataKey="avg_precip"
                stroke="#3b82f6"
                name="Avg Precip (mm)"
                strokeWidth={2}
              />
            </LineChart>
          </ResponsiveContainer>
        </Card>
      </div>

      {/* Climate Insights */}
      <Card className="p-6">
        <h3 className="mb-4 text-lg font-semibold">Climate Change Insights</h3>
        <div className="grid gap-4 md:grid-cols-3">
          <div className="rounded-lg border p-4">
            <div className="mb-2 flex items-center gap-2">
              <TrendingUp className="h-5 w-5 text-red-500" />
              <h4 className="font-semibold">Warming Trend</h4>
            </div>
            <p className="text-sm text-muted-foreground">
              Temperature increased by {warmingTrend}°C from 2022 to 2024, indicating a notable warming pattern.
            </p>
          </div>
          <div className="rounded-lg border p-4">
            <div className="mb-2 flex items-center gap-2">
              <Droplets className="h-5 w-5 text-blue-500" />
              <h4 className="font-semibold">Precipitation Pattern</h4>
            </div>
            <p className="text-sm text-muted-foreground">
              Inverse correlation between temperature and rainfall suggests potential water stress during warm periods.
            </p>
          </div>
          <div className="rounded-lg border p-4">
            <div className="mb-2 flex items-center gap-2">
              <AlertTriangle className="h-5 w-5 text-amber-500" />
              <h4 className="font-semibold">Extreme Events</h4>
            </div>
            <p className="text-sm text-muted-foreground">
              Only {veryHotDays} extreme hot days recorded, showing Medellín maintains relatively stable temperatures.
            </p>
          </div>
        </div>
      </Card>
    </div>
  );
}
