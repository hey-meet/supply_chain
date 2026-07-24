// --- SupplyChainNetwork.jsx ---
import React, { useState, useEffect } from 'react';

import {
    ReactFlow,
    Background,
    Controls,
    MarkerType,
    Handle,
    Position
} from '@xyflow/react';

import '@xyflow/react/dist/style.css';

import {
    Activity,
    Layers,
    Factory,
    Package,
    Route,
    Truck,
    Globe,
    Clock,
    Network,
    AlertTriangle,
    CheckCircle2,
    HelpCircle,
    TrendingUp,
    Cpu,
    CornerDownRight,
    ShieldCheck
} from 'lucide-react';
import networkService from "../services/networkService";
import '../styles/supply-chain-network.css';

// Icon Map for dynamic icon lookup from string values
const iconMap = {
    Activity,
    Layers,
    Factory,
    Package,
    Route,
    Truck,
    Globe,
    Clock,
    Network,
    AlertTriangle,
    CheckCircle2,
    TrendingUp,
    Cpu,
    ShieldCheck
};

// Custom Node Component
const TwinNode = ({ data }) => {
    const Icon = typeof data.icon === 'function' ? data.icon : (iconMap[data.icon] || Layers);
    return (
        <div className={`twin-node-card status-${data.health}`}>
            <Handle type="target" position={Position.Top} className="flow-handle" />
            <div className="twin-node-header">
                <span className={`node-icon-wrapper color-${data.health}`}>
                    <Icon size={14} />
                </span>
                <div className="node-title-block">
                    <h4 className="node-name">{data.name}</h4>
                    <span className="node-loc">{data.location}</span>
                </div>
            </div>
            <div className="twin-node-body">
                <div className="node-data-row">
                    <span className="nd-lbl">Core Feedstock:</span>
                    <span className="nd-val">{data.material}</span>
                </div>
                <div className="node-data-row">
                    <span className="nd-lbl">Operating Status:</span>
                    <span className={`nd-val color-${data.health}`}>{data.status}</span>
                </div>
            </div>
            <Handle type="source" position={Position.Bottom} className="flow-handle" />
        </div>
    );
};

const nodeTypes = {
    twinNode: TwinNode
};

export default function SupplyChainNetwork() {
    const [liveSync, setLiveSync] = useState('14:17:02');
    const [selectedNode, setSelectedNode] = useState(null);

    const [networkData, setNetworkData] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        const fetchNetworkData = async () => {
            try {
                setLoading(true);
                setError(null);
                const response = await networkService.getSupplyChainNetwork();
                if (response && response.success) {
                    const fetchedData = response.data;

                    // Process nodes to attach corresponding Lucide icon components if string provided
                    if (fetchedData && fetchedData.nodes) {
                        fetchedData.nodes = fetchedData.nodes.map((node) => ({
                            ...node,
                            data: {
                                ...node.data,
                                icon: typeof node.data.icon === 'string' ? (iconMap[node.data.icon] || Layers) : node.data.icon
                            }
                        }));
                    }

                    setNetworkData(fetchedData);
                    setError(null);

                    if (fetchedData && fetchedData.nodes && fetchedData.nodes.length > 0) {
                        setSelectedNode(fetchedData.nodes[0].data);
                    }
                } else {
                    setError(new Error(response?.message || "Failed to load supply chain network digital twin."));
                }
            } catch (err) {
                console.error("Failed to fetch supply chain network data:", err);
                setError(err);
            } finally {
                setLoading(false);
            }
        };

        fetchNetworkData();
    }, []);

    useEffect(() => {
        const timer = setInterval(() => {
            const now = new Date();
            setLiveSync(now.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', second: '2-digit' }));
        }, 1000);
        return () => clearInterval(timer);
    }, []);

    const handleNodeClick = (event, node) => {
        if (node && node.data) {
            setSelectedNode(node.data);
        }
    };

    if (loading) {
        return (
            <div className="twin-page-scope flex-center" style={{ minHeight: '400px', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                <p style={{ color: 'var(--intel-text-s)' }}>Loading Supply Chain Digital Twin Network...</p>
            </div>
        );
    }

    if (error && (!networkData || !networkData.nodes)) {
        const message = error.message || "";
        if (message.includes("pending") || message.includes("Initialize") || message.includes("query") || message.includes("execute") || message.includes("first")) {
            return (
                <div className="twin-page-scope flex-center-pending" style={{ minHeight: '500px', display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', gap: '16px', padding: '40px' }}>
                    <h1 className="twin-page-title">Supply Chain Digital Twin</h1>
                    <div className="alert-badge critical" style={{ background: 'var(--intel-critical)', color: 'white', padding: '8px 16px', borderRadius: '6px', fontWeight: 'bold' }}>NO ACTIVE SIMULATION</div>
                    <p style={{ color: 'var(--intel-text-s)', fontSize: '15px', maxWidth: '500px', textAlign: 'center', marginTop: '10px' }}>
                        No active supply chain simulation found. Please head to the <strong>News Intelligence</strong> tab to execute an incident search query.
                    </p>
                </div>
            );
        }
        return (
            <div className="twin-page-scope flex-center" style={{ minHeight: '400px', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                <p className="text-critical">Error: {message}</p>
            </div>
        );
    }

    const kpiData = networkData?.kpis ?? [];
    const networkHealthCards = networkData?.network_health_cards ?? [];
    const nodes = networkData?.nodes ?? [];
    const edges = networkData?.edges ?? [];
    const aiActionPlans = networkData?.ai_action_plans ?? [];
    const bottomMetrics = networkData?.bottom_metrics ?? {};

    return (
        <div className="twin-page-scope">

            {/* Header Viewport Block */}
            <header className="twin-header-block">
                <div className="twin-header-left">
                    <h1 className="twin-page-title">Supply Chain Digital Twin</h1>
                    <p className="twin-page-subtitle">Real-time AI visualization of the enterprise supply chain network.</p>
                </div>
                <div className="twin-header-right">
                    <div className="twin-sync-pill">
                        <Clock size={13} />
                        <span className="sync-lbl">Last Sync:</span>
                        <span className="sync-val font-mono">{liveSync}</span>
                    </div>
                    <div className="twin-assets-badge">
                        <Network size={13} />
                        <span>128 Connected Assets</span>
                    </div>
                    <div className="twin-status-tag-active">
                        <span className="twin-pulse-core"></span>
                        TWIN SIMULATION LIVE
                    </div>
                </div>
            </header>

            {/* Top 6 KPI Rows */}
            <section className="twin-kpi-grid">
                {kpiData.map((kpi) => {
                    const Icon = typeof kpi.icon === 'string' ? (iconMap[kpi.icon] || Layers) : (kpi.icon || Layers);
                    return (
                        <div key={kpi.id} className="twin-kpi-card">
                            <div className="kpi-header-flex">
                                <span className={`kpi-icon-wrapper color-${kpi.status}`}>
                                    <Icon size={16} />
                                </span>
                                <span className={`kpi-trend-lbl text-${kpi.status}`}>{kpi.trend}</span>
                            </div>
                            <div className="kpi-meta-block">
                                <span className="kpi-lbl">{kpi.title}</span>
                                <h3 className="kpi-val-text">{kpi.value}</h3>
                            </div>
                        </div>
                    );
                })}
            </section>

            {/* Main Interactive Diagram Grid */}
            <section className="twin-diagram-workspace-grid">

                {/* Left Side: ReactFlow Canvas Frame */}
                <div className="twin-diagram-container">
                    <div className="diagram-header-overlay">
                        <span className="dh-lbl">Enterprise Spatial Digital Twin Canvas</span>
                        <span className="dh-helper-txt">Use wheel to zoom. Click node to inspect details.</span>
                    </div>
                    <div style={{ width: '100%', height: '100%', minHeight: '400px' }}>
                        <ReactFlow
                            nodes={nodes}
                            edges={edges}
                            nodeTypes={nodeTypes}
                            onNodeClick={handleNodeClick}
                            fitView
                            maxZoom={1.5}
                            minZoom={0.5}
                            proOptions={{ hideAttribution: true }}
                        >
                            <Background color="#ECEFF1" gap={16} size={1} />
                            <Controls showInteractive={false} className="rf-controls-panel" />
                        </ReactFlow>
                    </div>
                </div>

                {/* Right Column Sidebar Panels */}
                <div className="twin-sidebar-column">

                    {/* Node Inspection Details Profiler */}
                    <div className="twin-sidebar-card">
                        <div className="column-header-row">
                            <h2 className="column-section-heading">Active Node Inspector</h2>
                        </div>
                        <div className="node-profile-body">
                            {selectedNode ? (
                                <>
                                    <div className="np-header-block">
                                        <h3 className="np-title">{selectedNode.name}</h3>
                                        <span className="np-loc"><Globe size={11} /> {selectedNode.location} Node Profile</span>
                                    </div>
                                    <div className="np-properties-list">
                                        <div className="np-prop-row"><span>Material Focus Allocation</span><strong className="text-brand">{selectedNode.material}</strong></div>
                                        <div className="np-prop-row"><span>Logistics Output Health</span><span className={`np-status-lbl color-${selectedNode.health}`}>{selectedNode.status}</span></div>
                                        <div className="np-prop-row"><span>Silo Buffer Horizon</span><span className="font-mono">8.8 Operating Days</span></div>
                                        <div className="np-prop-row"><span>Connected Supply Vectors</span><span>4 Active Routes Mapped</span></div>
                                    </div>
                                    <div className="np-connections-block-pills">
                                        <span className="connections-lbl">Connected Corridors</span>
                                        <div className="connections-flex-pills-row">
                                            <span className="conn-pill-item"><Truck size={10} /> Gujarat Rail Bypass</span>
                                            <span className="conn-pill-item"><Route size={10} /> State Line bypass</span>
                                        </div>
                                    </div>
                                </>
                            ) : (
                                <p style={{ color: 'var(--intel-text-s)', textAlign: 'center', padding: '20px' }}>Select any graph node from the digital twin canvas to inspect live telemetry.</p>
                            )}
                        </div>
                    </div>

                    {/* Network Segment Health Metrics */}
                    <div className="twin-sidebar-card">
                        <div className="column-header-row">
                            <h2 className="column-section-heading">Network Segment Health</h2>
                        </div>
                        <div className="segment-health-cards-stack">
                            {networkHealthCards.map((card) => (
                                <div key={card.id} className="segment-health-card-item">
                                    <div className="sh-header-row">
                                        <span className="sh-lbl-title">{card.label}</span>
                                        <strong className={`sh-val-pct text-${card.status}`}>{card.val}</strong>
                                    </div>
                                    <div className="sh-progress-track-frame">
                                        <span className={`sh-progress-fill-element fill-${card.status}`} style={{ width: `${card.pct}%` }}></span>
                                    </div>
                                    <span className="sh-desc-txt">{card.desc}</span>
                                </div>
                            ))}
                        </div>
                    </div>

                    {/* AI Mitigation Action Plans List */}
                    <div className="twin-sidebar-card border-none bg-none shadow-none">
                        <div className="column-header-row">
                            <h2 className="column-section-heading">AI Mitigation Action Plans</h2>
                        </div>
                        <div className="side-column-content-stack">
                            {aiActionPlans.length > 0 ? (
                                aiActionPlans.map((plan) => (
                                    <div key={plan.id} className={`action-plan-recommendation-card type-${plan.priority ? plan.priority.toLowerCase() : ''}`}>
                                        <div className="plan-card-top-row">
                                            <span className={`plan-priority-tag tag-${plan.priority ? plan.priority.toLowerCase() : ''}`}>{plan.priority} Priority</span>
                                            <span className="plan-agent-owner"><Cpu size={10} /> {plan.agent}</span>
                                        </div>
                                        <h3 className="plan-card-action-title">{plan.action}</h3>
                                        <div className="plan-card-parameters-grid">
                                            <div className="plan-param-cell"><span className="pp-lbl">Est. Delay</span><span className="pp-val color-crit font-mono">{plan.delay}</span></div>
                                            <div className="plan-param-cell"><span className="pp-lbl">Overhead Variance</span><span className="pp-val font-mono">{plan.cost}</span></div>
                                        </div>
                                        <div className="plan-card-impact-statement">
                                            <span className="pp-lbl">Targeted Impact Direction:</span>
                                            <p className="plan-impact-text-paragraph">{plan.impact}</p>
                                        </div>
                                        <div className="plan-card-footer-metrics">
                                            <span>Confidence rating: <strong>{plan.conf}</strong></span>
                                            <span>Target: <strong>{plan.time}</strong></span>
                                        </div>
                                    </div>
                                ))
                            ) : (
                                <div style={{ color: 'var(--intel-text-s)', textAlign: 'center', padding: '16px' }}>No active action plans compiled.</div>
                            )}
                        </div>
                    </div>

                </div>

            </section>

            {/* Bottom Section Component Panels */}
            <section className="twin-bottom-flow-summary-panel">
                <div className="column-header-row no-margin border-none">
                    <div className="bottom-title-wrapper-flex">
                        <ShieldCheck size={16} className="color-brand" />
                        <h2 className="column-section-heading">Autonomous Material Redistribution & Operational Balance Metrics</h2>
                    </div>
                </div>
                <div className="summary-metrics-fluid-row">
                    <div className="summary-metric-block-cell">
                        <span className="sm-lbl">Current Network Transfers</span>
                        <span className="sm-val-text color-brand">{bottomMetrics.network_transfers || "N/A"}</span>
                    </div>
                    <div className="summary-metric-block-cell">
                        <span className="sm-lbl">Materials In Transit Volume</span>
                        <span className="sm-val-text">{bottomMetrics.materials_in_transit || "N/A"}</span>
                    </div>
                    <div className="summary-metric-block-cell">
                        <span className="sm-lbl">Active Inventory Redistribution</span>
                        <span className="sm-val-text">{bottomMetrics.inventory_redistribution || "N/A"}</span>
                    </div>
                    <div className="summary-metric-block-cell">
                        <span className="sm-lbl">Delayed Shipments Tracked</span>
                        <span className="sm-val-text color-crit font-mono">{bottomMetrics.delayed_shipments || "N/A"}</span>
                    </div>
                    <div className="summary-metric-block-cell">
                        <span className="sm-lbl">Estimated Network Recovery Time</span>
                        <span className="sm-val-text font-mono">{bottomMetrics.network_recovery_time || "N/A"}</span>
                    </div>
                    <div className="summary-metric-block-cell">
                        <span className="sm-lbl">Business Continuity Index Rating</span>
                        <span className="sm-val-text color-success font-semibold">{bottomMetrics.continuity_index || "N/A"}</span>
                    </div>
                </div>
            </section>

        </div>
    );
}