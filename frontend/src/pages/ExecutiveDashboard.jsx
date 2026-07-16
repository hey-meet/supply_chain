// ExecutiveDashboard.jsx
import React, { useState, useEffect } from 'react';
import {
    Activity,
    AlertTriangle,
    Factory,
    Package,
    Route,
    Users,
    Newspaper,
    Globe,
    Cpu,
    CheckCircle2,
    Clock,
    FileText,
    TrendingUp,
    TrendingDown,
    ArrowRight,
    RefreshCw
} from 'lucide-react';
import '../styles/executive-dashboard.css';

const kpiData = [
    { id: 1, title: 'Supply Chain Health', value: '95%', type: 'circular', status: 'success', trend: '+1.2%', up: true, icon: Activity },
    { id: 2, title: 'Active Incidents', value: '8', type: 'badge', status: 'critical', trend: '+2 today', up: true, icon: AlertTriangle },
    { id: 3, title: 'Plants Online', value: '6 / 7', type: 'text', status: 'success', trend: 'Normal', up: true, icon: Factory },
    { id: 4, title: 'Inventory Health', value: '84%', type: 'text', status: 'warning', trend: '-2.4%', up: false, icon: Package },
    { id: 5, title: 'Critical Routes', value: '12', type: 'text', status: 'orange', trend: '+3 critical', up: true, icon: Route },
    { id: 6, title: 'Affected Suppliers', value: '5', type: 'text', status: 'critical', trend: '+1 new', up: true, icon: Users }
];

const newsIntelligence = [
    { id: 1, severity: 'critical', title: 'Port of Houston Intermittent Rail Gridlock', source: 'Reuters Logistics', time: '14 mins ago', confidence: '98%', location: 'Houston Hub', summary: 'Severe weather events combined with equipment failures have created an operational logjam, impacting all inbound container freight destined for Midwest distribution points.' },
    { id: 2, severity: 'warning', title: 'Limestone Quarry Delays Near Plant B', source: 'Internal Telemetry', time: '32 mins ago', confidence: '94%', location: 'Region 4', summary: 'Unscheduled hydraulic crusher maintenance has restricted raw rock output to 60% capacity. Buffer stock is currently mitigating downstream impacts.' },
    { id: 3, severity: 'critical', title: 'Regional Flash Flooding Cuts Off Route 10', source: 'NOAA Weather Advisory', time: '1 hr ago', confidence: '99%', location: 'Sector Southwest', summary: 'Flash floods have overwhelmed the lower overpass infrastructure on Route 10, requiring immediate rerouting of all class-8 cement bulk carriers.' },
    { id: 4, severity: 'warning', title: 'Coal Spot Prices Surge by 14% Nationally', source: 'Bloomberg Energy', time: '2 hrs ago', confidence: '96%', location: 'Global Markets', summary: 'Sudden export restrictions coupled with localized grid spikes have driven solid fuel raw costs upward, threatening margins across thermal-heavy kilns.' },
    { id: 5, severity: 'success', title: 'Alternative Rail Segment Reopened Safely', source: 'BNSF Dispatch', time: '3 hrs ago', confidence: '97%', location: 'Midwest Corridor', summary: 'Engineering inspections are finalized ahead of schedule. Normal track speeds restored for secondary clinker distribution trains.' },
    { id: 6, severity: 'warning', title: 'Supplier Shutdown Threat in Eastern Grid', source: 'Gov Threat Alert', time: '4 hrs ago', confidence: '89%', location: 'Zone East', summary: 'Labor renegotiations have stalled at a primary packaging materials plant. Contingency logistics brokers are being briefed on emergency alternatives.' }
];

const disruptionMarkers = [
    { id: 1, type: 'Flood', top: '42%', left: '28%', label: 'R-10 Flood', status: 'critical' },
    { id: 2, type: 'Road Closure', top: '58%', left: '48%', label: 'Route 44 Closed', status: 'critical' },
    { id: 3, type: 'Rail Delay', top: '31%', left: '62%', label: 'Houston Rail Block', status: 'warning' },
    { id: 4, type: 'Port Congestion', top: '72%', left: '76%', label: 'Port Hold', status: 'warning' }
];

const agentPipeline = [
    { id: 1, name: 'News Intelligence', status: 'Running', confidence: '98%', time: '1.2s', task: 'Collecting logistics news' },
    { id: 2, name: 'Supply Chain Impact', status: 'Running', confidence: '96%', time: '0.9s', task: 'Calculating business impact' },
    { id: 3, name: 'Mitigation Planning', status: 'Ready', confidence: '99%', time: '0.7s', task: 'Generating recommendations' }
];

const systemTimeline = [
    { id: 1, time: '14:02:11', event: 'Executive Report Ready', status: 'success', desc: 'Comprehensive disruption response plan compiled and formatted for executive signature.' },
    { id: 2, time: '14:01:45', event: 'Mitigation Generated', status: 'success', desc: 'AI multi-variable optimization engine finalized alternative sourcing pathways.' },
    { id: 3, time: '14:00:30', event: 'Inventory Assessment', status: 'warning', desc: 'Automated warehouse queries completed across all localized silos.' },
    { id: 4, time: '13:58:12', event: 'Supplier Mapping', status: 'success', desc: 'Alternative provider networks cross-referenced against historical lead-times.' }
];

const aiRecommendations = [
    { id: 1, priority: 'Critical', title: 'Activate alternate limestone supplier', impact: 'Avoid Plant A shutdown', delay: '2 hours', confidence: '97%', action: 'Transfer inventory from Plant C' },
    { id: 2, priority: 'High', title: 'Reroute Class-8 carriers to Secondary Bypass', impact: 'Mitigate Route 10 flood', delay: '45 mins', confidence: '94%', action: 'Deploy updated manifests via logistics edge' },
    { id: 3, priority: 'Medium', title: 'Secure forward energy blocks for Kiln 4', impact: 'Hedging coal price spikes', delay: 'None', confidence: '91%', action: 'Execute automated optionality clauses' },
    { id: 4, priority: 'Low', title: 'Adjust dispatch pacing for fly ash barges', impact: 'Optimize lock queue wait', delay: '12 hours', confidence: '88%', action: 'Throttle terminal loading rates dynamically' }
];

export default function ExecutiveDashboard() {
    const [timeStr, setTimeStr] = useState('13:01:06');

    useEffect(() => {
        const updateTime = () => {
            const now = new Date();
            setTimeStr(now.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', second: '2-digit' }));
        };
        updateTime();
        const interval = setInterval(updateTime, 1000);
        return () => clearInterval(interval);
    }, []);

    return (
        <div className="dashboard-content-scope">
            <header className="dashboard-header-block">
                <div className="header-meta-left">
                    <h1 className="page-main-title">Executive Dashboard</h1>
                    <p className="page-main-subtitle">Real-time AI-powered supply chain monitoring and decision intelligence.</p>
                </div>
                <div className="header-meta-right">
                    <div className="system-timestamp">
                        <span className="ts-lbl">Last Updated:</span>
                        <span className="ts-val">{timeStr}</span>
                    </div>
                    <div className="system-live-badge">
                        <span className="live-pulse-dot"></span>
                        LIVE MONITORING ACTIVE
                    </div>
                </div>
            </header>

            <section className="dashboard-kpi-grid">
                {kpiData.map((kpi) => {
                    const Icon = kpi.icon;
                    return (
                        <div key={kpi.id} className="fluid-kpi-card">
                            <div className="kpi-card-header">
                                <span className={`kpi-icon-container ${kpi.status}`}>
                                    <Icon size={16} />
                                </span>
                                <span className={`kpi-trend-label ${kpi.up ? 'up' : 'down'}`}>
                                    {kpi.up ? <TrendingUp size={12} /> : <TrendingDown size={12} />}
                                    {kpi.trend}
                                </span>
                            </div>
                            <div className="kpi-card-content">
                                <h3 className="kpi-card-title">{kpi.title}</h3>
                                <div className="kpi-card-data-row">
                                    <span className="kpi-card-value">{kpi.value}</span>
                                    {kpi.type === 'circular' && (
                                        <div className="kpi-radial-indicator">
                                            <svg viewBox="0 0 36 36" className="radial-svg-element">
                                                <path className="radial-bg" d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831" />
                                                <path className="radial-fill success" strokeDasharray="95, 100" d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831" />
                                            </svg>
                                        </div>
                                    )}
                                    {kpi.type === 'badge' && (
                                        <span className="kpi-card-alert-badge critical">CRITICAL</span>
                                    )}
                                </div>
                            </div>
                        </div>
                    );
                })}
            </section>

            <section className="dashboard-workspace-grid">

                <div className="workspace-column block-feed">
                    <div className="column-head-wrapper">
                        <div className="column-title-flex">
                            <Newspaper size={16} className="title-icon-sync" />
                            <h2 className="column-heading">Live News Intelligence</h2>
                        </div>
                        <span className="column-metric-pill">{newsIntelligence.length} Streams</span>
                    </div>
                    <div className="column-scrollable-area">
                        {newsIntelligence.map((news) => (
                            <div key={news.id} className={`feed-item-card severity-${news.severity}`}>
                                <div className="feed-item-meta">
                                    <span className={`severity-tag level-${news.severity}`}>{news.severity}</span>
                                    <span className="feed-item-time"><Clock size={10} /> {news.time}</span>
                                </div>
                                <h4 className="feed-item-title">{news.title}</h4>
                                <p className="feed-item-desc">{news.summary}</p>
                                <div className="feed-item-footer">
                                    <span className="feed-src">{news.source}</span>
                                    <span className="feed-loc">{news.location}</span>
                                    <span className="feed-conf">Conf: <strong>{news.confidence}</strong></span>
                                </div>
                            </div>
                        ))}
                    </div>
                </div>

                <div className="workspace-column block-map-pipeline">
                    <div className="column-head-wrapper">
                        <div className="column-title-flex">
                            <Globe size={16} className="title-icon-sync" />
                            <h2 className="column-heading">Live Geographic Monitoring</h2>
                        </div>
                        <span className="column-metric-pill font-mono">GRID INTERSECT</span>
                    </div>

                    <div className="map-card-canvas">
                        <img src="src/assets/images/map.png" alt="Operational Threat Matrix Map" className="map-fluid-media" />
                        <div className="map-dark-overlay"></div>
                        <div className="map-radar-sweep-effect"></div>

                        {disruptionMarkers.map((marker) => (
                            <div
                                key={marker.id}
                                className={`geo-marker-node type-${marker.status}`}
                                style={{ top: marker.top, left: marker.left }}
                            >
                                <span className="geo-node-pulse"></span>
                                <span className="geo-node-core"></span>
                                <span className="geo-node-label">{marker.label}</span>
                            </div>
                        ))}
                    </div>

                    <div className="agent-pipeline-workspace">
                        <div className="pipeline-workspace-title">
                            <Cpu size={12} />
                            <span>ORCHESTRATED AI AGENT PIPELINE</span>
                        </div>
                        <div className="pipeline-nodes-row">
                            {agentPipeline.map((agent, index) => (
                                <React.Fragment key={agent.id}>
                                    <div className="pipeline-agent-node">
                                        <div className="agent-node-header">
                                            <span className="agent-node-name">{agent.name}</span>
                                            <span className={`agent-node-status label-${agent.status.toLowerCase()}`}>{agent.status}</span>
                                        </div>
                                        <div className="agent-node-metrics">
                                            <span>C: {agent.confidence}</span>
                                            <span>T: {agent.time}</span>
                                        </div>
                                        <div className="agent-node-task-box">
                                            <p className="agent-node-task-text">{agent.task}</p>
                                        </div>
                                    </div>
                                    {index < agentPipeline.length - 1 && (
                                        <div className="pipeline-node-link">
                                            <div className="pipeline-wave-track">
                                                <span className="pipeline-wave-particle"></span>
                                                <span className="pipeline-wave-particle delay-a"></span>
                                            </div>
                                            <ArrowRight size={12} className="pipeline-arrow-sync" />
                                        </div>
                                    )}
                                </React.Fragment>
                            ))}
                        </div>
                    </div>
                </div>

                <div className="workspace-column block-timeline">
                    <div className="column-head-wrapper">
                        <div className="column-title-flex">
                            <Activity size={16} className="title-icon-sync" />
                            <h2 className="column-heading">System Activity Timeline</h2>
                        </div>
                        <button className="timeline-action-refresh" aria-label="Refresh timeline data"><RefreshCw size={12} /></button>
                    </div>
                    <div className="column-scrollable-area padding-left-sm">
                        {systemTimeline.map((item) => (
                            <div key={item.id} className="timeline-row-item">
                                <div className="timeline-row-aside">
                                    <span className="timeline-row-clock">{item.time}</span>
                                    <div className={`timeline-row-indicator state-${item.status}`}>
                                        {item.status === 'success' ? <CheckCircle2 size={10} /> : item.status === 'warning' ? <Clock size={10} /> : <AlertTriangle size={10} />}
                                    </div>
                                </div>
                                <div className="timeline-row-card">
                                    <h4 className="timeline-card-title">{item.event}</h4>
                                    <p className="timeline-card-desc">{item.desc}</p>
                                </div>
                            </div>
                        ))}
                    </div>
                </div>

            </section>

            <section className="recommendations-panel-wrapper">
                <div className="recommendations-panel-header">
                    <div className="column-title-flex">
                        <FileText size={18} className="title-icon-sync" />
                        <h2 className="column-heading">Latest AI Recommendations & Prescriptive Mitigations</h2>
                    </div>
                    <span className="column-metric-pill">DECISION INTEL GENERATED</span>
                </div>
                <div className="recommendations-fluid-grid">
                    {aiRecommendations.map((rec) => (
                        <div key={rec.id} className={`recommendation-action-card priority-${rec.priority.toLowerCase()}`}>
                            <div className="recommendation-card-top">
                                <span className={`rec-priority-badge type-${rec.priority.toLowerCase()}`}>{rec.priority}</span>
                                <span className="rec-accuracy-rating">Confidence: <strong>{rec.confidence}</strong></span>
                            </div>
                            <h3 className="recommendation-card-heading">{rec.title}</h3>
                            <div className="recommendation-card-metrics-block">
                                <div className="rec-metric-cell">
                                    <span className="rec-cell-lbl">Targeted Business Impact</span>
                                    <span className="rec-cell-val impact">{rec.impact}</span>
                                </div>
                                <div className="rec-metric-cell">
                                    <span className="rec-cell-lbl">Est. Mitigation Delay</span>
                                    <span className="rec-cell-val delay">{rec.delay}</span>
                                </div>
                            </div>
                            <div className="recommendation-card-strategy-block">
                                <span className="rec-strategy-lbl">Prescribed Execution Strategy:</span>
                                <p className="rec-strategy-txt">{rec.action}</p>
                            </div>
                            <button className={`recommendation-action-trigger execution-${rec.priority.toLowerCase()}`}>
                                Authorize Execution Protocols <ArrowRight size={12} />
                            </button>
                        </div>
                    ))}
                </div>
            </section>
        </div>
    );
}