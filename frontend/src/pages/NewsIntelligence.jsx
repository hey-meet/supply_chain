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
import newsService from "../services/newsService";
import incidentService from "../services/incidentService";

const IconMap = {
    Radio,
    AlertOctagon,
    Clock,
    CheckCircle,
    Database,
    Search,
    Layers,
    CheckSquare,
    FileCheck,
    Activity,
    Cpu,
    FileText,
    TrendingUp,
    Globe,
    MapPin,
    Network,
    RefreshCw
};

const defaultKpiIcons = [Radio, AlertOctagon, Clock, CheckCircle];
const defaultPipelineIcons = [Database, Search, Layers, CheckSquare, FileCheck];

export default function NewsIntelligence() {
    const [timeStr, setTimeStr] = useState('13:25:28');
    const [isRefreshing, setIsRefreshing] = useState(false);
    const [newsData, setNewsData] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [searchQuery, setSearchQuery] = useState('');
    const [isSearching, setIsSearching] = useState(false);
    const [statusMessage, setStatusMessage] = useState(null);

    const fetchNewsData = async () => {
        try {
            setIsRefreshing(true);
            const response = await newsService.getNewsIntelligence();
            if (response && response.success) {
                setNewsData(response.data);
                setError(null);
            } else {
                setError(new Error(response?.message || "Failed to fetch data"));
            }
        } catch (err) {
            setError(err);
        } finally {
            setLoading(false);
            setIsRefreshing(false);
        }
    };

    const handleSearch = async () => {
        if (!searchQuery.trim()) return;
        setIsSearching(true);
        setStatusMessage({ type: 'loading', text: 'Executing multi-agent incident classification pipeline...' });
        
        try {
            const result = await incidentService.getIncidentCenter(searchQuery);
            if (result && result.success) {
                setStatusMessage({ type: 'success', text: 'Incident successfully classified and supply chain impact simulated.' });
                setError(null);
                await fetchNewsData();
            } else {
                setStatusMessage({ type: 'error', text: result.message || 'Workflow execution failed.' });
            }
        } catch (err) {
            console.error("News Search error:", err);
            setStatusMessage({ type: 'error', text: 'Server error encountered during graph execution.' });
        } finally {
            setIsSearching(false);
        }
    };

    useEffect(() => {
        fetchNewsData();

        const interval = setInterval(() => {
            const now = new Date();
            setTimeStr(now.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', second: '2-digit' }));
        }, 1000);
        return () => clearInterval(interval);
    }, []);

    const handleManualRefresh = () => {
        fetchNewsData();
    };

    if (loading && !newsData) {
        return <div className="news-intel-loading">Loading...</div>;
    }

    if (error && !newsData) {
        const message = error.message || "";
        if (message.includes("pending") || message.includes("Initialize") || message.includes("query")) {
            return (
                <div className="news-intel-scope flex-center-pending" style={{ minHeight: '500px', display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', gap: '16px', padding: '40px' }}>
                    <h1 className="intel-page-title">News Intelligence</h1>
                    <p className="intel-page-subtitle" style={{ marginBottom: '20px' }}>No active incident analysis. Execute a classification query to initialize the supply chain graph.</p>
                    
                    <div className="search-container" style={{ maxWidth: '600px', width: '100%' }}>
                        <input
                            type="text"
                            className="search-input"
                            placeholder="Enter disruption event query (e.g., 'Heavy rainfall Jodhpur monsoons')..."
                            value={searchQuery}
                            onChange={(e) => setSearchQuery(e.target.value)}
                            disabled={isSearching}
                        />
                        <button
                            className="search-button"
                            onClick={handleSearch}
                            disabled={isSearching || !searchQuery.trim()}
                        >
                            {isSearching ? <RefreshCw size={14} className="rotating" /> : <Search size={14} />}
                            {isSearching ? "Analyzing..." : "Search & Classify"}
                        </button>
                    </div>

                    {statusMessage && (
                        <div className={`status-banner status-${statusMessage.type}`} style={{ maxWidth: '600px', width: '100%' }}>
                            {statusMessage.type === 'success' ? <CheckCircle size={16} /> : statusMessage.type === 'error' ? <AlertOctagon size={16} /> : <RefreshCw size={16} className="rotating" />}
                            <span style={{ marginLeft: '8px' }}>{statusMessage.text}</span>
                        </div>
                    )}
                </div>
            );
        }
        return <div className="news-intel-scope flex-center-pending" style={{ minHeight: '400px', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>Error loading News Intelligence.</div>;
    }

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

            {/* Interactive News Search Bar */}
            <div className="search-container">
                <input
                    type="text"
                    className="search-input"
                    placeholder="Enter disruption event query (e.g., 'Heavy rainfall Jodhpur monsoons')..."
                    value={searchQuery}
                    onChange={(e) => setSearchQuery(e.target.value)}
                    disabled={isSearching}
                />
                <button
                    className="search-button"
                    onClick={handleSearch}
                    disabled={isSearching || !searchQuery.trim()}
                >
                    {isSearching ? <RefreshCw size={14} className="rotating" /> : <Search size={14} />}
                    {isSearching ? "Analyzing..." : "Search & Classify"}
                </button>
            </div>

            {statusMessage && (
                <div className={`status-banner status-${statusMessage.type}`}>
                    {statusMessage.type === 'success' ? <CheckCircle size={16} /> : statusMessage.type === 'error' ? <AlertOctagon size={16} /> : <RefreshCw size={16} className="rotating" />}
                    <span style={{ marginLeft: '8px' }}>{statusMessage.text}</span>
                </div>
            )}

            {/* Top KPI Cards Section */}
            <section className="intel-kpi-grid">
                {newsData?.kpis?.map((kpi, index) => {
                    const IconComponent = (kpi.icon && IconMap[kpi.icon]) ? IconMap[kpi.icon] : (defaultKpiIcons[index % defaultKpiIcons.length] || Activity);
                    return (
                        <div key={kpi.id || index} className="intel-kpi-card">
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
                        {newsData?.news_feed?.map((news) => (
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
                            {newsData?.pipeline?.map((stage, index) => {
                                const StageIcon = (stage.icon && IconMap[stage.icon]) ? IconMap[stage.icon] : (defaultPipelineIcons[index % defaultPipelineIcons.length] || Activity);
                                return (
                                    <React.Fragment key={stage.id || index}>
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

                                        {index < newsData.pipeline.length - 1 && (
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
                            {newsData?.classified_events?.map((evt) => (
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
                                {newsData?.status?.global_regions?.map((region, idx) => (
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
                                {newsData?.status?.india_regions?.map((region, idx) => (
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
                                {newsData?.status?.system_services?.map((service, idx) => (
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
                            {newsData?.analytics?.most_active_sources?.map((src, idx) => (
                                <div key={idx} className="analytics-stack-row">
                                    <span className="stack-lbl-txt font-semibold">{src.name}</span>
                                    <span className="stack-val-txt font-mono">{src.articles}</span>
                                </div>
                            ))}
                        </div>
                    </div>
                    <div className="analytics-panel-card">
                        <h4 className="analytics-card-title">Latest Refresh Metrics</h4>
                        <div className="analytics-data-stack">
                            <div className="analytics-stack-row"><span className="stack-lbl-txt">Global crawl time</span><span className="stack-val-txt font-mono text-brand">{newsData?.analytics?.refresh_metrics?.global_crawl_time}</span></div>
                            <div className="analytics-stack-row"><span className="stack-lbl-txt">Polling frequency</span><span className="stack-val-txt font-mono">{newsData?.analytics?.refresh_metrics?.polling_frequency}</span></div>
                            <div className="analytics-stack-row"><span className="stack-lbl-txt">Success rate</span><span className="stack-val-txt font-mono text-success">{newsData?.analytics?.refresh_metrics?.success_rate}</span></div>
                        </div>
                    </div>
                    <div className="analytics-panel-card">
                        <h4 className="analytics-card-title">Collection Latency</h4>
                        <div className="analytics-data-stack">
                            <div className="analytics-stack-row"><span className="stack-lbl-txt">Ingestion latency</span><span className="stack-val-txt font-mono">{newsData?.analytics?.collection_latency?.ingestion_latency}</span></div>
                            <div className="analytics-stack-row"><span className="stack-lbl-txt">Fastest pipeline</span><span className="stack-val-txt font-mono text-success">{newsData?.analytics?.collection_latency?.fastest_pipeline}</span></div>
                            <div className="analytics-stack-row"><span className="stack-lbl-txt">Slowest edge</span><span className="stack-val-txt font-mono text-critical">{newsData?.analytics?.collection_latency?.slowest_edge}</span></div>
                        </div>
                    </div>
                    <div className="analytics-panel-card">
                        <h4 className="analytics-card-title">Coverage Summary</h4>
                        <div className="analytics-data-stack">
                            <div className="analytics-stack-row"><span className="stack-lbl-txt">Countries monitored</span><span className="stack-val-txt font-mono">{newsData?.analytics?.coverage_summary?.countries_monitored}</span></div>
                            <div className="analytics-stack-row"><span className="stack-lbl-txt">Indian states mapped</span><span className="stack-val-txt font-mono">{newsData?.analytics?.coverage_summary?.indian_states_mapped}</span></div>
                            <div className="analytics-stack-row"><span className="stack-lbl-txt">Reliability rating</span><span className="stack-val-txt font-mono text-brand">{newsData?.analytics?.coverage_summary?.reliability_rating}</span></div>
                        </div>
                    </div>
                </div>
            </section>

        </div>
    );
}