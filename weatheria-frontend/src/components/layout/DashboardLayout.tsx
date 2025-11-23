import { Link, Outlet, useLocation } from 'react-router-dom';
import { Cloud, Home, TrendingUp, Thermometer, Droplets, Info } from 'lucide-react';
import { cn } from '@/lib/utils';
import { Separator } from '@/components/ui/separator';

const navigation = [
  { name: 'Dashboard', to: '/dashboard', icon: Home },
  { name: 'Monthly Analysis', to: '/monthly', icon: TrendingUp },
  { name: 'Extreme Temperatures', to: '/extreme', icon: Thermometer },
  { name: 'Precipitation Analysis', to: '/precipitation', icon: Droplets },
  { name: 'About', to: '/about', icon: Info },
];

export function DashboardLayout() {
  const location = useLocation();

  return (
    <div className="flex h-screen bg-background">
      {/* Sidebar */}
      <div className="hidden w-64 flex-col border-r bg-card md:flex">
        <div className="flex h-16 items-center gap-2 border-b px-6">
          <Cloud className="h-8 w-8 text-primary" />
          <div className="flex flex-col">
            <span className="text-lg font-bold">Weatheria</span>
            <span className="text-xs text-muted-foreground">Climate Observatory</span>
          </div>
        </div>

        <nav className="flex-1 space-y-1 p-4">
          {navigation.map((item) => {
            const isActive = location.pathname === item.to;
            const Icon = item.icon;

            return (
              <Link
                key={item.name}
                to={item.to}
                className={cn(
                  'flex items-center gap-3 rounded-lg px-3 py-2 text-sm font-medium transition-colors',
                  isActive
                    ? 'bg-primary text-primary-foreground'
                    : 'text-muted-foreground hover:bg-accent hover:text-accent-foreground'
                )}
              >
                <Icon className="h-5 w-5" />
                {item.name}
              </Link>
            );
          })}
        </nav>

        <Separator />

        <div className="p-4">
          <div className="rounded-lg bg-muted p-3 text-sm">
            <p className="font-semibold">Medellín, Colombia</p>
            <p className="text-xs text-muted-foreground">2022-2024 Analysis</p>
            <p className="mt-2 text-xs text-muted-foreground">
              1,096 days of climate data processed
            </p>
          </div>
        </div>
      </div>

      {/* Main Content */}
      <div className="flex flex-1 flex-col overflow-hidden">
        {/* Header */}
        <header className="flex h-16 items-center justify-between border-b bg-card px-6">
          <div>
            <h1 className="text-2xl font-bold">Weatheria Climate Observatory</h1>
            <p className="text-sm text-muted-foreground">
              MapReduce-based weather analysis for Medellín (2022-2024)
            </p>
          </div>

          <div className="flex items-center gap-2">
            <div className="flex items-center gap-1 rounded-md bg-green-500/10 px-2 py-1 text-xs text-green-600">
              <div className="h-2 w-2 rounded-full bg-green-600" />
              API Connected
            </div>
          </div>
        </header>

        {/* Page Content */}
        <main className="flex-1 overflow-auto bg-background p-6">
          <Outlet />
        </main>
      </div>
    </div>
  );
}
