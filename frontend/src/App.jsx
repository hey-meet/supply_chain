import React from 'react';
import { Routes, Route } from 'react-router-dom';
import DashboardLayout from './components/layout/DashboardLayout';
import ExecutiveDashboard from './pages/ExecutiveDashboard';
import NewsIntelligence from './pages/NewsIntelligence';
import IncidentCenter from './pages/IncidentCenter';
import SupplyChainNetwork from './pages/SupplyChainNetwork';
import PlantsInventory from './pages/PlantsInventory';
import AIDecisionCenter from './pages/AIDecisionCenter';
import ExecutiveReports from './pages/ExecutiveReports';
import Settings from './pages/Settings';
import './App.css';

function App() {
  return (
    <Routes>
      <Route element={<DashboardLayout />}>
        <Route path="/" element={<ExecutiveDashboard />} />
        <Route path="/news" element={<NewsIntelligence />} />
        <Route path="/incidents" element={<IncidentCenter />} />
        <Route path="/network" element={<SupplyChainNetwork />} />
        <Route path="/plants" element={<PlantsInventory />} />
        <Route path="/ai-center" element={<AIDecisionCenter />} />
        <Route path="/reports" element={<ExecutiveReports />} />
        <Route path="/settings" element={<Settings />} />
      </Route>
    </Routes>
  );
}

export default App;