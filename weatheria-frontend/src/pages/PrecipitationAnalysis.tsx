import { useEffect, useState } from 'react';
import { Card } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Download, Droplets, TrendingDown, Calendar } from 'lucide-react';
import {
  ComposedChart,
  Line,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
  ScatterChart,
  Scatter,
  ZAxis,
} from 'recharts';
import { weatheriaApi } from '@/services/api';
import type { TemperaturePrecipitation } from '@/types';
import { StatCard } from '@/components/StatCard';

export function PrecipitationAnalysis() {
  const [data, setData] = useState<TemperaturePrecipitation[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const precip = await weatheriaApi.getTemperaturePrecipitation();
        setData(precip);
      } catch (error) {
        console.error('Error fetching precipitation data:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  const handleDownload = async () => {
    try {
      const blob = await weatheriaApi.downloadResults('temp-precipitation');
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = 'temp_precip_results.csv';
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
          <p className="mt-4 text-muted-foreground">Loading precipitation data...</p>
        </div>
      </div>
    );
  }

  const wettestMonth = data.reduce((max, item) =>
    item.total_precip > max.total_precip ? item : max, data[0]
  );
  const driestMonth = data.reduce((min, item) =>
    item.total_precip < min.total_precip ? item : min, data[0]
  );
  const totalPrecip = data.reduce((sum, item) => sum + item.total_precip, 0);
  const avgCorrelation = (data.reduce((sum, item) => sum + item.correlation, 0) / data.length).toFixed(3);

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-3xl font-bold tracking-tight">Temperature-Precipitation Analysis</h2>
          <p className="text-muted-foreground">
            Correlation analysis between temperature and rainfall patterns
          </p>
        </div>
        <Button onClick={handleDownload} className="gap-2">
          <Download className="h-4 w-4" />
          Download Data
        </Button>
      </div>

      {/* Summary Stats */}
      <div className="grid gap-4 md:grid-cols-4">
        <StatCard
          title="Total Precipitation"
          value={`${totalPrecip.toFixed(0)} mm`}
          description="Over 36 months"
          icon={Droplets}
        />
        <StatCard
          title="Avg Correlation"
          value={avgCorrelation}
          description="Temp-Precip relationship"
          icon={TrendingDown}
        />
        <Card className="p-6">
          <h3 className="text-sm font-medium text-muted-foreground">Wettest Month</h3>
          <p className="mt-2 text-2xl font-bold">{wettestMonth?.month}</p>
          <p className="text-sm text-muted-foreground">
            {wettestMonth?.total_precip.toFixed(0)} mm | {wettestMonth?.rainy_days} rainy days
          </p>
        </Card>
        <Card className="p-6">
          <h3 className="text-sm font-medium text-muted-foreground">Driest Month</h3>
          <p className="mt-2 text-2xl font-bold">{driestMonth?.month}</p>
          <p className="text-sm text-muted-foreground">
            {driestMonth?.total_precip.toFixed(0)} mm | {driestMonth?.rainy_days} rainy days
          </p>
        </Card>
      </div>

      {/* Combined Chart */}
      <Card className="p-6">
        <h3 className="mb-6 text-lg font-semibold">Temperature vs Precipitation Patterns</h3>
        <ResponsiveContainer width="100%" height={400}>
          <ComposedChart data={data}>
            <CartesianGrid strokeDasharray="3 3" className="stroke-muted" />
            <XAxis dataKey="month" className="text-xs" />
            <YAxis yAxisId="left" className="text-xs" label={{ value: 'Temperature (°C)', angle: -90, position: 'insideLeft' }} />
            <YAxis yAxisId="right" orientation="right" className="text-xs" label={{ value: 'Precipitation (mm)', angle: 90, position: 'insideRight' }} />
            <Tooltip
              contentStyle={{
                backgroundColor: 'hsl(var(--card))',
                border: '1px solid hsl(var(--border))',
                borderRadius: '0.5rem'
              }}
            />
            <Legend />
            <Bar yAxisId="right" dataKey="total_precip" fill="#3b82f6" name="Total Precipitation (mm)" />
            <Line
              yAxisId="left"
              type="monotone"
              dataKey="avg_temp"
              stroke="#ef4444"
              strokeWidth={2}
              name="Average Temperature (°C)"
            />
          </ComposedChart>
        </ResponsiveContainer>
      </Card>

      {/* Scatter Plot */}
      <Card className="p-6">
        <h3 className="mb-6 text-lg font-semibold">Correlation Scatter Plot</h3>
        <ResponsiveContainer width="100%" height={400}>
          <ScatterChart>
            <CartesianGrid strokeDasharray="3 3" className="stroke-muted" />
            <XAxis
              type="number"
              dataKey="avg_temp"
              name="Temperature"
              unit="°C"
              className="text-xs"
              label={{ value: 'Average Temperature (°C)', position: 'insideBottom', offset: -5 }}
            />
            <YAxis
              type="number"
              dataKey="total_precip"
              name="Precipitation"
              unit="mm"
              className="text-xs"
              label={{ value: 'Total Precipitation (mm)', angle: -90, position: 'insideLeft' }}
            />
            <ZAxis range={[100, 400]} />
            <Tooltip
              cursor={{ strokeDasharray: '3 3' }}
              contentStyle={{
                backgroundColor: 'hsl(var(--card))',
                border: '1px solid hsl(var(--border))',
                borderRadius: '0.5rem'
              }}
            />
            <Scatter name="Monthly Data" data={data} fill="#3b82f6" />
          </ScatterChart>
        </ResponsiveContainer>
        <p className="mt-4 text-sm text-muted-foreground text-center">
          Negative correlation suggests higher temperatures are associated with less precipitation
        </p>
      </Card>

      {/* Monthly Details Table */}
      <Card className="p-6">
        <h3 className="mb-4 text-lg font-semibold">Monthly Correlation Details</h3>
        <div className="overflow-x-auto">
          <table className="w-full text-sm">
            <thead>
              <tr className="border-b">
                <th className="p-3 text-left font-medium">Month</th>
                <th className="p-3 text-right font-medium">Correlation</th>
                <th className="p-3 text-right font-medium">Avg Temp (°C)</th>
                <th className="p-3 text-right font-medium">Avg Precip (mm)</th>
                <th className="p-3 text-right font-medium">Rainy Days</th>
                <th className="p-3 text-right font-medium">Total Precip (mm)</th>
              </tr>
            </thead>
            <tbody>
              {data.map((item) => (
                <tr key={item.month} className="border-b hover:bg-muted/50">
                  <td className="p-3">{item.month}</td>
                  <td className={`p-3 text-right font-medium ${
                    item.correlation < 0 ? 'text-blue-600' : 'text-red-600'
                  }`}>
                    {item.correlation.toFixed(4)}
                  </td>
                  <td className="p-3 text-right">{item.avg_temp.toFixed(2)}</td>
                  <td className="p-3 text-right">{item.avg_precip.toFixed(2)}</td>
                  <td className="p-3 text-right">{item.rainy_days}</td>
                  <td className="p-3 text-right">{item.total_precip.toFixed(2)}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </Card>

      {/* Insights */}
      <Card className="p-6">
        <h3 className="mb-4 text-lg font-semibold">Climate Insights</h3>
        <div className="grid gap-4 md:grid-cols-2">
          <div className="rounded-lg border p-4">
            <h4 className="mb-2 font-semibold">Inverse Relationship</h4>
            <p className="text-sm text-muted-foreground">
              The average correlation of {avgCorrelation} indicates a moderate negative relationship between
              temperature and precipitation. Warmer periods tend to have less rainfall, which could intensify
              with continued climate warming.
            </p>
          </div>
          <div className="rounded-lg border p-4">
            <h4 className="mb-2 font-semibold">Seasonal Pattern</h4>
            <p className="text-sm text-muted-foreground">
              The wettest month ({wettestMonth?.month}) recorded {wettestMonth?.total_precip.toFixed(0)} mm
              while the driest ({driestMonth?.month}) had only {driestMonth?.total_precip.toFixed(0)} mm,
              showing significant seasonal variation in precipitation.
            </p>
          </div>
        </div>
      </Card>
    </div>
  );
}
