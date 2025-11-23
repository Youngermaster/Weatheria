import { Routes, Route, Navigate } from 'react-router-dom';
import { DashboardLayout } from '@/components/layout/DashboardLayout';
import { Dashboard } from '@/pages/Dashboard';
import { MonthlyAnalysis } from '@/pages/MonthlyAnalysis';
import { ExtremeAnalysis } from '@/pages/ExtremeAnalysis';
import { PrecipitationAnalysis } from '@/pages/PrecipitationAnalysis';
import { About } from '@/pages/About';
import './App.css';

function App() {
  return (
    <Routes>
      <Route path="/" element={<DashboardLayout />}>
        <Route index element={<Navigate to="/dashboard" replace />} />
        <Route path="dashboard" element={<Dashboard />} />
        <Route path="monthly" element={<MonthlyAnalysis />} />
        <Route path="extreme" element={<ExtremeAnalysis />} />
        <Route path="precipitation" element={<PrecipitationAnalysis />} />
        <Route path="about" element={<About />} />
      </Route>
    </Routes>
  );
}

export default App;
