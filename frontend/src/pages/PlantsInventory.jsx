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
import plantService from "../services/plantService";
import '../styles/plants-inventory.css';

const pieColors = ['#708C72', '#C8A652', '#B15A52'];

// Map icon string names or fallbacks if icons are provided via backend strings
const getKpiIcon = (kpi) => {
    switch (kpi.id) {
        case 1:
            return Factory;
        case 2:
            return Package;
        case 3:
            return CheckCircle2;
        case 4:
            return AlertTriangle;
        default:
            return Factory;
    }
};

export default function PlantsInventory() {
    const [liveSyncTime, setLiveSyncTime] = useState('14:37:50');
    const [selectedPlant, setSelectedPlant] = useState(null);

    // API Data State
    const [data, setData] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    // Filter & Search states (Local filtering only - no backend requests)
    const [searchQuery, setSearchQuery] = useState('');
    const [selectedLocation, setSelectedLocation] = useState('All');
    const [selectedRisk, setSelectedRisk] = useState('All');
    const [selectedMaterial, setSelectedMaterial] = useState('All');

    // Fetch Backend Data
    useEffect(() => {
        const fetchInventoryData = async () => {
            try {
                setLoading(true);
                setError(null);
                const response = await plantService.getPlantsInventory();
                if (response && response.success) {
                    const fetchedData = response.data;
                    setData(fetchedData);
                    if (fetchedData && fetchedData.plants && fetchedData.plants.length > 0) {
                        setSelectedPlant(fetchedData.plants[0]);
                    }
                } else {
                    setError(new Error(response?.message || "Failed to load plant inventory data."));
                }
            } catch (err) {
                console.error("Failed to fetch plant inventory data:", err);
                setError(err);
            } finally {
                setLoading(false);
            }
        };

        fetchInventoryData();
    }, []);

    // Timer Sync
    useEffect(() => {
        const timer = setInterval(() => {
            const now = new Date();
            setLiveSyncTime(now.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', second: '2-digit' }));
        }, 1000);
        return () => clearInterval(timer);
    }, []);

    const handleAuthorizeAction = (title) => {
        alert(`Action has no backend implementation. Sourcing protocols for "${title}" cannot be executed.`);
    };

    if (loading) {
        return (
            <div className="pi-content-scope flex-center" style={{ minHeight: '400px', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                <p style={{ color: 'var(--intel-text-s)' }}>Loading Plant Operations & Inventory data...</p>
            </div>
        );
    }

    if (error && (!data || !data.plants)) {
        const message = error.message || "";
        if (message.includes("pending") || message.includes("Initialize") || message.includes("query") || message.includes("execute") || message.includes("first")) {
            return (
                <div className="pi-content-scope flex-center-pending" style={{ minHeight: '500px', display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', gap: '16px', padding: '40px' }}>
                    <h1 className="pi-page-title">Plant Operations & Inventory</h1>
                    <div className="alert-badge critical" style={{ background: 'var(--intel-critical)', color: 'white', padding: '8px 16px', borderRadius: '6px', fontWeight: 'bold' }}>NO ACTIVE SIMULATION</div>
                    <p style={{ color: 'var(--intel-text-s)', fontSize: '15px', maxWidth: '500px', textAlign: 'center', marginTop: '10px' }}>
                        No active supply chain risk assessment was found. Please head to the <strong>News Intelligence</strong> tab to execute an incident search query.
                    </p>
                </div>
            );
        }
        return (
            <div className="pi-content-scope flex-center" style={{ minHeight: '400px', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                <p className="text-critical">Error: {message}</p>
            </div>
        );
    }

    const kpiData = data?.kpis || [];
    const plantsData = data?.plants || [];
    const inventoryData = data?.inventory || [];
    const aiInsights = data?.ai_insights || [];
    const productionTrendData = data?.production_trend || [];
    const inventoryConsumptionData = data?.inventory_consumption || [];
    const capacityUtilizationData = data?.capacity_utilization || [];
    const materialAvailabilityData = data?.material_availability || [];

    // Local state filtering collections
    const uniqueLocations = Array.from(new Set(plantsData.map(p => p.location.split(',')[1]?.trim() || p.location)));
    const uniqueMaterials = Array.from(new Set(inventoryData.map(i => i.material)));

    const filteredPlants = plantsData.filter(plant => {
        const matchesSearch = plant.name.toLowerCase().includes(searchQuery.toLowerCase()) || 
                              plant.location.toLowerCase().includes(searchQuery.toLowerCase());
        const matchesLocation = selectedLocation === 'All' || plant.location.includes(selectedLocation);
        const matchesRisk = selectedRisk === 'All' || 
                            (selectedRisk === 'High' && (plant.status === 'At Risk' || plant.status === 'Critical')) ||
                            (selectedRisk === 'Medium' && plant.status === 'Warning') ||
                            (selectedRisk === 'Low' && plant.status === 'Healthy');
        return matchesSearch && matchesLocation && matchesRisk;
    });

    const filteredInventory = inventoryData.filter(item => {
        const matchesSearch = item.material.toLowerCase().includes(searchQuery.toLowerCase()) ||
                              item.supplier.toLowerCase().includes(searchQuery.toLowerCase());
        const matchesMaterial = selectedMaterial === 'All' || item.material === selectedMaterial;
        return matchesSearch && matchesMaterial;
    });

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
                        {plantsData.length} ACTIVE PRODUCTION KILNS RENDERED
                    </div>
                </div>
            </header>

            {/* Top Executive KPI Grid Section */}
            <section className="pi-kpi-grid">
                {kpiData.map((kpi) => {
                    const Icon = getKpiIcon(kpi);
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
                    {filteredPlants.length > 0 ? (
                        filteredPlants.map((plant) => (
                            <div
                                key={plant.id}
                                className={`pi-plant-card-item is-${plant.status ? plant.status.toLowerCase().replace(' ', '-') : ''} ${selectedPlant?.id === plant.id ? 'active-selected' : ''}`}
                                onClick={() => setSelectedPlant(plant)}
                            >
                                <div className="plant-card-top-row">
                                    <div className="plant-card-identity">
                                        <h3 className="plant-card-name">{plant.name}</h3>
                                        <span className="plant-card-location"><MapPin size={11} /> {plant.location}</span>
                                    </div>
                                    <span className={`plant-status-badge tag-${plant.status ? plant.status.toLowerCase().replace(' ', '-') : ''}`}>
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
                                        <span className={`strip-val font-semibold variant-${plant.status ? plant.status.toLowerCase().replace(' ', '-') : ''}`}>
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
                                            className={`progress-fill-element fill-${plant.status ? plant.status.toLowerCase().replace(' ', '-') : ''}`}
                                            style={{ width: `${plant.utilization}%` }}
                                        ></span>
                                    </div>
                                </div>

                                <div className="plant-card-risk-statement">
                                    <span className="risk-lbl-tag">Operational Directive Risk Context:</span>
                                    <p className="risk-text-paragraph truncate">{plant.risk}</p>
                                </div>
                            </div>
                        ))
                    ) : (
                        <div className="pi-plant-card-item flex-center" style={{ gridColumn: '1 / -1', padding: '40px', textAlign: 'center', color: 'var(--intel-text-s)' }}>
                            No active plants matching selected filters.
                        </div>
                    )}
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
                            <input 
                                type="text" 
                                className="filter-input-element" 
                                placeholder="Search plant assets..." 
                                value={searchQuery}
                                onChange={(e) => setSearchQuery(e.target.value)}
                            />
                        </div>

                        <div className="dummy-filter-row-item">
                            <span className="filter-label-txt">Location Matrix Node</span>
                            <select 
                                className="filter-select-element" 
                                value={selectedLocation} 
                                onChange={(e) => setSelectedLocation(e.target.value)}
                            >
                                <option value="All">All Regions</option>
                                {uniqueLocations.map(loc => (
                                    <option key={loc} value={loc}>{loc}</option>
                                ))}
                            </select>
                        </div>
                        <div className="dummy-filter-row-item">
                            <span className="filter-label-txt">Risk Level Parameter</span>
                            <select 
                                className="filter-select-element" 
                                value={selectedRisk} 
                                onChange={(e) => setSelectedRisk(e.target.value)}
                            >
                                <option value="All">All Risk Levels</option>
                                <option value="High">High / Critical</option>
                                <option value="Medium">Warning / Medium</option>
                                <option value="Low">Healthy / Low</option>
                            </select>
                        </div>
                        <div className="dummy-filter-row-item">
                            <span className="filter-label-txt">Primary Input Material</span>
                            <select 
                                className="filter-select-element" 
                                value={selectedMaterial} 
                                onChange={(e) => setSelectedMaterial(e.target.value)}
                            >
                                <option value="All">All Materials</option>
                                {uniqueMaterials.map(mat => (
                                    <option key={mat} value={mat}>{mat}</option>
                                ))}
                            </select>
                        </div>
                    </div>

                    <div className="quick-statistics-subpanel">
                        <h4 className="subpanel-title-label">Quick Statistics</h4>
                        <div className="quick-stats-rows-stack">
                            <div className="q-stat-row"><span>Plants Active Online</span><span className="font-mono font-semibold text-success">{plantsData.filter(p => p.status === 'Healthy').length} / {plantsData.length}</span></div>
                            <div className="q-stat-row"><span>Critical Risks Tracked</span><span className="font-mono font-semibold text-critical">{plantsData.filter(p => p.status === 'At Risk' || p.status === 'Critical').length} Plant(s)</span></div>
                            <div className="q-stat-row"><span>Materials Mapped</span><span className="font-mono font-semibold text-brand">{uniqueMaterials.length} Items</span></div>
                            <div className="q-stat-row"><span>Avg Capacity Utilization</span><span className="font-mono font-semibold text-brand">
                                {plantsData.length > 0 ? (plantsData.reduce((acc, p) => acc + p.utilization, 0) / plantsData.length).toFixed(1) : 0}%
                            </span></div>
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
                                {filteredInventory.length > 0 ? (
                                    filteredInventory.map((row, idx) => (
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
                                    ))
                                ) : (
                                    <tr>
                                        <td colSpan={8} style={{ textAlign: 'center', padding: '20px', color: 'var(--intel-text-s)' }}>
                                            No matching materials found.
                                        </td>
                                    </tr>
                                )}
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
                        {selectedPlant ? (
                            <>
                                <div className="profile-identity-header">
                                    <span className="profile-lbl">Selected Target Asset</span>
                                    <h4 className="profile-asset-title-text">{selectedPlant.name}</h4>
                                    <span className="profile-meta-subtext"><MapPin size={10} /> {selectedPlant.location} Sector Profile</span>
                                </div>

                                <div className="profile-metrics-property-list">
                                    <div className="p-property-row"><span>Production Capacity Status</span><span className="font-semibold">{selectedPlant.production} / {selectedPlant.capacity}</span></div>
                                    <div className="p-property-row"><span>Active Operating Shift</span><span className="font-mono font-semibold">Shift B - Operational Matrix</span></div>
                                    <div className="p-property-row"><span>Incoming Freight Shipments</span><span className="font-mono text-brand font-semibold">{selectedPlant.suppliers} Supplier Vectors</span></div>
                                    <div className="p-property-row"><span>Silo Buffer Inventory Level</span><span className={`font-semibold ${selectedPlant.inventoryHealth === 'Critical' ? 'text-critical' : 'text-brand'}`}>{selectedPlant.inventoryHealth} Reserve</span></div>
                                    <div className="p-property-row"><span>Estimated Shutdown Risk</span><span className={`font-semibold ${selectedPlant.status !== 'Healthy' ? 'text-critical' : 'text-success'}`}>{selectedPlant.status !== 'Healthy' ? 'High Risk Exposure' : 'Low Risk Exposure'}</span></div>
                                    <div className="p-property-row"><span>Remaining Operating Horizon</span><span className="font-mono text-brand font-semibold">{selectedPlant.remainingDays} Days</span></div>
                                </div>

                                <div className="profile-asset-connections-block">
                                    <span className="profile-lbl">Connected Asset Infrastructure</span>
                                    <div className="connections-pills-row">
                                        <span className="conn-pill"><Truck size={10} /> Inter-Modal Fleet Loop</span>
                                        <span className="conn-pill"><Factory size={10} /> Kiln Grinding Array 1</span>
                                    </div>
                                </div>
                            </>
                        ) : (
                            <div className="flex-center" style={{ padding: '24px', color: 'var(--intel-text-s)' }}>
                                Select a plant asset to view profile details.
                            </div>
                        )}
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
                            {productionTrendData && productionTrendData.length > 0 ? (
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
                            ) : (
                                <div className="no-data-placeholder" style={{ height: '100%', display: 'flex', alignItems: 'center', justifyContent: 'center', color: 'var(--intel-text-s, #7d8791)' }}>
                                    No data available
                                </div>
                            )}
                        </div>
                    </div>

                    {/* Chart 2: Bar Chart */}
                    <div className="chart-canvas-card">
                        <h4 className="chart-card-heading-title">Inventory vs Safety Thresholds (T)</h4>
                        <div className="recharts-container-element">
                            {inventoryConsumptionData && inventoryConsumptionData.length > 0 ? (
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
                            ) : (
                                <div className="no-data-placeholder" style={{ height: '100%', display: 'flex', alignItems: 'center', justifyContent: 'center', color: 'var(--intel-text-s, #7d8791)' }}>
                                    No data available
                                </div>
                            )}
                        </div>
                    </div>

                    {/* Chart 3: Radial Bar Chart */}
                    <div className="chart-canvas-card">
                        <h4 className="chart-card-heading-title">Capacity Utilization (%)</h4>
                        <div className="recharts-container-element flex-center">
                            {capacityUtilizationData && capacityUtilizationData.length > 0 ? (
                                <ResponsiveContainer width="100%" height="100%">
                                    <RadialBarChart cx="50%" cy="50%" innerRadius="30%" outerRadius="90%" barSize={12} data={capacityUtilizationData}>
                                        <RadialBar minAngle={15} background clockWise dataKey="value" cornerRadius={4} />
                                        <Tooltip />
                                    </RadialBarChart>
                                </ResponsiveContainer>
                            ) : (
                                <div className="no-data-placeholder" style={{ height: '100%', display: 'flex', alignItems: 'center', justifyContent: 'center', color: 'var(--intel-text-s, #7d8791)' }}>
                                    No data available
                                </div>
                            )}
                        </div>
                    </div>

                    {/* Chart 4: Donut Chart */}
                    <div className="chart-canvas-card">
                        <h4 className="chart-card-heading-title">Material Availability Risk Nodes</h4>
                        <div className="recharts-container-element flex-center">
                            {materialAvailabilityData && materialAvailabilityData.length > 0 ? (
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
                            ) : (
                                <div className="no-data-placeholder" style={{ height: '100%', display: 'flex', alignItems: 'center', justifyContent: 'center', color: 'var(--intel-text-s, #7d8791)' }}>
                                    No data available
                                </div>
                            )}
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
                    {aiInsights.length > 0 ? (
                        aiInsights.map((insight, idx) => (
                            <div key={idx} className={`pi-insight-action-card rank-${insight.priority ? insight.priority.toLowerCase() : ''}`}>
                                <div className="insight-card-top-header-row">
                                    <span className={`insight-priority-pill tag-${insight.priority ? insight.priority.toLowerCase() : ''}`}>
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
                                <button 
                                    className={`insight-execution-trigger btn-${insight.priority ? insight.priority.toLowerCase() : ''}`}
                                    onClick={() => handleAuthorizeAction(insight.title)}
                                >
                                    Authorize Logistics Protocols <ArrowRight size={13} />
                                </button>
                            </div>
                        ))
                    ) : (
                        <div className="pi-insight-action-card flex-center" style={{ gridColumn: '1 / -1', padding: '40px', color: 'var(--intel-text-s)' }}>
                            No operations insights generated.
                        </div>
                    )}
                </div>
            </section>

        </div>
    );
}