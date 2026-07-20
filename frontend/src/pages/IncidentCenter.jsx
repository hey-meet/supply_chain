// IncidentCenter.jsx
import React, { useState, useEffect } from 'react';
import {
    ShieldAlert,
    Clock,
    Activity,
    FileText,
    Layers,
    TrendingUp,
    MapPin,
    Globe,
    Factory,
    Users,
    Package,
    Route,
    DollarSign,
    AlertTriangle,
    CheckCircle2,
    HelpCircle,
    Cpu,
    ArrowRight,
    Briefcase
} from 'lucide-react';
import incidentService from "../services/incidentService";
import '../styles/incident-center.css';

// Helper map to match icon strings to Lucide components
const iconMap = {
    Factory,
    Users,
    Package,
    Route,
    ShieldAlert,
    Layers,
    Activity,
    DollarSign,
    Clock
};

export default function IncidentCenter() {
    const [liveTime, setLiveTime] = useState('14:02:11');
    const [incidentData, setIncidentData] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        const fetchIncidentData = async () => {
            try {
                setLoading(true);
                setError(null);
                const response = await incidentService.getIncidentCenter();
                setIncidentData(response.data);
            } catch (err) {
                console.error("Failed to fetch incident center data:", err);
                setError(err?.message || "Failed to load incident investigation data.");
            } finally {
                setLoading(false);
            }
        };

        fetchIncidentData();
    }, []);

    useEffect(() => {
        const timer = setInterval(() => {
            const now = new Date();
            setLiveTime(now.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', second: '2-digit' }));
        }, 1000);
        return () => clearInterval(timer);
    }, []);

    if (loading) {
        return (
            <div className="incident-center-scope flex-center" style={{ minHeight: '400px' }}>
                <p>Loading Incident Investigation Center...</p>
            </div>
        );
    }

    if (error) {
        return (
            <div className="incident-center-scope flex-center" style={{ minHeight: '400px' }}>
                <p className="text-critical">Error: {error}</p>
            </div>
        );
    }

    const incidentMeta = incidentData?.incident_meta || {};
    const extractedEntities = incidentData?.extracted_entities ?? [];
    const supportingSources = incidentData?.supporting_sources ?? [];
    const timelineSteps = incidentData?.timeline_steps ?? [];
    const impactCards = incidentData?.impact_cards ?? [];
    const progressStages = incidentData?.progress_stages ?? [];

    return (
        <div className="incident-center-scope">

            {/* Page Header Area */}
            <header className="ic-header-block">
                <div className="ic-header-left">
                    <h1 className="ic-page-title">Incident Investigation Center</h1>
                    <p className="ic-page-subtitle">Detailed AI investigation of a selected supply chain disruption.</p>
                </div>
                <div className="ic-header-right">
                    <div className="ic-timestamp-group">
                        <span className="ic-ts-lbl">System Time:</span>
                        <span className="ic-ts-val">{liveTime}</span>
                    </div>
                    <div className={`ic-status-capsule ${incidentMeta.severity?.toLowerCase() || 'critical'}`}>
                        <span className={`ic-status-indicator-dot ${incidentMeta.severity?.toLowerCase() || 'critical'}`}></span>
                        {incidentMeta.status ? incidentMeta.status.toUpperCase() : ''}
                    </div>
                    <div className="ic-live-ops-badge">
                        <span className="ic-pulse-ring"></span>
                        LIVE INVESTIGATION IN PROGRESS
                    </div>
                </div>
            </header>

            {/* Top Large Incident Summary Card */}
            <section className="ic-summary-section">
                <div className="ic-summary-card">
                    <div className="ic-summary-top-row">
                        <div className="ic-id-badge-flex">
                            <span className="ic-meta-id">{incidentMeta.id}</span>
                            <span className={`ic-sev-badge ${incidentMeta.severity?.toLowerCase() || 'critical'}`}>{incidentMeta.severity} Severity</span>
                            <span className="ic-priority-tag">{incidentMeta.businessPriority}</span>
                        </div>
                        <div className="ic-summary-quick-metrics">
                            <div className="quick-metric-item">
                                <span className="qm-lbl">Category:</span>
                                <span className="qm-val">{incidentMeta.riskCategory}</span>
                            </div>
                            <div className="quick-metric-item">
                                <span className="qm-lbl">AI Confidence:</span>
                                <span className="qm-val font-mono highlight-success">{incidentMeta.confidence}</span>
                            </div>
                        </div>
                    </div>

                    <p className="ic-summary-description-text">{incidentMeta.description}</p>

                    <div className="ic-summary-footer-grid">
                        <div className="summary-footer-cell">
                            <span className="sf-lbl">Primary Geography Location</span>
                            <span className="sf-val"><MapPin size={12} /> {incidentMeta.location}, {incidentMeta.state}, {incidentMeta.country}</span>
                        </div>
                        <div className="summary-footer-cell">
                            <span className="sf-lbl">Initial Automated Detection</span>
                            <span className="sf-val font-mono"><Clock size={12} /> {incidentMeta.detectedTime}</span>
                        </div>
                        <div className="summary-footer-cell">
                            <span className="sf-lbl">Analytical Engine Core Update</span>
                            <span className="sf-val font-mono"><Clock size={12} /> {incidentMeta.lastUpdated}</span>
                        </div>
                    </div>
                </div>
            </section>

            {/* Main Content Workspace Grid */}
            <section className="ic-workspace-three-column">

                {/* Left Panel: Original News Intelligence & Feeds */}
                <div className="ic-workspace-column column-left-intel">
                    <div className="column-head-wrapper">
                        <h2 className="column-section-title">Original News Intelligence</h2>
                    </div>

                    <div className="ic-card-body-container">
                        <div className="original-news-report-box">
                            <div className="news-report-header">
                                <span className="report-author-brand">Reuters Logistics Ingestion</span>
                                <span className="report-time-ago">Detected {incidentMeta.detectedTime}</span>
                            </div>
                            <h3 className="report-main-headline">NH-48 Freight Transit Halted Near Valsad Border Post Following Severe Regional Weather Damage</h3>
                            <p className="report-main-body">
                                Torrential rainfall lines have triggered swift water accumulation and micro-landslides along primary infrastructure sectors. State highways confirm immediate roadblocks for heavy commercial vehicle configurations until structural engineers complete assessments.
                            </p>
                        </div>

                        <div className="extracted-entities-wrapper">
                            <h4 className="panel-sub-label">EXTRACTED BUSINESS ENTITIES</h4>
                            <div className="entity-chips-flex">
                                {extractedEntities.map((entity, idx) => (
                                    <span key={idx} className="entity-chip-item">{entity}</span>
                                ))}
                            </div>
                        </div>

                        <div className="supporting-sources-wrapper">
                            <h4 className="panel-sub-label">CROSS-CHECKED SUPPORTING CHANNELS</h4>
                            <div className="supporting-sources-stack">
                                {supportingSources.map((src) => (
                                    <div key={src.id} className="supporting-source-row">
                                        <div className="src-identity-flex">
                                            <div className="src-avatar-circle">{src.publisher ? src.publisher.charAt(0) : ''}</div>
                                            <div className="src-meta-block">
                                                <span className="src-publisher-title">{src.publisher}</span>
                                                <span className="src-time-label"><Clock size={10} /> {src.time}</span>
                                            </div>
                                        </div>
                                        <div className="src-metrics-block">
                                            <span className="src-reliability-score font-mono">{src.reliability} Trust</span>
                                            <span className="src-verification-badge status-complete">{src.status}</span>
                                        </div>
                                    </div>
                                ))}
                            </div>
                        </div>
                    </div>
                </div>

                {/* Center Panel: AI Investigation Timeline Flow */}
                <div className="ic-workspace-column column-center-timeline">
                    <div className="column-head-wrapper">
                        <h2 className="column-section-title">AI Investigation Timeline</h2>
                    </div>

                    <div className="investigation-vertical-timeline">
                        {timelineSteps.map((step) => (
                            <div key={step.id} className={`investigation-timeline-card-row ${step.active ? 'active-step-glow' : ''}`}>
                                <div className="timeline-aside-node-track">
                                    <div className={`timeline-step-node-circle ${step.active ? 'active-node-pulse' : 'completed-node'}`}>
                                        {step.id}
                                    </div>
                                    <div className="timeline-track-connector-line"></div>
                                </div>

                                <div className="timeline-card-content-surface">
                                    <div className="timeline-card-header-flex">
                                        <h3 className="timeline-step-title">{step.title}</h3>
                                        <span className="timeline-agent-owner-label"><Cpu size={11} /> {step.agent}</span>
                                    </div>

                                    <div className="timeline-step-metrics-grid">
                                        {step.metrics && Object.entries(step.metrics).map(([key, val]) => (
                                            <div key={key} className="step-metric-badge-box">
                                                <span className="sm-badge-lbl">{key.replace(/([A-Z])/g, ' $1').toUpperCase()}</span>
                                                <span className="sm-badge-val truncate">{val}</span>
                                            </div>
                                        ))}
                                    </div>

                                    <div className="timeline-step-reasoning-block">
                                        <span className="step-reasoning-label">Agent Analytical Reasoning:</span>
                                        <p className="step-reasoning-paragraph">{step.reasoning}</p>
                                    </div>

                                    {step.active && (
                                        <div className="step-live-processing-bar">
                                            <span className="live-processing-fill-line"></span>
                                        </div>
                                    )}
                                </div>
                            </div>
                        ))}
                    </div>
                </div>

                {/* Right Panel: Business Impact Analysis */}
                <div className="ic-workspace-column column-right-impact">
                    <div className="column-head-wrapper">
                        <h2 className="column-section-title">Business Impact Analysis</h2>
                    </div>

                    <div className="compact-impact-cards-stack">
                        {impactCards.map((card) => {
                            const Icon = typeof card.icon === 'string' ? (iconMap[card.icon] || ShieldAlert) : (card.icon || ShieldAlert);
                            return (
                                <div key={card.id} className="compact-impact-card-item">
                                    <div className="cic-top-row">
                                        <div className="cic-title-flex">
                                            <span className={`cic-icon-wrapper color-${card.status}`}>
                                                <Icon size={14} />
                                            </span>
                                            <h4 className="cic-card-heading">{card.title}</h4>
                                        </div>
                                        <span className={`cic-count-label status-${card.status}`}>{card.count}</span>
                                    </div>
                                    <p className="cic-card-description">{card.desc}</p>
                                </div>
                            );
                        })}
                    </div>
                </div>

            </section>

            {/* Bottom Section: Progress Workflow */}
            <section className="ic-progress-workflow-section">
                <div className="workflow-horizontal-flow-row">
                    {progressStages.map((stage, index) => (
                        <React.Fragment key={stage.id}>
                            <div className={`workflow-stage-node-box ${stage.active ? 'current-active-glow' : ''}`}>
                                <div className="stage-node-circle-icon">
                                    {stage.status === 'Complete' ? <CheckCircle2 size={16} className="color-success" /> : stage.active ? <Clock size={16} className="color-warning" /> : <HelpCircle size={16} className="color-text-s" />}
                                </div>
                                <div className="stage-node-meta-labels">
                                    <h4 className="stage-node-name-text">{stage.name}</h4>
                                    <span className="stage-node-agent-owner truncate">{stage.agent}</span>
                                    <span className="stage-node-timestamp font-mono">{stage.time}</span>
                                </div>
                            </div>

                            {index < progressStages.length - 1 && (
                                <div className="workflow-connector-wave-bar">
                                    <svg className="workflow-wave-svg-element" viewBox="0 0 100 20" preserveAspectRatio="none">
                                        <path className="workflow-wave-bg-track" d="M 0 10 Q 25 2, 50 10 T 100 10" />
                                        <path className={`workflow-wave-active-fill ${stage.status === 'Complete' ? 'filled-complete' : stage.active ? 'filling-active' : ''}`} d="M 0 10 Q 25 2, 50 10 T 100 10" />
                                    </svg>
                                </div>
                            )}
                        </React.Fragment>
                    ))}
                </div>
            </section>

            {/* Bottom Panel: Executive Decision Summary */}
            <section className="ic-executive-decision-section">
                <div className="executive-decision-summary-card">
                    <div className="eds-header-row-flex">
                        <div className="eds-title-left-side">
                            <Briefcase size={18} className="eds-heading-icon" />
                            <h2 className="eds-card-main-title">Executive Decision & Prescriptive Mitigation Summary</h2>
                        </div>
                        <div className="eds-approval-badge status-pending">
                            AWAITING EXECUTOR AUTHORIZATION
                        </div>
                    </div>

                    <div className="eds-core-recommendation-alert-box">
                        <span className="eds-alert-action-label">IMMEDIATE MANDATORY STRATEGY ACTION REQUIRED:</span>
                        <p className="eds-alert-action-text">
                            Authorize dynamic redirection of fleet segment Bravo to Alternative Quarry Hub 7 (Rajasthan sector) via Bypass State Line 14 protocols to intercept full feedstock supply collapse at Plant A.
                        </p>
                    </div>

                    <div className="eds-mitigation-parameters-grid">
                        <div className="eds-parameter-cell">
                            <span className="ed-cell-lbl">Targeted Business Impact</span>
                            <span className="ed-cell-val highlight-brand">Avoid Complete Plant A Grinding Line Shutdown</span>
                        </div>
                        <div className="eds-parameter-cell">
                            <span className="ed-cell-lbl">Estimated Transit Pacing Variance</span>
                            <span className="ed-cell-val highlight-warning">+2.5 Hours Additional Cycle Time</span>
                        </div>
                        <div className="eds-parameter-cell">
                            <span className="ed-cell-lbl">Calculated Operational Overhead cost</span>
                            <span className="ed-cell-val highlight-warning">$14,200 Net Variance Allocation</span>
                        </div>
                        <div className="eds-parameter-cell">
                            <span className="ed-cell-lbl">Prescribed Alternative Supplier Node</span>
                            <span className="ed-cell-val font-semibold">Quarry Hub 7 Cluster (Rajasthan Industrial Block)</span>
                        </div>
                        <div className="eds-parameter-cell">
                            <span className="ed-cell-lbl">Rerouted Transport Routing Vector</span>
                            <span className="ed-cell-val font-semibold">Bypass Route State Line 14 Loop Area</span>
                        </div>
                        <div className="eds-parameter-cell">
                            <span className="ed-cell-lbl">Silo Raw Inventory Transfer Plan</span>
                            <span className="ed-cell-val font-semibold">Reallocate 400 Tons Inbound Clinker Bulk Mix Load</span>
                        </div>
                    </div>

                    <div className="eds-decision-action-footer-row">
                        <div className="eds-confidence-assurance-label">
                            Mitigation Optimization Engine Assurance Level Rating: <strong>97% Confidence Matrix Score</strong>
                        </div>
                        <div className="eds-action-buttons-group">
                            <button className="eds-btn-reject-action">Reject Plan</button>
                            <button className="eds-btn-approve-action">
                                Authorize Mitigation Protocols <ArrowRight size={14} />
                            </button>
                        </div>
                    </div>
                </div>
            </section>

        </div>
    );
}