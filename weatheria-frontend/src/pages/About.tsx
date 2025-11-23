import { Card } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Cloud, Database, LineChart, Server, Code2, Cpu } from 'lucide-react';

export function About() {
  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-3xl font-bold tracking-tight">About Weatheria Climate Observatory</h2>
        <p className="text-muted-foreground">
          MapReduce-based climate analysis system for Medellín, Colombia
        </p>
      </div>

      {/* Project Overview */}
      <Card className="p-6">
        <div className="flex items-start gap-4">
          <div className="rounded-lg bg-primary/10 p-3">
            <Cloud className="h-8 w-8 text-primary" />
          </div>
          <div className="flex-1">
            <h3 className="text-xl font-semibold">Project Overview</h3>
            <p className="mt-2 text-muted-foreground">
              Weatheria Climate Observatory is an academic project for EAFIT University (ST0263: Tópicos Especiales en Telemática)
              that implements a complete distributed batch processing pipeline using Hadoop MapReduce to analyze temperature
              patterns in Medellín, Colombia from 2022 to 2024.
            </p>
            <p className="mt-2 text-sm text-muted-foreground italic">
              Inspired by Weatheria, the sky island from One Piece dedicated to climate science research,
              this project brings that same spirit of climate research using modern distributed computing technologies.
            </p>
          </div>
        </div>
      </Card>

      {/* Technical Stack */}
      <div>
        <h3 className="mb-4 text-lg font-semibold">Technology Stack</h3>
        <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
          <Card className="p-4">
            <div className="flex items-center gap-3">
              <Database className="h-6 w-6 text-primary" />
              <div>
                <h4 className="font-semibold">Data Processing</h4>
                <p className="text-sm text-muted-foreground">Python, pandas, numpy</p>
              </div>
            </div>
          </Card>
          <Card className="p-4">
            <div className="flex items-center gap-3">
              <Cpu className="h-6 w-6 text-primary" />
              <div>
                <h4 className="font-semibold">MapReduce</h4>
                <p className="text-sm text-muted-foreground">Hadoop 3.3.6, MRJOB</p>
              </div>
            </div>
          </Card>
          <Card className="p-4">
            <div className="flex items-center gap-3">
              <Server className="h-6 w-6 text-primary" />
              <div>
                <h4 className="font-semibold">API Backend</h4>
                <p className="text-sm text-muted-foreground">FastAPI, Uvicorn</p>
              </div>
            </div>
          </Card>
          <Card className="p-4">
            <div className="flex items-center gap-3">
              <Code2 className="h-6 w-6 text-primary" />
              <div>
                <h4 className="font-semibold">Frontend</h4>
                <p className="text-sm text-muted-foreground">React, TypeScript, Vite</p>
              </div>
            </div>
          </Card>
          <Card className="p-4">
            <div className="flex items-center gap-3">
              <LineChart className="h-6 w-6 text-primary" />
              <div>
                <h4 className="font-semibold">Visualization</h4>
                <p className="text-sm text-muted-foreground">Recharts, TailwindCSS</p>
              </div>
            </div>
          </Card>
          <Card className="p-4">
            <div className="flex items-center gap-3">
              <Cloud className="h-6 w-6 text-primary" />
              <div>
                <h4 className="font-semibold">Deployment</h4>
                <p className="text-sm text-muted-foreground">Docker, AWS EMR</p>
              </div>
            </div>
          </Card>
        </div>
      </div>

      {/* MapReduce Jobs */}
      <div>
        <h3 className="mb-4 text-lg font-semibold">MapReduce Analyses</h3>
        <div className="space-y-4">
          <Card className="p-4">
            <div className="flex items-start gap-3">
              <Badge>1</Badge>
              <div className="flex-1">
                <h4 className="font-semibold">Monthly Average Temperature</h4>
                <p className="text-sm text-muted-foreground">
                  Calculates average maximum and minimum temperatures per month across 36 months (2022-2024),
                  revealing a warming trend of +1.8°C from 2022 to 2024.
                </p>
              </div>
            </div>
          </Card>
          <Card className="p-4">
            <div className="flex items-start gap-3">
              <Badge>2</Badge>
              <div className="flex-1">
                <h4 className="font-semibold">Extreme Temperature Detection</h4>
                <p className="text-sm text-muted-foreground">
                  Identifies days with extreme weather conditions (very hot &gt;30°C, cool &lt;15°C, very cool &lt;12°C),
                  showing that 63.9% of days had normal temperatures while 34.7% experienced cool conditions.
                </p>
              </div>
            </div>
          </Card>
          <Card className="p-4">
            <div className="flex items-start gap-3">
              <Badge>3</Badge>
              <div className="flex-1">
                <h4 className="font-semibold">Temperature-Precipitation Correlation</h4>
                <p className="text-sm text-muted-foreground">
                  Analyzes the relationship between temperature and rainfall by month, revealing a negative correlation
                  (-0.15 to -0.52) suggesting that warmer periods tend to have less precipitation.
                </p>
              </div>
            </div>
          </Card>
        </div>
      </div>

      {/* Data Source */}
      <Card className="p-6">
        <h3 className="mb-4 text-lg font-semibold">Data Source</h3>
        <div className="space-y-2 text-sm">
          <p><strong>Source:</strong> Open-Meteo Archive API</p>
          <p><strong>Location:</strong> Medellín, Colombia (6.25°N, 75.56°W)</p>
          <p><strong>Time Period:</strong> January 1, 2022 - December 31, 2024</p>
          <p><strong>Total Records:</strong> 1,096 daily measurements</p>
          <p><strong>Variables:</strong> Maximum temperature, minimum temperature, precipitation sum</p>
        </div>
      </Card>

      {/* Key Findings */}
      <Card className="p-6">
        <h3 className="mb-4 text-lg font-semibold">Key Climate Findings</h3>
        <div className="space-y-3">
          <div className="flex items-start gap-2">
            <div className="mt-1 h-2 w-2 rounded-full bg-red-500" />
            <p className="text-sm">
              <strong>Warming Trend:</strong> Temperature increased by 1.8°C from 2022 to 2024, indicating a notable warming pattern
            </p>
          </div>
          <div className="flex items-start gap-2">
            <div className="mt-1 h-2 w-2 rounded-full bg-blue-500" />
            <p className="text-sm">
              <strong>Inverse Correlation:</strong> Negative correlation between temperature and precipitation suggests
              potential water stress during warm periods
            </p>
          </div>
          <div className="flex items-start gap-2">
            <div className="mt-1 h-2 w-2 rounded-full bg-green-500" />
            <p className="text-sm">
              <strong>Temperature Stability:</strong> Only 23 extreme hot days (2.1%) recorded, showing Medellín maintains
              relatively stable temperatures
            </p>
          </div>
          <div className="flex items-start gap-2">
            <div className="mt-1 h-2 w-2 rounded-full bg-amber-500" />
            <p className="text-sm">
              <strong>Precipitation Patterns:</strong> Total rainfall of 5,754.5 mm over 3 years with significant
              seasonal variation (wettest month: 347.9 mm, driest: 106.5 mm)
            </p>
          </div>
        </div>
      </Card>

      {/* Links */}
      <Card className="p-6">
        <h3 className="mb-4 text-lg font-semibold">Resources</h3>
        <div className="space-y-2">
          <a
            href="http://localhost:8000/docs"
            target="_blank"
            rel="noopener noreferrer"
            className="block text-sm text-primary hover:underline"
          >
            API Documentation →
          </a>
          <a
            href="https://open-meteo.com"
            target="_blank"
            rel="noopener noreferrer"
            className="block text-sm text-primary hover:underline"
          >
            Open-Meteo API →
          </a>
          <p className="mt-4 text-xs text-muted-foreground">
            EAFIT University - ST0263: Tópicos Especiales en Telemática (2025-2)
          </p>
        </div>
      </Card>
    </div>
  );
}
