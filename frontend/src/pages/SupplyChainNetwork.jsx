// SupplyChainNetwork.jsx
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
                    <span className="node-lbl">Material:</span>
                    <span className="node-val truncate">{data.material}</span>
                </div>
                <div className="node-data-row">
                    <span className="node-lbl">Status:</span>
                    <span className={`node-status-txt text-${data.health}`}>{data.status}</span>
                </div>
            </div>
            <div className="node-health-bar-container">
                <span className={`node-health-fill bg-${data.health}`}></span>
            </div>
            <Handle type="source" position={Position.Bottom} className="flow-handle" />
        </div>
    );
};

const nodeTypes = { twinNode: TwinNode };

function UsersPlaceholder(props) { return <Layers {...props} />; }

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

                if (fetchedData && fetchedData.nodes && fetchedData.nodes.length > 0) {
                    setSelectedNode(fetchedData.nodes[0].data);
                }
            } catch (err) {
                console.error("Failed to fetch supply chain network data:", err);
                setError(err?.message || "Failed to load supply chain network digital twin.");
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
            <div className="twin-page-scope flex-center" style={{ minHeight: '400px' }}>
                <p>Loading Supply Chain Digital Twin Network...</p>
            </div>
        );
    }

    if (error) {
        return (
            <div className="twin-page-scope flex-center" style={{ minHeight: '400px' }}>
                <p className="text-critical">Error: {error}</p>
            </div>
        );
    }

    const kpiData = networkData?.kpis ?? [];
    const networkHealthCards = networkData?.network_health_cards ?? [];
    const nodes = networkData?.nodes ?? [];
    const edges = networkData?.edges ?? [];
    const aiActionPlans = networkData?.ai_action_plans ?? [];

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
                    const Icon = typeof kpi.icon === 'string' ? (iconMap[kpi.icon] || UsersPlaceholder) : (kpi.icon || UsersPlaceholder);
                    return (
                        <div key={kpi.id} className="twin-kpi-card">
                            <div className="twin-kpi-header">
                                <span className={`twin-kpi-icon-box color-${kpi.status}`}>
                                    <Icon size={16} />
                                </span>
                                <span className="twin-kpi-trend-txt">{kpi.trend}</span>
                            </div>
                            <div className="twin-kpi-body">
                                <h3 className="twin-kpi-card-title">{kpi.title}</h3>
                                <span className="twin-kpi-value-text">{kpi.value}</span>
                            </div>
                        </div>
                    );
                })}
            </section>

            {/* Main Framework Columns */}
            <section className="twin-workspace-layout-grid">

                {/* Left Side: Network Infrastructure Health Cards */}
                <div className="twin-side-column column-left">
                    <div className="column-header-row">
                        <h2 className="column-section-heading">Network Health Matrix</h2>
                    </div>
                    <div className="side-column-content-stack">
                        {networkHealthCards.map((card) => (
                            <div key={card.id} className="infra-status-card-item">
                                <div className="infra-card-top">
                                    <div className="infra-title-flex">
                                        <span className={`infra-status-dot bg-${card.status}`}></span>
                                        <h4 className="infra-card-label">{card.label}</h4>
                                    </div>
                                    <span className="infra-card-value font-mono">{card.val}</span>
                                </div>
                                <div className="infra-progress-track">
                                    <span className={`infra-progress-bar fill-${card.status}`} style={{ width: `${card.pct}%` }}></span>
                                </div>
                                <p className="infra-card-description">{card.desc}</p>
                            </div>
                        ))}
                    </div>
                </div>

                {/* Center Canvas: Live Map Flow Engine */}
                <div className="twin-center-visualization-column">
                    <div className="column-header-row transparent-bg">
                        <h2 className="column-section-heading">Live Supply Chain Graph Twin</h2>
                    </div>

                    <div className="react-flow-canvas-viewport">
                        <ReactFlow
                            nodes={nodes}
                            edges={edges}
                            nodeTypes={nodeTypes}
                            onNodeClick={handleNodeClick}
                            fitView
                            zoomOnScroll={false}
                            preventScrolling={true}
                            nodesConnectable={false}
                            nodesDraggable={false}
                        >
                            <Background color="#D1D5D8" gap={16} size={1} />
                            <Controls showZoom={true} showInteractive={false} className="twin-canvas-controls" />
                        </ReactFlow>

                        {/* Network Legend Canvas Overlay */}
                        <div className="twin-canvas-legend-box">
                            <h5 className="legend-main-title">Network Flow Legend</h5>
                            <div className="legend-items-grid">
                                <div className="legend-cell"><span className="legend-dot bg-success"></span><span>Healthy Node</span></div>
                                <div className="legend-cell"><span className="legend-dot bg-warning"></span><span>Warning Node</span></div>
                                <div className="legend-cell"><span className="legend-dot bg-critical"></span><span>Critical Risk</span></div>
                                <div className="legend-cell"><span className="legend-line edge-healthy"></span><span>Material Flow</span></div>
                                <div className="legend-cell"><span className="legend-line edge-alternative-dashed"></span><span>Alternative Path</span></div>
                                <div className="legend-cell"><span className="legend-line edge-transfer-blue"></span><span>Inventory Transfer</span></div>
                            </div>
                        </div>
                    </div>

                    {/* Node Interaction Details Subpanel Context View */}
                    <div className="node-interaction-details-subpanel">
                        <div className="subpanel-header">
                            <span className="subpanel-title-lbl">Selected Asset Inspection Profile:</span>
                            <h3 className="subpanel-asset-name">{selectedNode ? selectedNode.name : 'Select a Node above'}</h3>
                        </div>
                        {selectedNode ? (
                            <div className="subpanel-metrics-grid">
                                <div className="subpanel-cell"><span className="sc-lbl">Location Coordinates</span><span className="sc-val">{selectedNode.location} Sector</span></div>
                                <div className="subpanel-cell"><span className="sc-lbl">Operational Status</span><span className={`sc-val text-${selectedNode.health} font-semibold`}>{selectedNode.status}</span></div>
                                <div className="sc-long-cell"><span className="sc-lbl">Assigned Supply Material Cargo Linkage</span><span className="sc-val text-brand font-semibold">{selectedNode.material}</span></div>
                            </div>
                        ) : (
                            <p className="subpanel-fallback-text">Click any node profile configuration inside the Digital Twin canvas matrix map above to execute targeted system telemetry readings.</p>
                        )}
                    </div>
                </div>

                {/* Right Side: Prescriptive AI Actions Grid Layout */}
                <div className="twin-side-column column-right">
                    <div className="column-header-row">
                        <h2 className="column-section-heading">AI Mitigation Action Plans</h2>
                    </div>
                    <div className="side-column-content-stack">
                        {aiActionPlans.map((plan) => (
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
                        ))}
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
                        <span className="sm-val-text color-brand">4 Automated Plans Active</span>
                    </div>
                    <div className="summary-metric-block-cell">
                        <span className="sm-lbl">Materials In Transit Volume</span>
                        <span className="sm-val-text">1,450 Tons Bulk Cargo</span>
                    </div>
                    <div className="summary-metric-block-cell">
                        <span className="sm-lbl">Active Inventory Redistribution</span>
                        <span className="sm-val-text">2 Rail Corridors Engaged</span>
                    </div>
                    <div className="summary-metric-block-cell">
                        <span className="sm-lbl">Delayed Shipments Tracked</span>
                        <span className="sm-val-text color-crit font-mono">3 Freight Vectors Blocked</span>
                    </div>
                    <div className="summary-metric-block-cell">
                        <span className="sm-lbl">Estimated Network Recovery Time</span>
                        <span className="sm-val-text font-mono">2.5 Hours Calculated</span>
                    </div>
                    <div className="summary-metric-block-cell">
                        <span className="sm-lbl">Business Continuity Index Rating</span>
                        <span className="sm-val-text color-success font-semibold">94.8% System Load Stability</span>
                    </div>
                </div>
            </section>

        </div>
    );
}