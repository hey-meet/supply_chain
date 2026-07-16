// NewsIntelligence.jsx
import React, { useState, useEffect } from 'react';
import {
    Radio,
    RefreshCw,
    Database,
    AlertOctagon,
    Clock,
    CheckCircle,
    Activity,
    Cpu,
    FileText,
    Search,
    TrendingUp,
    Globe,
    MapPin,
    Layers,
    CheckSquare,
    FileCheck,
    Network
} from 'lucide-react';
import '../styles/news-intelligence.css';

const kpiData = [
    { id: 1, title: 'Total News Today', value: '256', trend: '+14% from yesterday', colorClass: 'blue', icon: Radio },
    { id: 2, title: 'Critical News', value: '18', trend: 'Requires action', colorClass: 'red', icon: AlertOctagon },
    { id: 3, title: 'Processing Queue', value: '12', trend: 'Active ingestion', colorClass: 'amber', icon: Clock },
    { id: 4, title: 'Classified News', value: '244', trend: '100% parsed', colorClass: 'green', icon: CheckCircle }
];

const mockNews = [
    { id: 1, publisher: 'Reuters Logistics', initials: 'RL', headline: 'Port of Mumbai Terminal 2 Faces Heavy Container Congestion', time: '5 mins ago', country: 'India', state: 'Maharashtra', location: 'Mumbai Hub', summary: 'Labor strikes and crane maintenance schedules have created a 48-hour container backlog, severely affecting outbound aggregate distributions.', entity: 'JNPT Port Authority', severity: 'Critical', confidence: '98%', status: 'Validated' },
    { id: 2, publisher: 'Bloomberg Supply', initials: 'BS', headline: 'Limestone Mining Regulations Tighten in Rajasthan', time: '12 mins ago', country: 'India', state: 'Rajasthan', location: 'Western Block', summary: 'State environmental board mandates immediate structural compliance reviews on limestone quarry crushers, slowing output rates.', entity: 'Rajasthan Mines Dept', severity: 'Warning', confidence: '94%', status: 'Processing' },
    { id: 3, publisher: 'JOC Logistics', initials: 'JC', headline: 'National Highway 48 Landslide Blocks Heavy Freight Vehicles', time: '20 mins ago', country: 'India', state: 'Gujarat', location: 'Valsad Corridor', summary: 'Monsoon flash floods trigger hillside collapse on primary logistics route. Rerouting required for all bulk cement carriers.', entity: 'NHAI Highway Patrol', severity: 'Critical', confidence: '99%', status: 'Validated' },
    { id: 4, publisher: 'Steel & Coal Intel', initials: 'SC', headline: 'Petcoke Import Tariffs Set to Rise Next Quarter', time: '35 mins ago', country: 'Global', state: 'All', location: 'International Trade', summary: 'New maritime trade policy updates suggest a 4% tariff hike on imported solid fuels, directly escalating kiln operating costs.', entity: 'Ministry of Commerce', severity: 'Warning', confidence: '91%', status: 'Classified' },
    { id: 5, publisher: 'Logistics Insider', initials: 'LI', headline: 'Silo Storage Upgrades Completed at Chennai Plant', time: '1 hr ago', country: 'India', state: 'Tamil Nadu', location: 'Chennai South', summary: 'Automated high-capacity blending systems successfully online. Local inventory buffer capacity elevated by 25% safely.', entity: 'Asset Operations Edge', severity: 'Safe', confidence: '97%', status: 'Collected' },
    { id: 6, publisher: 'Mint Energy', initials: 'ME', headline: 'Grid Voltage Fluctuation Restricts Industrial Kiln Operations', time: '2 hrs ago', country: 'India', state: 'Madhya Pradesh', location: 'Central Grid', summary: 'Substation maintenance forces localized power capping. Finished clinker grinding throughput restricted to off-peak slots.', entity: 'State Electricity Board', severity: 'Warning', confidence: '95%', status: 'Validated' }
];

const pipelineStages = [
    { id: 1, name: 'Collect', icon: Database, status: 'Active', count: '14,205 articles', time: '0.3s avg', task: 'Polling 450 global feeds', active: true },
    { id: 2, name: 'Extract', icon: Search, status: 'Active', count: '3,110 entities', time: '0.4s avg', task: 'NER text parsing engine', active: true },
    { id: 3, name: 'Classify', icon: Layers, status: 'Active', count: '2,890 parsed', time: '0.2s avg', task: 'Supply chain tag match', active: true },
    { id: 4, name: 'Validate', icon: CheckSquare, status: 'Idle', count: '456 verified', time: '0.5s avg', task: 'Cross-telemetry checking', active: false },
    { id: 5, name: 'Completed', icon: FileCheck, status: 'Idle', count: '244 ready', time: '0.1s avg', task: 'Dispatching payload logs', active: false }
];

const classifiedEvents = [
    { id: 1, time: '13:20', type: 'Port Disruption', detail: 'Mumbai Port backlog confirmed via multi-source verification.' },
    { id: 2, time: '13:08', type: 'Regulatory Change', detail: 'Limestone mining caps matching operational risk markers in Rajasthan.' },
    { id: 3, time: '12:55', type: 'Route Hazard', detail: 'Landslide on NH-48 mapped to primary supply corridor.' }
];

const globalRegions = [
    { name: 'North America', status: 'optimal', sources: '45', event: 'Houston Port normal', coverage: '99.4%' },
    { name: 'Europe', status: 'warning', sources: '64', event: 'Rhine barge low levels', coverage: '99.7%' },
    { name: 'Asia Pacific', status: 'critical', sources: '88', event: 'Mumbai Port strike alert', coverage: '99.9%' }
];

const indiaRegions = [
    { name: 'North', status: 'optimal', sources: '24', event: 'NTPC supply normal', coverage: '99.1%' },
    { name: 'West', status: 'critical', sources: '36', event: 'Landslide blocking NH-48', coverage: '99.8%' },
    { name: 'East', status: 'warning', sources: '22', event: 'Rail allocation delay', coverage: '98.4%' }
];

const systemServices = [
    { name: 'API Status', status: 'optimal' },
    { name: 'Crawler Status', status: 'optimal' },
    { name: 'AI Status', status: 'warning' },
    { name: 'Validation Engine', status: 'optimal' }
];

export default function NewsIntelligence() {
    const [timeStr, setTimeStr] = useState('13:25:28');
    const [isRefreshing, setIsRefreshing] = useState(false);

    useEffect(() => {
        const interval = setInterval(() => {
            const now = new Date();
            setTimeStr(now.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', second: '2-digit' }));
        }, 1000);
        return () => clearInterval(interval);
    }, []);

    const handleManualRefresh = () => {
        setIsRefreshing(true);
        setTimeout(() => setIsRefreshing(false), 800);
    };

    return (
        <div className="news-intel-scope">

            {/* Page Header Area */}
            <header className="intel-header-block">
                <div className="intel-header-left">
                    <h1 className="intel-page-title">News Intelligence</h1>
                    <p className="intel-page-subtitle">Real-time AI-powered logistics news monitoring and disruption intelligence.</p>
                </div>
                <div className="intel-header-right">
                    <div className="intel-source-pill">
                        <Network size={14} />
                        <span>568 Connected Sources</span>
                    </div>
                    <div className="intel-refresh-group">
                        <span className="intel-ts-lbl">Last Refresh:</span>
                        <span className="intel-ts-val">{timeStr}</span>
                        <button
                            className={`intel-refresh-btn ${isRefreshing ? 'rotating' : ''}`}
                            onClick={handleManualRefresh}
                            aria-label="Refresh intelligence data"
                        >
                            <RefreshCw size={14} />
                        </button>
                    </div>
                    <div className="intel-live-badge">
                        <span className="intel-pulse-dot"></span>
                        AI INGESTION ACTIVE
                    </div>
                </div>
            </header>

            {/* Top KPI Cards Section */}
            <section className="intel-kpi-grid">
                {kpiData.map((kpi) => {
                    const IconComponent = kpi.icon;
                    return (
                        <div key={kpi.id} className="intel-kpi-card">
                            <div className="intel-kpi-top">
                                <span className={`intel-kpi-icon ${kpi.colorClass}`}>
                                    <IconComponent size={18} />
                                </span>
                                <span className="intel-kpi-trend">
                                    <TrendingUp size={12} />
                                    {kpi.trend}
                                </span>
                            </div>
                            <div className="intel-kpi-bottom">
                                <h3 className="intel-kpi-title">{kpi.title}</h3>
                                <span className="intel-kpi-val">{kpi.value}</span>
                            </div>
                        </div>
                    );
                })}
            </section>

            {/* Main Responsive Grid Workspace */}
            <section className="intel-workspace-grid">

                {/* Left Column: Live News Feed */}
                <div className="intel-column column-feed">
                    <div className="intel-column-head">
                        <h2 className="intel-column-title">Live News Feed</h2>
                        <span className="intel-count-badge">Streaming Live</span>
                    </div>
                    <div className="intel-scroll-container">
                        {mockNews.map((news) => (
                            <div key={news.id} className="intel-report-card">
                                <div className="report-card-top">
                                    <div className="report-publisher-row">
                                        <div className="publisher-avatar">{news.initials}</div>
                                        <div className="publisher-meta">
                                            <h4 className="publisher-name">{news.publisher}</h4>
                                            <span className="report-time"><Clock size={11} /> {news.time}</span>
                                        </div>
                                    </div>
                                    <span className={`report-severity-badge severity-${news.severity.toLowerCase()}`}>
                                        {news.severity}
                                    </span>
                                </div>

                                <h3 className="report-headline">{news.headline}</h3>
                                <p className="report-summary">{news.summary}</p>

                                <div className="report-location-row">
                                    <div className="geo-tag">
                                        <Globe size={12} />
                                        <span>{news.country}</span>
                                    </div>
                                    {news.state !== 'All' && (
                                        <div className="geo-tag">
                                            <MapPin size={12} />
                                            <span>{news.state}</span>
                                        </div>
                                    )}
                                </div>

                                <div className="report-card-footer">
                                    <div className="footer-meta-cell">
                                        <span className="meta-lbl">Detected Entity</span>
                                        <span className="meta-val truncate">{news.entity}</span>
                                    </div>
                                    <div className="footer-meta-cell text-right">
                                        <span className="meta-lbl">Conf. / Status</span>
                                        <span className="meta-val fw-bold">
                                            {news.confidence} <span className="status-dot-separator">•</span> <span className={`status-txt-${news.status.toLowerCase()}`}>{news.status}</span>
                                        </span>
                                    </div>
                                </div>
                            </div>
                        ))}
                    </div>
                </div>

                {/* Center Column: Pipeline & Classified Events */}
                <div className="intel-column column-pipeline-middle">
                    <div className="intel-column-head">
                        <h2 className="intel-column-title">News Processing Pipeline</h2>
                    </div>

                    <div className="pipeline-horizontal-box">
                        <div className="pipeline-flow-row">
                            {pipelineStages.map((stage, index) => {
                                const StageIcon = stage.icon;
                                return (
                                    <React.Fragment key={stage.id}>
                                        <div className={`pipeline-stage-node ${stage.active ? 'active-glow' : ''}`}>
                                            <div className="stage-icon-circle">
                                                <StageIcon size={16} />
                                            </div>
                                            <h4 className="stage-node-title">{stage.name}</h4>
                                            <span className={`stage-status-indicator ${stage.status.toLowerCase()}`}>
                                                {stage.status}
                                            </span>
                                            <div className="stage-node-details">
                                                <span className="detail-row-txt font-mono fw-bold">{stage.count}</span>
                                                <span className="detail-row-txt text-secondary">{stage.time}</span>
                                            </div>
                                            <div className="stage-task-hover">
                                                <span className="task-lbl">Directive:</span>
                                                <p className="task-desc">{stage.task}</p>
                                            </div>
                                        </div>

                                        {index < pipelineStages.length - 1 && (
                                            <div className="pipeline-wave-connector">
                                                <div className="wave-animation-container">
                                                    <svg className="wave-svg" viewBox="0 0 100 20" preserveAspectRatio="none">
                                                        <path className="wave-path-bg" d="M 0 10 Q 25 2, 50 10 T 100 10" />
                                                        <path className="wave-path-animated" d="M 0 10 Q 25 2, 50 10 T 100 10" />
                                                    </svg>
                                                </div>
                                            </div>
                                        )}
                                    </React.Fragment>
                                );
                            })}
                        </div>
                    </div>

                    <div className="classified-timeline-container">
                        <div className="intel-column-head border-none padding-none margin-bottom-md">
                            <h2 className="intel-column-title size-sub">Recent Classified Events</h2>
                        </div>
                        <div className="timeline-vertical-stack">
                            {classifiedEvents.map((evt) => (
                                <div key={evt.id} className="timeline-event-row">
                                    <div className="timeline-left-node">
                                        <span className="timeline-time-lbl font-mono">{evt.time}</span>
                                        <div className="timeline-circle-marker"></div>
                                    </div>
                                    <div className="timeline-right-content">
                                        <h4 className="timeline-event-type">{evt.type}</h4>
                                        <p className="timeline-event-detail">{evt.detail}</p>
                                    </div>
                                </div>
                            ))}
                        </div>
                    </div>
                </div>

                {/* Right Column: Global Monitoring Status */}
                <div className="intel-column column-status-right">
                    <div className="intel-column-head">
                        <h2 className="intel-column-title">Global Monitoring Status</h2>
                    </div>

                    <div className="monitoring-scroll-area">
                        <div className="region-section-wrapper">
                            <h3 className="region-section-heading">WORLD MONITOR</h3>
                            <div className="region-matrix-grid">
                                {globalRegions.map((region, idx) => (
                                    <div key={idx} className="region-matrix-row">
                                        <div className="region-identity">
                                            <span className={`status-indicator-dot dot-${region.status}`}></span>
                                            <span className="region-name-txt">{region.name}</span>
                                        </div>
                                        <div className="region-stats-block">
                                            <span className="stat-value-txt">{region.sources} Src</span>
                                            <span className="stat-value-txt text-right font-mono">{region.coverage}</span>
                                        </div>
                                        <div className="region-event-marquee">
                                            <span className="marquee-lbl">Latest:</span>
                                            <span className="marquee-txt truncate">{region.event}</span>
                                        </div>
                                    </div>
                                ))}
                            </div>
                        </div>

                        <div className="region-section-wrapper margin-top-lg">
                            <h3 className="region-section-heading">INDIA MONITOR</h3>
                            <div className="region-matrix-grid">
                                {indiaRegions.map((region, idx) => (
                                    <div key={idx} className="region-matrix-row">
                                        <div className="region-identity">
                                            <span className={`status-indicator-dot dot-${region.status}`}></span>
                                            <span className="region-name-txt">{region.name}</span>
                                        </div>
                                        <div className="region-stats-block">
                                            <span className="stat-value-txt">{region.sources} Src</span>
                                            <span className="stat-value-txt text-right font-mono">{region.coverage}</span>
                                        </div>
                                        <div className="region-event-marquee">
                                            <span className="marquee-lbl">Latest:</span>
                                            <span className="marquee-txt truncate">{region.event}</span>
                                        </div>
                                    </div>
                                ))}
                            </div>
                        </div>

                        <div className="system-infrastructure-wrapper margin-top-lg">
                            <h3 className="region-section-heading">SYSTEM SERVICE NODES</h3>
                            <div className="system-status-pill-grid">
                                {systemServices.map((service, idx) => (
                                    <div key={idx} className="system-node-pill">
                                        <span className={`node-indicator-dot dot-${service.status}`}></span>
                                        <span className="node-service-name">{service.name}</span>
                                    </div>
                                ))}
                            </div>
                        </div>
                    </div>
                </div>
            </section>

            {/* Bottom Section: Analytics Panels */}
            <section className="intel-analytics-section">
                <div className="intel-column-head">
                    <h2 className="intel-column-title">News Source Analytics</h2>
                </div>
                <div className="analytics-fluid-grid">
                    <div className="analytics-panel-card">
                        <h4 className="analytics-card-title">Most Active Sources</h4>
                        <div className="analytics-data-stack">
                            <div className="analytics-stack-row"><span className="stack-lbl-txt font-semibold">Reuters Logistics</span><span className="stack-val-txt font-mono">74 articles</span></div>
                            <div className="analytics-stack-row"><span className="stack-lbl-txt font-semibold">Bloomberg Supply</span><span className="stack-val-txt font-mono">62 articles</span></div>
                            <div className="analytics-stack-row"><span className="stack-lbl-txt font-semibold">Lloyds Maritime</span><span className="stack-val-txt font-mono">48 articles</span></div>
                        </div>
                    </div>
                    <div className="analytics-panel-card">
                        <h4 className="analytics-card-title">Latest Refresh Metrics</h4>
                        <div className="analytics-data-stack">
                            <div className="analytics-stack-row"><span className="stack-lbl-txt">Global crawl time</span><span className="stack-val-txt font-mono text-brand">13:24:11</span></div>
                            <div className="analytics-stack-row"><span className="stack-lbl-txt">Polling frequency</span><span className="stack-val-txt font-mono">180s avg</span></div>
                            <div className="analytics-stack-row"><span className="stack-lbl-txt">Success rate</span><span className="stack-val-txt font-mono text-success">99.84%</span></div>
                        </div>
                    </div>
                    <div className="analytics-panel-card">
                        <h4 className="analytics-card-title">Collection Latency</h4>
                        <div className="analytics-data-stack">
                            <div className="analytics-stack-row"><span className="stack-lbl-txt">Ingestion latency</span><span className="stack-val-txt font-mono">0.34s avg</span></div>
                            <div className="analytics-stack-row"><span className="stack-lbl-txt">Fastest pipeline</span><span className="stack-val-txt font-mono text-success">0.08s</span></div>
                            <div className="analytics-stack-row"><span className="stack-lbl-txt">Slowest edge</span><span className="stack-val-txt font-mono text-critical">1.42s</span></div>
                        </div>
                    </div>
                    <div className="analytics-panel-card">
                        <h4 className="analytics-card-title">Coverage Summary</h4>
                        <div className="analytics-data-stack">
                            <div className="analytics-stack-row"><span className="stack-lbl-txt">Countries monitored</span><span className="stack-val-txt font-mono">142 nodes</span></div>
                            <div className="analytics-stack-row"><span className="stack-lbl-txt">Indian states mapped</span><span className="stack-val-txt font-mono">28 states</span></div>
                            <div className="analytics-stack-row"><span className="stack-lbl-txt">Reliability rating</span><span className="stack-val-txt font-mono text-brand">99.91%</span></div>
                        </div>
                    </div>
                </div>
            </section>

        </div>
    );
}