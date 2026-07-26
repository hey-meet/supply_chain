// --- SupplyChainNetwork.jsx ---
import React, { useState, useEffect } from 'react';

import {
    ReactFlow,
    Background,
    Controls,
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
    const isSupplier = data.node_type === 'supplier';
    const isCustomer = data.node_type === 'customer';
    
    return (
        <div className={`twin-node-card status-${data.health}`}>
            {!isSupplier && <Handle type="target" position={Position.Left} className="flow-handle" />}
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
                {data.node_type === 'supplier' && (
                    <>
                        <div className="node-data-row">
                            <span className="nd-lbl">Daily Cap:</span>
                            <span className="nd-val">{data.capacity}</span>
                        </div>
                        <div className="node-data-row">
                            <span className="nd-lbl">Reliability:</span>
                            <span className="nd-val text-brand" style={{ color: 'var(--tw-brand)' }}>{data.reliability}</span>
                        </div>
                    </>
                )}
                {data.node_type === 'material' && (
                    <>
                        <div className="node-data-row">
                            <span className="nd-lbl">Criticality:</span>
                            <span className="nd-val text-brand" style={{ color: 'var(--tw-brand)' }}>{data.criticality}</span>
                        </div>
                        <div className="node-data-row">
                            <span className="nd-lbl">Monthly Req:</span>
                            <span className="nd-val">{data.monthly_req}</span>
                        </div>
                    </>
                )}
                {data.node_type === 'plant' && (
                    <>
                        <div className="node-data-row">
                            <span className="nd-lbl">Capacity:</span>
                            <span className="nd-val">{data.capacity}</span>
                        </div>
                        <div className="node-data-row">
                            <span className="nd-lbl">Utilization:</span>
                            <span className="nd-val text-brand" style={{ color: 'var(--tw-brand)' }}>{data.utilization}</span>
                        </div>
                    </>
                )}
                {data.node_type === 'distribution_center' && (
                    <>
                        <div className="node-data-row">
                            <span className="nd-lbl">Dispatch Cap:</span>
                            <span className="nd-val">{data.capacity}</span>
                        </div>
                        <div className="node-data-row">
                            <span className="nd-lbl">Operating Status:</span>
                            <span className={`nd-val color-${data.health}`} style={{ fontSize: '9px', fontWeight: 'bold' }}>{data.status}</span>
                        </div>
                    </>
                )}
                {data.node_type === 'customer' && (
                    <>
                        <div className="node-data-row">
                            <span className="nd-lbl">Demand Vol:</span>
                            <span className="nd-val">{data.capacity}</span>
                        </div>
                        <div className="node-data-row">
                            <span className="nd-lbl">Demand Coverage:</span>
                            <span className="nd-val text-success" style={{ fontSize: '9px', fontWeight: 'bold' }}>{data.status}</span>
                        </div>
                    </>
                )}
            </div>
            {!isCustomer && <Handle type="source" position={Position.Right} className="flow-handle" />}
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
                    <h1 className="twin-page-title">Supply Chain Network</h1>
                    <p className="twin-page-subtitle">Real-time enterprise spatial digital twin layout visualization.</p>
                </div>
                <div className="twin-header-right">
                    <div className="twin-sync-pill">
                        <Clock size={13} />
                        <span className="sync-lbl">Last Sync:</span>
                        <span className="sync-val font-mono">{liveSync}</span>
                    </div>
                    <div className="twin-assets-badge">
                        <Network size={13} />
                        <span>18 Mapped Grid Assets</span>
                    </div>
                    <div className="twin-status-tag-active">
                        <span className="twin-pulse-core"></span>
                        TWIN SIMULATION LIVE
                    </div>
                </div>
            </header>

            {/* Top KPI Summary Grid */}
            <section className="twin-kpi-grid" style={{ gridTemplateColumns: 'repeat(2, 1fr)', gap: '20px', marginBottom: '24px' }}>
                {kpiData.map((kpi) => {
                    const Icon = typeof kpi.icon === 'string' ? (iconMap[kpi.icon] || Layers) : (kpi.icon || Layers);
                    return (
                        <div key={kpi.id} className="twin-kpi-card" style={{ padding: '16px', backgroundColor: 'var(--tw-card)', border: '1px solid var(--tw-border)', borderRadius: '12px' }}>
                            <div className="kpi-header-flex" style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', width: '100%' }}>
                                <span className={`kpi-icon-wrapper color-${kpi.status}`} style={{ width: '28px', height: '28px', borderRadius: '4px', display: 'flex', alignItems: 'center', justifyContent: 'center', backgroundColor: kpi.status === 'success' ? 'rgba(112, 140, 114, 0.15)' : 'rgba(200, 166, 82, 0.15)' }}>
                                    <Icon size={16} />
                                </span>
                                <span className={`kpi-trend-lbl text-${kpi.status}`} style={{ fontSize: '11px', fontWeight: '600' }}>{kpi.trend}</span>
                            </div>
                            <div className="kpi-meta-block" style={{ marginTop: '12px', textAlign: 'left' }}>
                                <span className="kpi-lbl" style={{ fontSize: '13px', color: 'var(--tw-text-s)' }}>{kpi.title}</span>
                                <h3 className="kpi-val-text" style={{ fontSize: '24px', margin: '4px 0 0 0', fontWeight: '700' }}>{kpi.value}</h3>
                            </div>
                        </div>
                    );
                })}
            </section>

            {/* Main Interactive Diagram Grid */}
            <section className="twin-diagram-workspace-grid" style={{ display: 'grid', gridTemplateColumns: '1.8fr 1fr', gap: '24px', width: '100%', alignItems: 'stretch' }}>

                {/* Left Side: ReactFlow Canvas Frame */}
                <div className="twin-diagram-container" style={{ position: 'relative', border: '1px solid var(--tw-border)', borderRadius: '18px', overflow: 'hidden', height: '560px', minHeight: '560px', backgroundColor: '#fafafa' }}>
                    <div className="diagram-header-overlay" style={{ padding: '12px 16px', borderBottom: '1px solid var(--tw-border)', backgroundColor: '#ffffff', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                        <span className="dh-lbl" style={{ fontWeight: '700', fontSize: '13px', color: 'var(--tw-brand)' }}>Enterprise Spatial Digital Twin Canvas</span>
                        <span className="dh-helper-txt" style={{ fontSize: '11px', color: 'var(--tw-text-s)' }}>Select any graph node from the digital twin canvas to inspect live telemetry.</span>
                    </div>

                    <div style={{ width: '100%', height: 'calc(100% - 44px)', minHeight: '400px' }}>
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
                            <Background color="#ECEFF1" gap={16} size={1.2} />
                            <Controls showInteractive={false} className="rf-controls-panel" style={{ bottom: '20px', right: '20px', left: 'auto' }} />
                        </ReactFlow>
                    </div>
                </div>

                {/* Right Column Sidebar Panels */}
                <div className="twin-sidebar-column" style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>

                    {/* Node Inspection Details Profiler */}
                    <div className="twin-sidebar-card" style={{ backgroundColor: 'var(--tw-card)', border: '1px solid var(--tw-border)', borderRadius: '18px', padding: '20px', boxShadow: 'var(--tw-shadow)', textAlign: 'left' }}>
                        <div className="column-header-row" style={{ borderBottom: '1px solid var(--tw-border)', paddingBottom: '10px', marginBottom: '16px' }}>
                            <h2 className="column-section-heading" style={{ fontSize: '18px', fontWeight: '700', color: 'var(--tw-brand)' }}>Active Telemetry Inspector</h2>
                        </div>
                        <div className="node-profile-body">
                            {selectedNode ? (
                                <>
                                    <div className="np-header-block" style={{ marginBottom: '16px' }}>
                                        <h3 className="np-title" style={{ margin: '0 0 4px 0', fontSize: '15px', fontWeight: '700', color: 'var(--tw-text-p)' }}>{selectedNode.name}</h3>
                                        <span className="np-loc" style={{ fontSize: '11px', color: 'var(--tw-text-s)', display: 'inline-flex', alignItems: 'center', gap: '4px' }}><Globe size={11} /> {selectedNode.location} Node Profile</span>
                                    </div>
                                    <div className="np-properties-list" style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
                                        <div className="np-prop-row" style={{ display: 'flex', justifyContent: 'space-between', fontSize: '12px', borderBottom: '1px solid var(--tw-bg-p)', paddingBottom: '6px' }}>
                                            <span>Asset Class Type</span>
                                            <strong className="text-brand" style={{ textTransform: 'uppercase', color: 'var(--tw-brand)' }}>{selectedNode.node_type?.replace('_', ' ')}</strong>
                                        </div>
                                        <div className="np-prop-row" style={{ display: 'flex', justifyContent: 'space-between', fontSize: '12px', borderBottom: '1px solid var(--tw-bg-p)', paddingBottom: '6px' }}>
                                            <span>Operating Health</span>
                                            <span className={`np-status-lbl color-${selectedNode.health}`} style={{ fontWeight: 'bold', color: selectedNode.health === 'critical' ? 'var(--tw-critical)' : (selectedNode.health === 'warning' ? 'var(--tw-warning)' : 'var(--tw-success)') }}>{selectedNode.health?.toUpperCase()}</span>
                                        </div>
                                        
                                        {/* Conditional properties based on type */}
                                        {selectedNode.node_type === 'supplier' && (
                                            <>
                                                <div className="np-prop-row" style={{ display: 'flex', justifyContent: 'space-between', fontSize: '12px', borderBottom: '1px solid var(--tw-bg-p)', paddingBottom: '6px' }}><span>Sourced Feedstock</span><strong>{selectedNode.material}</strong></div>
                                                <div className="np-prop-row" style={{ display: 'flex', justifyContent: 'space-between', fontSize: '12px', borderBottom: '1px solid var(--tw-bg-p)', paddingBottom: '6px' }}><span>Daily Output Cap</span><strong>{selectedNode.capacity}</strong></div>
                                                <div className="np-prop-row" style={{ display: 'flex', justifyContent: 'space-between', fontSize: '12px', borderBottom: '1px solid var(--tw-bg-p)', paddingBottom: '6px' }}><span>Supplier Reliability</span><strong className="text-brand" style={{ color: 'var(--tw-brand)' }}>{selectedNode.reliability}</strong></div>
                                                <div className="np-prop-row" style={{ display: 'flex', justifyContent: 'space-between', fontSize: '12px', borderBottom: '1px solid var(--tw-bg-p)', paddingBottom: '6px' }}><span>Transit Lead Time</span><span>{selectedNode.lead_time}</span></div>
                                                <div className="np-prop-row" style={{ display: 'flex', justifyContent: 'space-between', fontSize: '12px', borderBottom: '1px solid var(--tw-bg-p)', paddingBottom: '6px' }}><span>Preferred Transport</span><span>{selectedNode.transport}</span></div>
                                            </>
                                        )}
                                        
                                        {selectedNode.node_type === 'material' && (
                                            <>
                                                <div className="np-prop-row" style={{ display: 'flex', justifyContent: 'space-between', fontSize: '12px', borderBottom: '1px solid var(--tw-bg-p)', paddingBottom: '6px' }}><span>Criticality Level</span><strong className="text-brand" style={{ color: 'var(--tw-brand)' }}>{selectedNode.criticality}</strong></div>
                                                <div className="np-prop-row" style={{ display: 'flex', justifyContent: 'space-between', fontSize: '12px', borderBottom: '1px solid var(--tw-bg-p)', paddingBottom: '6px' }}><span>Monthly Requirement</span><strong>{selectedNode.monthly_req}</strong></div>
                                                <div className="np-prop-row" style={{ display: 'flex', justifyContent: 'space-between', fontSize: '12px', borderBottom: '1px solid var(--tw-bg-p)', paddingBottom: '6px' }}><span>Associated Feedstock</span><span>{selectedNode.material}</span></div>
                                            </>
                                        )}
                                        
                                        {selectedNode.node_type === 'plant' && (
                                            <>
                                                <div className="np-prop-row" style={{ display: 'flex', justifyContent: 'space-between', fontSize: '12px', borderBottom: '1px solid var(--tw-bg-p)', paddingBottom: '6px' }}><span>Manufacturing Focus</span><strong>{selectedNode.material}</strong></div>
                                                <div className="np-prop-row" style={{ display: 'flex', justifyContent: 'space-between', fontSize: '12px', borderBottom: '1px solid var(--tw-bg-p)', paddingBottom: '6px' }}><span>Daily Kiln Capacity</span><strong>{selectedNode.capacity}</strong></div>
                                                <div className="np-prop-row" style={{ display: 'flex', justifyContent: 'space-between', fontSize: '12px', borderBottom: '1px solid var(--tw-bg-p)', paddingBottom: '6px' }}><span>Asset Utilization</span><strong className="text-brand" style={{ color: 'var(--tw-brand)' }}>{selectedNode.utilization}</strong></div>
                                                <div className="np-prop-row" style={{ display: 'flex', justifyContent: 'space-between', fontSize: '12px', borderBottom: '1px solid var(--tw-bg-p)', paddingBottom: '6px' }}><span>Active Production Lines</span><span>{selectedNode.lines}</span></div>
                                            </>
                                        )}
                                        
                                        {selectedNode.node_type === 'distribution_center' && (
                                            <>
                                                <div className="np-prop-row" style={{ display: 'flex', justifyContent: 'space-between', fontSize: '12px', borderBottom: '1px solid var(--tw-bg-p)', paddingBottom: '6px' }}><span>Material Dispatched</span><strong>{selectedNode.material}</strong></div>
                                                <div className="np-prop-row" style={{ display: 'flex', justifyContent: 'space-between', fontSize: '12px', borderBottom: '1px solid var(--tw-bg-p)', paddingBottom: '6px' }}><span>Dispatch Capacity</span><strong>{selectedNode.capacity}</strong></div>
                                                <div className="np-prop-row" style={{ display: 'flex', justifyContent: 'space-between', fontSize: '12px', borderBottom: '1px solid var(--tw-bg-p)', paddingBottom: '6px' }}><span>Supported Markets</span><span style={{ fontSize: '11px', textAlign: 'right' }}>{selectedNode.regions}</span></div>
                                            </>
                                        )}
                                        
                                        {selectedNode.node_type === 'customer' && (
                                            <>
                                                <div className="np-prop-row" style={{ display: 'flex', justifyContent: 'space-between', fontSize: '12px', borderBottom: '1px solid var(--tw-bg-p)', paddingBottom: '6px' }}><span>Commercial Demand</span><strong>{selectedNode.capacity}</strong></div>
                                                <div className="np-prop-row" style={{ display: 'flex', justifyContent: 'space-between', fontSize: '12px', borderBottom: '1px solid var(--tw-bg-p)', paddingBottom: '6px' }}><span>Served Areas</span><span style={{ fontSize: '11px', textAlign: 'right' }}>{selectedNode.regions}</span></div>
                                                <div className="np-prop-row" style={{ display: 'flex', justifyContent: 'space-between', fontSize: '12px', borderBottom: '1px solid var(--tw-bg-p)', paddingBottom: '6px' }}><span>Demand Coverage</span><span className="text-success">{selectedNode.status}</span></div>
                                            </>
                                        )}
                                        
                                        <div className="np-prop-row" style={{ display: 'flex', justifyContent: 'space-between', fontSize: '12px', paddingTop: '4px' }}>
                                            <span>Operational Status</span>
                                            <span style={{ fontWeight: 'bold', color: selectedNode.health === 'critical' ? 'var(--tw-critical)' : (selectedNode.health === 'warning' ? 'var(--tw-warning)' : 'var(--tw-success)') }}>{selectedNode.status}</span>
                                        </div>
                                    </div>
                                </>
                            ) : (
                                <p style={{ color: 'var(--intel-text-s)', textAlign: 'center', padding: '20px', fontSize: '12.5px' }}>Select any graph node from the digital twin canvas to inspect live telemetry.</p>
                            )}
                        </div>
                    </div>

                    {/* Network Segment Health Metrics */}
                    <div className="twin-sidebar-card" style={{ backgroundColor: 'var(--tw-card)', border: '1px solid var(--tw-border)', borderRadius: '18px', padding: '20px', boxShadow: 'var(--tw-shadow)' }}>
                        <div className="column-header-row" style={{ borderBottom: '1px solid var(--tw-border)', paddingBottom: '10px', marginBottom: '16px', textAlign: 'left' }}>
                            <h2 className="column-section-heading" style={{ fontSize: '18px', fontWeight: '700', color: 'var(--tw-brand)' }}>Network Segment Health</h2>
                        </div>
                        <div className="segment-health-cards-stack" style={{ display: 'flex', flexDirection: 'column', gap: '14px' }}>
                            {networkHealthCards.map((card) => (
                                <div key={card.id} className="segment-health-card-item" style={{ textAlign: 'left' }}>
                                    <div className="sh-header-row" style={{ display: 'flex', justifyContent: 'space-between', fontSize: '13px', marginBottom: '6px' }}>
                                        <span className="sh-lbl-title" style={{ fontWeight: '600' }}>{card.label}</span>
                                        <strong className={`sh-val-pct text-${card.status}`} style={{ color: card.status === 'critical' ? 'var(--tw-critical)' : (card.status === 'warning' ? 'var(--tw-warning)' : 'var(--tw-success)') }}>{card.val}</strong>
                                    </div>
                                    <div className="sh-progress-track-frame" style={{ width: '100%', height: '5px', backgroundColor: 'var(--tw-surf)', borderRadius: '3px', overflow: 'hidden', marginBottom: '6px' }}>
                                        <span className={`sh-progress-fill-element fill-${card.status}`} style={{ display: 'block', height: '100%', width: `${card.pct}%`, backgroundColor: card.status === 'critical' ? 'var(--tw-critical)' : (card.status === 'warning' ? 'var(--tw-warning)' : 'var(--tw-success)') }}></span>
                                    </div>
                                    <span className="sh-desc-txt" style={{ fontSize: '11px', color: 'var(--tw-text-s)' }}>{card.desc}</span>
                                </div>
                            ))}
                        </div>
                    </div>

                    {/* AI Mitigation Action Plans List */}
                    <div className="twin-sidebar-card border-none bg-none shadow-none" style={{ textAlign: 'left' }}>
                        <div className="column-header-row" style={{ borderBottom: '1px solid var(--tw-border)', paddingBottom: '10px', marginBottom: '16px' }}>
                            <h2 className="column-section-heading" style={{ fontSize: '18px', fontWeight: '700', color: 'var(--tw-brand)' }}>AI Mitigation Action Plans</h2>
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
                                <div style={{ color: 'var(--intel-text-s)', textAlign: 'center', padding: '16px', fontSize: '12px' }}>No active action plans compiled.</div>
                            )}
                        </div>
                    </div>

                </div>

            </section>

            {/* Bottom Section Component Panels */}
            <section className="twin-bottom-flow-summary-panel" style={{ marginTop: '32px', backgroundColor: 'var(--tw-card)', border: '1px solid var(--tw-border)', borderRadius: '18px', padding: '24px', boxShadow: 'var(--tw-shadow)' }}>
                <div className="column-header-row no-margin border-none" style={{ textAlign: 'left', borderBottom: 'none', marginBottom: '0' }}>
                    <div className="bottom-title-wrapper-flex" style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                        <ShieldCheck size={16} className="color-brand" />
                        <h2 className="column-section-heading" style={{ fontSize: '18px', fontWeight: '700', color: 'var(--tw-brand)' }}>Autonomous Material Redistribution & Operational Balance Metrics</h2>
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