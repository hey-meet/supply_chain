// --- PlantsInventory.jsx ---
import React, { useState, useEffect } from 'react';
import {
    LineChart, Line, BarChart, Bar, RadialBarChart, RadialBar, PieChart, Pie, Cell,
    XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer
} from 'recharts';
import {
    Factory,
    Package,
    AlertTriangle,
    CheckCircle2,
    Search,
    Filter,
    TrendingUp,
    TrendingDown,
    Clock,
    Truck,
    Layers,
    ArrowRight,
    ShieldAlert,
    SlidersHorizontal,
    MapPin,
    Cpu
} from 'lucide-react';
import '../styles/plants-inventory.css';

// --- STATIC MOCK DATA ---
const kpiData = [
    { id: 1, title: 'Total Production Today', value: '14,850 T', trend: '+4.2% vs baseline', status: 'success', icon: Factory },
    { id: 2, title: 'Inventory Health', value: '84%', trend: '-1.5% weekly slip', status: 'warning', icon: Package },
    { id: 3, title: 'Plants Online', value: '6 / 7', trend: '1 High Risk Obstructed', status: 'success', icon: CheckCircle2 },
    { id: 4, title: 'Materials at Risk', value: '2 Items', trend: 'Safety stock violated', status: 'critical', icon: AlertTriangle }
];

const plantsData = [
    {
        id: 'PLT-A',
        name: 'Plant A - Western Grinding Complex',
        location: 'Gujarat East',
        status: 'At Risk',
        healthScore: 68,
        production: '4,200 T/d',
        capacity: '5,000 T/d',
        utilization: 84,
        risk: 'Limestone supply vector obstruction via NH-48 flooding.',
        suppliers: 4,
        inventoryHealth: 'Critical',
        remainingDays: 1.5
    },
    {
        id: 'PLT-B',
        name: 'Plant B - Central Kiln Facility',
        location: 'Madhya Pradesh',
        status: 'Healthy',
        healthScore: 94,
        production: '6,100 T/d',
        capacity: '6,500 T/d',
        utilization: 93,
        risk: 'None. Off-peak power grid schedules nominal.',
        suppliers: 6,
        inventoryHealth: 'Optimal',
        remainingDays: 14
    },
    {
        id: 'PLT-C',
        name: 'Plant C - Southern Port Terminal',
        location: 'Tamil Nadu',
        status: 'Healthy',
        healthScore: 91,
        production: '4,550 T/d',
        capacity: '5,000 T/d',
        utilization: 91,
        risk: 'Minor diesel overhead variance via terminal port wait lanes.',
        suppliers: 5,
        inventoryHealth: 'Stable',
        remainingDays: 10
    }
];

const inventoryData = [
    { material: 'Limestone', stock: '6,200 T', safety: '15,000 T', consumption: '4,000 T/d', days: 1.5, incoming: '8,500 T', status: 'critical', supplier: 'Valsad Quarry Hub', risk: 'Critical', pct: 41 },
    { material: 'Coal', stock: '14,500 T', safety: '12,000 T', consumption: '1,200 T/d', days: 12, incoming: '5,000 T', status: 'warning', supplier: 'International Trade', risk: 'Medium', pct: 120 },
    { material: 'Fly Ash', stock: '9,800 T', safety: '8,000 T', consumption: '1,500 T/d', days: 6.5, incoming: '3,000 T', status: 'success', supplier: 'NTPC Cluster Node', risk: 'Low', pct: 122 },
    { material: 'Gypsum', stock: '4,100 T', safety: '3,500 T', consumption: '450 T/d', days: 9.1, incoming: '1,200 T', status: 'success', supplier: 'Border Transit Check', risk: 'Low', pct: 117 },
    { material: 'Diesel', stock: '85,000 L', safety: '90,000 L', consumption: '10,000 L/d', days: 8.5, incoming: '45,000 L', status: 'warning', supplier: 'Ministry Petroleum Link', risk: 'Medium', pct: 94 },
    { material: 'Packaging Material', stock: '240k Units', safety: '200k Units', consumption: '35k/d', days: 6.8, incoming: '150k Units', status: 'success', supplier: 'Zone East Pack Co', risk: 'Low', pct: 120 }
];

const aiInsights = [
    { priority: 'Critical', impact: 'Avoid Plant A shutdown completely', confidence: '97%', delay: '2 hours net', agent: 'Mitigation Planning Agent', action: 'Transfer 1,200 T Limestone from Plant C reserves via rail segment bypass loops.', title: 'Transfer Limestone from Plant C' },
    { priority: 'High', impact: 'Bypass broken logistics corridors on NH-48', confidence: '94%', delay: '+45 mins cycle', agent: 'Sourcing Optimization Engine', action: 'Activate alternative solid fuel contract terms with emergency Rajasthan Quarry suppliers.', title: 'Activate Emergency Backup Supplier' },
    { priority: 'Medium', impact: 'Hedging spot energy margin variance scales', confidence: '91%', delay: 'None', agent: 'Procurement Balance Module', action: 'Increase Coal procurement schedules across secondary rail loops to balance clinker burn runs.', title: 'Increase Coal Procurement' }
];

// --- CHART DATA CONFIGS ---
const productionTrendData = [
    { name: '08:00', PlantA: 380, PlantB: 590, PlantC: 420 },
    { name: '10:00', PlantA: 400, PlantB: 600, PlantC: 450 },
    { name: '12:00', PlantA: 420, PlantB: 610, PlantC: 455 },
    { name: '14:00', PlantA: 350, PlantB: 610, PlantC: 450 }
];

const inventoryConsumptionData = [
    { name: 'Limestone', Current: 6200, Safety: 15000 },
    { name: 'Coal', Current: 14500, Safety: 12000 },
    { name: 'Fly Ash', Current: 9800, Safety: 8000 },
    { name: 'Gypsum', Current: 4100, Safety: 3500 }
];

const capacityUtilizationData = [
    { name: 'Plant A', value: 84, fill: '#B15A52' },
    { name: 'Plant B', value: 93, fill: '#708C72' },
    { name: 'Plant C', value: 91, fill: '#3E556B' }
];

const materialAvailabilityData = [
    { name: 'Healthy Nodes', value: 4 },
    { name: 'Warning Nodes', value: 1 },
    { name: 'Critical Risks', value: 1 }
];
const pieColors = ['#708C72', '#C8A652', '#B15A52'];

export default function PlantsInventory() {
    const [liveSyncTime, setLiveSyncTime] = useState('14:37:50');
    const [selectedPlant, setSelectedPlant] = useState(plantsData[0]);

    useEffect(() => {
        const timer = setInterval(() => {
            const now = new Date();
            setLiveSyncTime(now.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', second: '2-digit' }));
        }, 1000);
        return () => clearInterval(timer);
    }, []);

    return (
        <div className="pi-content-scope">

            {/* Page Header Area */}
            <header className="pi-header-block">
                <div className="pi-header-left">
                    <h1 className="pi-page-title">Plant Operations & Inventory</h1>
                    <p className="pi-page-subtitle">Real-time monitoring of production plants, inventory health and material availability.</p>
                </div>
                <div className="pi-header-right">
                    <div className="pi-sync-pill">
                        <Clock size={13} />
                        <span className="pi-sync-lbl">Last Sync:</span>
                        <span className="pi-sync-val font-mono">{liveSyncTime}</span>
                    </div>
                    <div className="pi-badge-live">
                        <span className="pi-pulse-dot"></span>
                        3 ACTIVE PRODUCTION KILNS RENDERED
                    </div>
                </div>
            </header>

            {/* Top Executive KPI Grid Section */}
            <section className="pi-kpi-grid">
                {kpiData.map((kpi) => {
                    const Icon = kpi.icon;
                    return (
                        <div key={kpi.id} className="pi-kpi-card">
                            <div className="pi-kpi-header-flex">
                                <span className={`pi-kpi-icon-wrapper status-${kpi.status}`}>
                                    <Icon size={18} />
                                </span>
                                <span className={`pi-kpi-trend-tag status-${kpi.status}`}>
                                    {kpi.status === 'critical' || kpi.id === 2 ? <TrendingDown size={12} /> : <TrendingUp size={12} />}
                                    {kpi.trend}
                                </span>
                            </div>
                            <div className="pi-kpi-meta-block">
                                <span className="pi-kpi-lbl">{kpi.title}</span>
                                <h3 className="pi-kpi-val-text">{kpi.value}</h3>
                            </div>
                        </div>
                    );
                })}
            </section>

            {/* Plant Overview Layer Panel */}
            <section className="pi-plants-overview-section">
                <div className="pi-section-title-wrapper">
                    <Factory size={16} className="pi-section-title-icon" />
                    <h2 className="pi-section-title">Industrial Plant Execution Framework</h2>
                </div>
                <div className="pi-plants-grid">
                    {plantsData.map((plant) => (
                        <div
                            key={plant.id}
                            className={`pi-plant-card-item is-${plant.status.toLowerCase().replace(' ', '-')}`}
                            onClick={() => setSelectedPlant(plant)}
                        >
                            <div className="plant-card-top-row">
                                <div className="plant-card-identity">
                                    <h3 className="plant-card-name">{plant.name}</h3>
                                    <span className="plant-card-location"><MapPin size={11} /> {plant.location}</span>
                                </div>
                                <span className={`plant-status-badge tag-${plant.status.toLowerCase().replace(' ', '-')}`}>
                                    {plant.status}
                                </span>
                            </div>

                            <div className="plant-card-metrics-strip">
                                <div className="plant-strip-cell">
                                    <span className="strip-lbl">Yield Output</span>
                                    <span className="strip-val">{plant.production}</span>
                                </div>
                                <div className="plant-strip-cell">
                                    <span className="strip-lbl">Utilization</span>
                                    <span className="strip-val font-mono">{plant.utilization}%</span>
                                </div>
                                <div className="plant-strip-cell text-right">
                                    <span className="strip-lbl">Remaining Days</span>
                                    <span className={`strip-val font-semibold variant-${plant.status.toLowerCase().replace(' ', '-')}`}>
                                        {plant.remainingDays} Days
                                    </span>
                                </div>
                            </div>

                            <div className="plant-progress-measure-block">
                                <div className="progress-labels-row">
                                    <span className="p-lbl">Capacity Threshold Allocation ({plant.capacity})</span>
                                </div>
                                <div className="progress-track-frame">
                                    <span
                                        className={`progress-fill-element fill-${plant.status.toLowerCase().replace(' ', '-')}`}
                                        style={{ width: `${plant.utilization}%` }}
                                    ></span>
                                </div>
                            </div>

                            <div className="plant-card-risk-statement">
                                <span className="risk-lbl-tag">Operational Directive Risk Context:</span>
                                <p className="risk-text-paragraph truncate">{plant.risk}</p>
                            </div>
                        </div>
                    ))}
                </div>
            </section>

            {/* Main Content Workspace Layout Grid */}
            <section className="pi-workspace-layout-grid">

                {/* Left Column Panel: Plant System Filters */}
                <div className="pi-column-container col-left-filters">
                    <div className="column-header-row">
                        <SlidersHorizontal size={14} className="col-icon-sync" />
                        <h3 className="column-title-heading">Plant Filters</h3>
                    </div>

                    <div className="filter-controls-stack">
                        <div className="search-input-wrapper-box">
                            <Search size={13} className="search-icon-inside" />
                            <input type="text" className="filter-input-element" placeholder="Search plant assets..." disabled value="Plant A - Western Complex" />
                        </div>

                        <div className="dummy-filter-row-item">
                            <span className="filter-label-txt">Location Matrix Node</span>
                            <select className="filter-select-element" disabled><option>All Mapped States</option></select>
                        </div>
                        <div className="dummy-filter-row-item">
                            <span className="filter-label-txt">Risk Level Parameter</span>
                            <select className="filter-select-element" disabled><option>High Execution Risks</option></select>
                        </div>
                        <div className="dummy-filter-row-item">
                            <span className="filter-label-txt">Primary Input Material</span>
                            <select className="filter-select-element" disabled><option>Limestone Bulk Cargo</option></select>
                        </div>
                    </div>

                    <div className="quick-statistics-subpanel">
                        <h4 className="subpanel-title-label">Quick Statistics</h4>
                        <div className="quick-stats-rows-stack">
                            <div className="q-stat-row"><span>Plants Active Online</span><span className="font-mono font-semibold text-success">6 / 7</span></div>
                            <div className="q-stat-row"><span>Critical Risks Tracked</span><span className="font-mono font-semibold text-critical">1 Plant</span></div>
                            <div className="q-stat-row"><span>Materials Below Safety Stock</span><span className="font-mono font-semibold text-critical">2 Items</span></div>
                            <div className="q-stat-row"><span>Avg Capacity Utilization</span><span className="font-mono font-semibold text-brand">89.3%</span></div>
                        </div>
                    </div>
                </div>

                {/* Center Column Panel: Enterprise Inventory Table */}
                <div className="pi-column-container col-center-table">
                    <div className="column-header-row">
                        <Layers size={14} className="col-icon-sync" />
                        <h3 className="column-title-heading">Enterprise Inventory Table</h3>
                    </div>

                    <div className="responsive-table-scroll-window">
                        <table className="enterprise-data-table-element">
                            <thead>
                                <tr>
                                    <th>Material</th>
                                    <th>Current Stock</th>
                                    <th>Safety Stock</th>
                                    <th>Daily Burn</th>
                                    <th>Remaining</th>
                                    <th>Incoming</th>
                                    <th>Supplier Node</th>
                                    <th>Status</th>
                                </tr>
                            </thead>
                            <tbody>
                                {inventoryData.map((row, idx) => (
                                    <tr key={idx} className={`table-row-state-${row.status}`}>
                                        <td className="font-semibold text-brand">{row.material}</td>
                                        <td className="font-mono">{row.stock}</td>
                                        <td className="font-mono text-secondary">{row.safety}</td>
                                        <td className="font-mono">{row.consumption}</td>
                                        <td>
                                            <span className={`table-days-pill state-${row.status}`}>
                                                {row.days} Days
                                            </span>
                                        </td>
                                        <td className="font-mono text-brand">{row.incoming}</td>
                                        <td className="truncate-cell">{row.supplier}</td>
                                        <td>
                                            <div className="table-status-badge-cell">
                                                <span className={`status-dot dot-${row.status}`}></span>
                                                <span className={`status-label-txt text-${row.status}`}>{row.risk}</span>
                                            </div>
                                        </td>
                                    </tr>
                                ))}
                            </tbody>
                        </table>
                    </div>
                </div>

                {/* Right Column Panel: Mapped Plant Telemetry Details */}
                <div className="pi-column-container col-right-details">
                    <div className="column-header-row">
                        <ShieldAlert size={14} className="col-icon-sync" />
                        <h3 className="column-title-heading">Plant Details Profile</h3>
                    </div>

                    <div className="plant-details-profile-stack">
                        <div className="profile-identity-header">
                            <span className="profile-lbl">Selected Target Asset</span>
                            <h4 className="profile-asset-title-text">{selectedPlant.name}</h4>
                            <span className="profile-meta-subtext"><MapPin size={10} /> {selectedPlant.location} Sector Profile</span>
                        </div>

                        <div className="profile-metrics-property-list">
                            <div className="p-property-row"><span>Production Capacity Status</span><span className="font-semibold">{selectedPlant.production} / {selectedPlant.capacity}</span></div>
                            <div className="p-property-row"><span>Active Operating Shift</span><span className="font-mono font-semibold">Shift B - Operational Matrix</span></div>
                            <div className="p-property-row"><span>Incoming Freight Shipments</span><span className="font-mono text-brand font-semibold">2 Fleet Vectors Enroute</span></div>
                            <div className="p-property-row"><span>Silo Buffer Inventory Level</span><span className="font-semibold text-critical">{selectedPlant.inventoryHealth} Reserve</span></div>
                            <div className="p-property-row"><span>Estimated Shutdown Risk</span><span className="font-semibold text-critical">High Risk Exposure (36h)</span></div>
                            <div className="p-property-row"><span>Recovery Time Estimation</span><span className="font-mono text-brand font-semibold">4.5 Hours Post Route Reopen</span></div>
                        </div>

                        <div className="profile-asset-connections-block">
                            <span className="profile-lbl">Connected Asset Infrastructure</span>
                            <div className="connections-pills-row">
                                <span className="conn-pill"><Truck size={10} /> NH-48 Fleet Loop</span>
                                <span className="conn-pill"><Factory size={10} /> Kiln Grinding Array 1</span>
                            </div>
                        </div>
                    </div>
                </div>

            </section>

            {/* Bottom Section: Recharts Operations Analytics */}
            <section className="pi-analytics-charts-section">
                <div className="pi-section-title-wrapper border-bottom-sync">
                    <TrendingUp size={16} className="pi-section-title-icon" />
                    <h2 className="pi-section-title">Operations & Ingestion Analytics</h2>
                </div>
                <div className="analytics-charts-fluid-grid">

                    {/* Chart 1: Line Chart */}
                    <div className="chart-canvas-card">
                        <h4 className="chart-card-heading-title">Production Output Trend (T/h)</h4>
                        <div className="recharts-container-element">
                            <ResponsiveContainer width="100%" height="100%">
                                <LineChart data={productionTrendData} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
                                    <CartesianGrid strokeDasharray="3 3" stroke="#D1D5D8" />
                                    <XAxis dataKey="name" stroke="#7D8791" style={{ fontSize: 11 }} />
                                    <YAxis stroke="#7D8791" style={{ fontSize: 11 }} />
                                    <Tooltip />
                                    <Line type="monotone" dataKey="PlantA" stroke="#B15A52" strokeWidth={2.5} dot={{ r: 3 }} name="Plant A" />
                                    <Line type="monotone" dataKey="PlantB" stroke="#708C72" strokeWidth={2.5} dot={{ r: 3 }} name="Plant B" />
                                </LineChart>
                            </ResponsiveContainer>
                        </div>
                    </div>

                    {/* Chart 2: Bar Chart */}
                    <div className="chart-canvas-card">
                        <h4 className="chart-card-heading-title">Inventory vs Safety Thresholds (T)</h4>
                        <div className="recharts-container-element">
                            <ResponsiveContainer width="100%" height="100%">
                                <BarChart data={inventoryConsumptionData} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
                                    <CartesianGrid strokeDasharray="3 3" stroke="#D1D5D8" />
                                    <XAxis dataKey="name" stroke="#7D8791" style={{ fontSize: 11 }} />
                                    <YAxis stroke="#7D8791" style={{ fontSize: 11 }} />
                                    <Tooltip />
                                    <Bar dataKey="Current" fill="#3E556B" radius={[4, 4, 0, 0]} name="Current Stock" />
                                    <Bar dataKey="Safety" fill="#ECEFF1" radius={[4, 4, 0, 0]} name="Safety Margin" />
                                </BarChart>
                            </ResponsiveContainer>
                        </div>
                    </div>

                    {/* Chart 3: Radial Bar Chart */}
                    <div className="chart-canvas-card">
                        <h4 className="chart-card-heading-title">Capacity Utilization (%)</h4>
                        <div className="recharts-container-element flex-center">
                            <ResponsiveContainer width="100%" height="100%">
                                <RadialBarChart cx="50%" cy="50%" innerRadius="30%" outerRadius="90%" barSize={12} data={capacityUtilizationData}>
                                    <RadialBar minAngle={15} background clockWise dataKey="value" cornerRadius={4} />
                                    <Tooltip />
                                </RadialBarChart>
                            </ResponsiveContainer>
                        </div>
                    </div>

                    {/* Chart 4: Donut Chart */}
                    <div className="chart-canvas-card">
                        <h4 className="chart-card-heading-title">Material Availability Risk Nodes</h4>
                        <div className="recharts-container-element flex-center">
                            <ResponsiveContainer width="100%" height="100%">
                                <PieChart>
                                    <Pie data={materialAvailabilityData} cx="50%" cy="50%" innerRadius={35} outerRadius={55} paddingAngle={4} dataKey="value">
                                        {materialAvailabilityData.map((entry, index) => (
                                            <Cell key={`cell-${index}`} fill={pieColors[index % pieColors.length]} />
                                        ))}
                                    </Pie>
                                    <Tooltip />
                                </PieChart>
                            </ResponsiveContainer>
                        </div>
                    </div>

                </div>
            </section>

            {/* Bottom Panel: AI Operations Ingestion Insights */}
            <section className="pi-ai-insights-panel-section">
                <div className="pi-section-title-wrapper border-none">
                    <Cpu size={16} className="pi-section-title-icon color-brand" />
                    <h2 className="pi-section-title">Autonomous AI Operations Insights</h2>
                </div>
                <div className="pi-insights-fluid-grid">
                    {aiInsights.map((insight, idx) => (
                        <div key={idx} className={`pi-insight-action-card rank-${insight.priority.toLowerCase()}`}>
                            <div className="insight-card-top-header-row">
                                <span className={`insight-priority-pill tag-${insight.priority.toLowerCase()}`}>
                                    {insight.priority} Priority
                                </span>
                                <span className="insight-agent-identity-txt"><Cpu size={10} /> {insight.agent}</span>
                            </div>
                            <h3 className="insight-action-heading-title">{insight.title}</h3>
                            <div className="insight-impact-parameters-box">
                                <div className="insight-param-cell"><span className="ip-lbl">Business Target Impact</span><span className="ip-val color-brand font-semibold">{insight.impact}</span></div>
                                <div className="insight-param-cell"><span className="ip-lbl">Latency / Variance</span><span className="ip-val font-mono color-crit">{insight.delay}</span></div>
                            </div>
                            <div className="insight-strategy-directive-block">
                                <span className="ip-lbl">Prescribed Execution Strategy Action:</span>
                                <p className="insight-strategy-paragraph-text">{insight.action}</p>
                            </div>
                            <button className={`insight-execution-trigger btn-${insight.priority.toLowerCase()}`}>
                                Authorize Logistics Protocols <ArrowRight size={13} />
                            </button>
                        </div>
                    ))}
                </div>
            </section>

        </div>
    );
}