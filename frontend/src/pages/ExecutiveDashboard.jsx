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
import { getDashboardData } from '../services/dashboardService';
import '../styles/executive-dashboard.css';

const iconMap = {
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
};

export default function ExecutiveDashboard() {
    const [timeStr, setTimeStr] = useState('13:01:06');
    const [dashboardData, setDashboardData] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    const fetchDashboard = async () => {
        try {
            setLoading(true);
            const response = await getDashboardData();
            if (response && response.success) {
                setDashboardData(response.data);
                setError(null);
            } else {
                setError(new Error(response?.message || "Failed to fetch data"));
            }
        } catch (err) {
            setError(err);
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchDashboard();

        const updateTime = () => {
            const now = new Date();
            setTimeStr(now.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', second: '2-digit' }));
        };
        updateTime();
        const interval = setInterval(updateTime, 1000);
        return () => clearInterval(interval);
    }, []);

    if (loading && !dashboardData) {
        return (
            <div className="dashboard-content-scope" style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', minHeight: '400px' }}>
                <div className="news-intel-loading">Loading Dashboard Data...</div>
            </div>
        );
    }

    if (error && !dashboardData) {
        return (
            <div className="dashboard-content-scope" style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', minHeight: '500px', gap: '16px', padding: '40px' }}>
                <h1 className="page-main-title">Executive Dashboard</h1>
                <div className="alert-badge critical" style={{ background: 'var(--intel-critical)', color: 'white', padding: '8px 16px', borderRadius: '6px', fontWeight: 'bold' }}>NO ACTIVE INVESTIGATION</div>
                <p style={{ color: 'var(--intel-text-s)', fontSize: '15px', maxWidth: '500px', textAlign: 'center' }}>
                    No active supply chain risk assessment was found. Please head to the <strong>News Intelligence</strong> tab to execute an incident search query.
                </p>
            </div>
        );
    }

    const {
        kpis = [],
        news_intelligence = [],
        disruption_markers = [],
        agent_pipeline = [],
        system_timeline = [],
        ai_recommendations = [],
        metrics = {}
    } = dashboardData || {};

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
                    {metrics.graph_execution_time_seconds !== undefined && (
                        <div className="system-timestamp" style={{ fontSize: '11px', color: 'var(--intel-text-s)', display: 'flex', flexDirection: 'column', alignItems: 'flex-end', marginTop: '4px' }}>
                            <span>Graph Exec: {metrics.graph_execution_time_seconds}s | API: {metrics.api_response_time_seconds}s</span>
                            {metrics.cache_last_updated && (
                                <span>Cache Updated: {new Date(metrics.cache_last_updated).toLocaleTimeString()}</span>
                            )}
                        </div>
                    )}
                    <div className="system-live-badge">
                        <span className="live-pulse-dot"></span>
                        LIVE MONITORING ACTIVE
                    </div>
                </div>
            </header>

            <section className="dashboard-kpi-grid">
                {kpis.map((kpi) => {
                    const Icon = iconMap[kpi.icon] || Activity;
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
                        <span className="column-metric-pill">{news_intelligence.length} Streams</span>
                    </div>
                    <div className="column-scrollable-area">
                        {news_intelligence.map((news) => (
                            <div key={news.id} className={`feed-item-card severity-${news.severity}`}>
                                <div className="feed-item-meta">
                                    <span className={`severity-tag level-${news.severity}`}>{news.severity}</span>
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

                        {disruption_markers.map((marker) => (
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
                            {agent_pipeline.map((agent, index) => (
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
                                    {index < agent_pipeline.length - 1 && (
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
                    </div>
                    <div className="column-scrollable-area padding-left-sm">
                        {system_timeline.map((item) => (
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
                    {ai_recommendations.map((rec) => (
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