// --- IncidentCenter.jsx ---
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
                if (response && response.success) {
                    setIncidentData(response.data);
                    setError(null);
                } else {
                    setError(new Error(response?.message || "Failed to load incident investigation details."));
                }
            } catch (err) {
                console.error("Failed to fetch incident center data:", err);
                setError(err);
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

    const handleAuthorize = () => {
        alert("Action has no backend implementation. Sourcing protocol authorization is disabled.");
    };

    const handleReject = () => {
        alert("Action has no backend implementation. Mitigation plan rejection is disabled.");
    };

    if (loading) {
        return (
            <div className="incident-center-scope flex-center" style={{ minHeight: '400px', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                <p style={{ color: 'var(--intel-text-s)' }}>Loading Incident Investigation Center...</p>
            </div>
        );
    }

    if (error && (!incidentData || !incidentData.incident_meta)) {
        const message = error.message || "";
        if (message.includes("pending") || message.includes("Initialize") || message.includes("query") || message.includes("execute") || message.includes("first")) {
            return (
                <div className="incident-center-scope flex-center-pending" style={{ minHeight: '500px', display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', gap: '16px', padding: '40px' }}>
                    <h1 className="ic-page-title">Incident Investigation Center</h1>
                    <div className="alert-badge critical" style={{ background: 'var(--intel-critical)', color: 'white', padding: '8px 16px', borderRadius: '6px', fontWeight: 'bold' }}>NO ACTIVE INVESTIGATION</div>
                    <p style={{ color: 'var(--intel-text-s)', fontSize: '15px', maxWidth: '500px', textAlign: 'center', marginTop: '10px' }}>
                        No active incident under investigation. Please head to the <strong>News Intelligence</strong> tab to execute an incident search query.
                    </p>
                </div>
            );
        }
        return (
            <div className="incident-center-scope flex-center" style={{ minHeight: '400px', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                <p className="text-critical">Error: {message}</p>
            </div>
        );
    }

    const incidentMeta = incidentData?.incident_meta || {};
    const extractedEntities = incidentData?.extracted_entities ?? [];
    const supportingSources = incidentData?.supporting_sources ?? [];
    const timelineSteps = incidentData?.timeline_steps ?? [];
    const impactCards = incidentData?.impact_cards ?? [];
    const progressStages = incidentData?.progress_stages ?? [];

    // Extract dynamic mitigation step metrics
    const mitigationStep = timelineSteps.find(step => step.id === 3);
    const mitigationRecommendation = mitigationStep?.reasoning || "Authorize dynamic route redirection and allocate alternative suppliers.";
    const targetedImpact = incidentMeta.originalHeadline ? `Avoid shut down of affected assets` : "Minimize raw material sourcing disruption";
    const delayVariance = mitigationStep?.metrics?.estDelay || "N/A";
    const overheadCost = mitigationStep?.metrics?.estCost || "N/A";
    const altSupplier = mitigationStep?.metrics?.alternate || "N/A";
    const routingVector = mitigationStep?.metrics?.route || "N/A";
    const confidenceScore = incidentMeta.confidence || "95%";

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
                        <span className="ic-ts-val font-mono">{liveTime}</span>
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
                            <h3 className="report-main-headline">{incidentMeta.originalHeadline}</h3>
                            <p className="report-main-body">{incidentMeta.originalBody}</p>
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
                                        <div className="src-score-block">
                                            <span className="src-score-val">{src.reliability} Reliability</span>
                                            <span className="src-status-pill">{src.status}</span>
                                        </div>
                                    </div>
                                ))}
                            </div>
                        </div>
                    </div>
                </div>

                {/* Center Panel: Chain Blast Radius Analysis */}
                <div className="ic-workspace-column column-center-blast">
                    <div className="column-head-wrapper">
                        <h2 className="column-section-title">Chain Blast Radius Analysis</h2>
                    </div>

                    <div className="ic-card-body-container">
                        <div className="impact-grid-cards">
                            {impactCards.map((card) => {
                                const CardIcon = iconMap[card.icon] || FileText;
                                return (
                                    <div key={card.id} className={`impact-measure-card status-${card.status}`}>
                                        <div className="card-top-header">
                                            <span className={`card-icon-badge ${card.status}`}>
                                                <CardIcon size={14} />
                                            </span>
                                            <span className="card-lbl-title">{card.title}</span>
                                        </div>
                                        <h4 className="card-impact-magnitude">{card.count}</h4>
                                        <p className="card-impact-desc">{card.desc}</p>
                                    </div>
                                );
                            })}
                        </div>
                    </div>
                </div>

                {/* Right Panel: Resolution Pipeline Stages */}
                <div className="ic-workspace-column column-right-pipeline">
                    <div className="column-head-wrapper">
                        <h2 className="column-section-title">Agentic Investigation Output</h2>
                    </div>

                    <div className="ic-card-body-container pipeline-vertical-scroller">
                        <div className="pipeline-steps-timeline">
                            {timelineSteps.map((step, idx) => (
                                <div key={step.id} className={`pipeline-step-node-card ${step.active ? 'active-highlight' : ''}`}>
                                    <div className="step-card-header">
                                        <h4 className="step-card-title-lbl">{step.title}</h4>
                                        <span className="step-agent-tag"><Cpu size={10} /> {step.agent}</span>
                                    </div>
                                    <div className="step-metrics-strip-row">
                                        {Object.entries(step.metrics || {}).map(([key, val]) => (
                                            <div key={key} className="step-metric-cell">
                                                <span className="sm-lbl">{key.replace(/([A-Z])/g, ' $1').trim()}</span>
                                                <span className="sm-val font-mono">{val}</span>
                                            </div>
                                        ))}
                                    </div>
                                    <div className="step-reasoning-textbox">
                                        <span className="textbox-title-tag">Agent Reason Logic:</span>
                                        <p className="textbox-paragraph-content">{step.reasoning}</p>
                                    </div>
                                    {idx < timelineSteps.length - 1 && (
                                        <div className="step-vertical-connector-line"></div>
                                    )}
                                </div>
                            ))}
                        </div>
                    </div>
                </div>

            </section>

            {/* Bottom Progress Tracker Breadcrumbs */}
            <section className="ic-progress-milestones-bar">
                <div className="milestones-flex-line">
                    {progressStages.map((stage, idx) => (
                        <React.Fragment key={stage.id}>
                            <div className={`milestone-node-element ${stage.active ? 'active-pulse' : ''} ${stage.status === 'Complete' ? 'state-complete' : 'state-pending'}`}>
                                <div className="node-circle-indicator">
                                    {stage.status === 'Complete' ? <CheckCircle2 size={14} /> : <HelpCircle size={14} />}
                                </div>
                                <div className="node-meta-block-text">
                                    <span className="node-step-lbl">{stage.name}</span>
                                    <span className="node-agent-name"><Cpu size={9} /> {stage.agent}</span>
                                    <span className="node-time-stamp font-mono">{stage.time}</span>
                                </div>
                            </div>
                            {idx < progressStages.length - 1 && (
                                <div className={`milestone-segment-line ${stage.status === 'Complete' ? 'state-complete' : 'state-pending'}`}>
                                    <svg width="100%" height="2" preserveAspectRatio="none">
                                        <line x1="0" y1="1" x2="100%" y2="1" strokeDasharray={stage.status !== 'Complete' ? "4 4" : "0"} strokeWidth="2" />
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
                        <p className="eds-alert-action-text">{mitigationRecommendation}</p>
                    </div>

                    <div className="eds-mitigation-parameters-grid">
                        <div className="eds-parameter-cell">
                            <span className="ed-cell-lbl">Targeted Business Impact</span>
                            <span className="ed-cell-val highlight-brand">{targetedImpact}</span>
                        </div>
                        <div className="eds-parameter-cell">
                            <span className="ed-cell-lbl">Estimated Transit Pacing Variance</span>
                            <span className="ed-cell-val highlight-warning">{delayVariance} Additional Cycle Time</span>
                        </div>
                        <div className="eds-parameter-cell">
                            <span className="ed-cell-lbl">Calculated Operational Overhead cost</span>
                            <span className="ed-cell-val highlight-warning">{overheadCost} Net Variance Allocation</span>
                        </div>
                        <div className="eds-parameter-cell">
                            <span className="ed-cell-lbl">Prescribed Alternative Supplier Node</span>
                            <span className="ed-cell-val font-semibold">{altSupplier}</span>
                        </div>
                        <div className="eds-parameter-cell">
                            <span className="ed-cell-lbl">Rerouted Transport Routing Vector</span>
                            <span className="ed-cell-val font-semibold">{routingVector}</span>
                        </div>
                        <div className="eds-parameter-cell">
                            <span className="ed-cell-lbl">Silo Raw Inventory Transfer Plan</span>
                            <span className="ed-cell-val font-semibold">Reallocate inbound raw material bulk mixes</span>
                        </div>
                    </div>

                    <div className="eds-decision-action-footer-row">
                        <div className="eds-confidence-assurance-label">
                            Mitigation Optimization Engine Assurance Level Rating: <strong>{confidenceScore} Confidence Matrix Score</strong>
                        </div>
                        <div className="eds-action-buttons-group">
                            <button className="eds-btn-reject-action" onClick={handleReject}>Reject Plan</button>
                            <button className="eds-btn-approve-action" onClick={handleAuthorize}>
                                Authorize Mitigation Protocols <ArrowRight size={14} />
                            </button>
                        </div>
                    </div>
                </div>
            </section>

        </div>
    );
}