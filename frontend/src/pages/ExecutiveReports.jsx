// --- ExecutiveReports.jsx ---
import React, { useState, useEffect } from 'react';
import {
    FileText, AlertTriangle, Clock, ThumbsUp, ChevronRight, Download,
    FileDown, RefreshCw, Share2, Eye, Copy, CheckCircle2,
    Layers, TrendingUp, BarChart2, Shield, Calendar, User, AlertCircle
} from 'lucide-react';
import reportService from '../services/reportService';
import '../styles/executive-reports.css';

// Icon mapping dictionary for dynamic string-based icons from backend API
const ICON_MAP = {
    FileText,
    AlertTriangle,
    Clock,
    ThumbsUp,
    TrendingUp,
    BarChart2,
    Shield
};

export default function ExecutiveReports() {
    const [reportData, setReportData] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [selectedReportId, setSelectedReportId] = useState('');

    const fetchExecutiveReports = async () => {
        try {
            setLoading(true);
            setError(null);
            const response = await reportService.getExecutiveReports();
            if (response && response.success) {
                setReportData(response.data);
                setError(null);
                // Automatically select the first report from history if available
                if (response.data?.report_history && response.data.report_history.length > 0) {
                    setSelectedReportId(response.data.report_history[0].id);
                }
            } else {
                setError(new Error(response?.message || "Failed to load executive reports from service."));
            }
        } catch (err) {
            console.error('Failed to fetch executive reports:', err);
            setError(err);
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchExecutiveReports();
    }, []);

    // Print A4 Document to PDF
    const handleExportPDF = () => {
        window.print();
    };

    // Export report document as markdown
    const handleExportMarkdown = (selectedReport) => {
        if (!selectedReport) return;
        const element = document.createElement("a");
        const file = new Blob([
            `# ${selectedReport.title}\n\n`,
            `**Report ID:** ${selectedReport.id}\n`,
            `**Date:** ${selectedReport.date}\n`,
            `**Incident:** ${selectedReport.incident}\n`,
            `**Severity:** ${selectedReport.severity}\n\n`,
            `## Executive Summary\n${selectedReport.summary}\n\n`,
            `## Business Impact\n`,
            `- Operational: ${selectedReport.business_impact?.operational}\n`,
            `- Financial: ${selectedReport.business_impact?.financial}\n`,
            `- Production: ${selectedReport.business_impact?.production}\n`,
            `- Continuity: ${selectedReport.business_impact?.continuity}\n\n`,
            `## Sourcing Vector\n`,
            `- Primary Hub: ${selectedReport.sourcing_vector?.[0]?.hub}\n`,
            `- Material Core: ${selectedReport.sourcing_vector?.[0]?.material}\n`,
            `- Disruption Context: ${selectedReport.sourcing_vector?.[0]?.impact}\n`,
            `- Alternate Node: ${selectedReport.sourcing_vector?.[0]?.alternate}\n\n`,
            `## Sourcing Mitigation Plan\n`,
            selectedReport.mitigation_bullets?.map((bullet, idx) => `${idx + 1}. ${bullet}`).join('\n')
        ], { type: 'text/markdown' });
        element.href = URL.createObjectURL(file);
        element.download = `${selectedReport.id}.md`;
        document.body.appendChild(element);
        element.click();
        document.body.removeChild(element);
    };

    // Copy summary snippet to clipboard
    const handleShareReport = (selectedReport) => {
        if (!selectedReport) return;
        navigator.clipboard.writeText(selectedReport.summary);
        alert("Report summary copied to clipboard!");
    };

    const handleDownloadPayload = (row) => {
        const element = document.createElement("a");
        const file = new Blob([JSON.stringify(row, null, 2)], { type: 'application/json' });
        element.href = URL.createObjectURL(file);
        element.download = `${row.id}_payload.json`;
        document.body.appendChild(element);
        element.click();
        document.body.removeChild(element);
    };

    const handleDuplicateReport = () => {
        alert("Action has no backend implementation. Duplicate report function is disabled.");
    };

    const handleShareVector = () => {
        alert("Action has no backend implementation. Share vector function is disabled.");
    };

    // --- RENDER LOADING STATE ---
    if (loading) {
        return (
            <div className="er-content-scope">
                <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', minHeight: '400px', gap: '1rem' }}>
                    <RefreshCw className="animate-spin text-brand" size={32} />
                    <p style={{ color: 'var(--text-secondary, #64748b)', fontSize: '0.95rem' }}>Loading Executive Reports & Analysis Payload...</p>
                </div>
            </div>
        );
    }

    // --- RENDER ERROR STATE ---
    if (error && (!reportData || !reportData.report_history)) {
        const message = error.message || "";
        if (message.includes("pending") || message.includes("Initialize") || message.includes("query") || message.includes("execute") || message.includes("first")) {
            return (
                <div className="er-content-scope flex-center-pending" style={{ minHeight: '500px', display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', gap: '16px', padding: '40px' }}>
                    <h1 className="er-page-title">Executive Reports</h1>
                    <div className="alert-badge critical" style={{ background: 'var(--intel-critical)', color: 'white', padding: '8px 16px', borderRadius: '6px', fontWeight: 'bold' }}>NO ACTIVE REPORT</div>
                    <p style={{ color: 'var(--intel-text-s)', fontSize: '15px', maxWidth: '500px', textAlign: 'center', marginTop: '10px' }}>
                        No active reports compiled. Please head to the <strong>News Intelligence</strong> tab to execute an incident search query.
                    </p>
                </div>
            );
        }
        return (
            <div className="er-content-scope">
                <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', minHeight: '400px', gap: '1rem', textAlign: 'center' }}>
                    <AlertCircle className="text-critical" size={40} />
                    <h3 style={{ fontSize: '1.2rem', fontWeight: 600 }}>Failed to Load Reports</h3>
                    <p style={{ color: 'var(--text-secondary, #64748b)', maxWidth: '480px' }}>{message}</p>
                    <button className="er-btn-action-trigger primary-brand" onClick={fetchExecutiveReports} style={{ width: 'auto', padding: '0.5rem 1.25rem' }}>
                        <RefreshCw size={14} /> <span>Retry Request</span>
                    </button>
                </div>
            </div>
        );
    }

    const reportMeta = reportData?.report_meta;
    const kpis = reportData?.kpis ?? [];
    const qualityMetrics = reportData?.quality_metrics ?? [];
    const timelineActivity = reportData?.timeline_activity ?? [];
    const reportHistory = reportData?.report_history ?? [];

    const selectedReport = reportHistory.find(r => r.id === selectedReportId) || reportHistory[0];

    return (
        <div className="er-content-scope">

            {/* Page Title Block Area */}
            <header className="er-header-block">
                <div className="er-header-left">
                    <h1 className="er-page-title">Executive Reports</h1>
                    <p className="er-page-subtitle">AI-generated executive reports for supply chain disruptions and strategic decision making.</p>
                </div>
                <div className="er-header-right">
                    <div className="er-header-pill">
                        <Clock size={13} />
                        <span className="er-pill-lbl">Latest Update:</span>
                        <span className="er-pill-val font-mono">{selectedReport?.creationTime ? selectedReport.creationTime.split(' ')[1] : '10:37:43'}</span>
                    </div>
                    <div className="er-header-pill">
                        <span className="er-status-dot-active"></span>
                        <span className="er-pill-lbl">Status:</span>
                        <span className="er-pill-val text-success">Synced</span>
                    </div>
                    <div className="er-header-pill font-semibold text-brand">
                        <Shield size={13} />
                        <span>{selectedReport?.confidence || reportMeta?.confidence || '96.4%'} AI Conf</span>
                    </div>
                </div>
            </header>

            {/* Top Corporate KPI Row Section */}
            <section className="er-kpi-grid">
                {kpis.map((kpi, index) => {
                    const KpiIcon = ICON_MAP[kpi.icon] || FileText;
                    return (
                        <div key={kpi.id || index} className="er-kpi-card">
                            <div className="er-kpi-header-flex">
                                <span className="er-kpi-lbl">{kpi.title}</span>
                                <span className={`er-kpi-icon-container variant-${kpi.status}`}>
                                    <KpiIcon size={16} />
                                </span>
                            </div>
                            <h3 className="er-kpi-val-text">{kpi.value}</h3>
                            <p className="er-kpi-trend-meta">
                                <span className={`er-trend-indicator text-${kpi.status}`}>
                                    {kpi.trend || kpi.desc}
                                </span>
                            </p>
                        </div>
                    );
                })}
            </section>

            {/* Responsive Main Content Grid Arrangement */}
            <div className="er-workspace-layout-grid">

                {/* Left Workspace Panel: Premium White Paper Consulting Style Report Preview */}
                <div className="er-panel-column col-left-preview">
                    <h2 className="er-panel-section-title">Report Preview Workspace</h2>

                    <article className="er-premium-a4-document-paper">

                        {/* A4 Executive Document Header Block */}
                        <div className="er-doc-header-block">
                            <div className="er-doc-title-meta">
                                <span className="er-doc-tag-priority">BOARD-LEVEL DISRUPTION DISPATCH</span>
                                <h2 className="er-doc-main-heading">{selectedReport?.title || 'STRATEGIC RISK & MITIGATION REPORT'}</h2>
                                <p className="er-doc-sub-text">Evaluation of structural transit bottlenecks and inventory re-allocation protocols.</p>
                            </div>
                            <div className="er-doc-id-stamp">
                                <span className="font-mono font-semibold text-brand">{selectedReport?.id || selectedReportId}</span>
                            </div>
                        </div>

                        {/* Executive Summary Section */}
                        <section className="er-doc-content-section">
                            <h3 className="er-doc-section-title-heading">I. Executive Summary</h3>
                            <p className="er-doc-paragraph-text">{selectedReport?.summary}</p>
                        </section>

                        {/* Incident Summary Technical Section */}
                        <section className="er-doc-content-section">
                            <h3 className="er-doc-section-title-heading">II. Incident Diagnostic Summary</h3>
                            <div className="er-doc-key-value-grid columns-3">
                                <div className="er-doc-kv-cell"><span className="er-doc-lbl">Incident ID</span><p className="font-mono">{selectedReport?.diagnostic?.incident_id}</p></div>
                                <div className="er-doc-kv-cell"><span className="er-doc-lbl">Severity Rank</span><p className={`${(selectedReport?.diagnostic?.severity || '').includes('Critical') ? 'text-critical' : 'text-warning'} font-semibold`}>{selectedReport?.diagnostic?.severity}</p></div>
                                <div className="er-doc-kv-cell"><span className="er-doc-lbl">Geographic Node</span><p>{selectedReport?.diagnostic?.location}</p></div>
                                <div className="er-doc-kv-cell"><span className="er-doc-lbl">Detection Datetime</span><p className="font-mono">{selectedReport?.diagnostic?.date}</p></div>
                                <div className="er-doc-kv-cell"><span className="er-doc-lbl">Orchestration Phase</span><p className="text-warning font-semibold">{selectedReport?.diagnostic?.phase}</p></div>
                                <div className="er-doc-kv-cell"><span className="er-doc-lbl">Affected Network Vector</span><p>{selectedReport?.diagnostic?.vector}</p></div>
                            </div>
                        </section>

                        {/* Enterprise Business Impact Structural Matrix */}
                        <section className="er-doc-content-section">
                            <h3 className="er-doc-section-title-heading">III. Multi-Agent Business Impact Matrix</h3>
                            <div className="er-doc-key-value-grid columns-2">
                                <div className="er-doc-kv-cell">
                                    <span className="er-doc-lbl">Operational Constraint Impact</span>
                                    <p>{selectedReport?.business_impact?.operational}</p>
                                </div>
                                <div className="er-doc-kv-cell">
                                    <span className="er-doc-lbl">Financial Impact Vector</span>
                                    <p>{selectedReport?.business_impact?.financial}</p>
                                </div>
                                <div className="er-doc-kv-cell">
                                    <span className="er-doc-lbl">Production Yield Impact</span>
                                    <p>{selectedReport?.business_impact?.production}</p>
                                </div>
                                <div className="er-doc-kv-cell">
                                    <span className="er-doc-lbl">Business Continuity Index</span>
                                    <p>{selectedReport?.business_impact?.continuity}</p>
                                </div>
                            </div>
                        </section>

                        {/* Affected Industrial Infrastructure Assets */}
                        <section className="er-doc-content-section">
                            <h3 className="er-doc-section-title-heading">IV. Affected Plant Infrastructure Nodes</h3>
                            <div className="er-doc-key-value-grid columns-2">
                                {selectedReport?.affected_plants?.map((plant, idx) => (
                                    <div key={idx} className={`er-doc-kv-cell border-left-${plant.status.includes('Critical') ? 'critical' : 'success'}`}>
                                        <h4 className="er-doc-node-title">{plant.name}</h4>
                                        <div className="er-doc-node-details">
                                            <span className={`${plant.status.includes('Critical') ? 'text-critical' : 'text-success'} font-semibold`}>{plant.status}</span> | {plant.buffer}
                                        </div>
                                    </div>
                                ))}
                            </div>
                        </section>

                        {/* Affected Enterprise Suppliers Sourcing Mapping */}
                        <section className="er-doc-content-section">
                            <h3 className="er-doc-section-title-heading">V. Sourcing Vector & Supplier Analysis</h3>
                            <div className="er-doc-table-inner-wrapper">
                                <table className="er-doc-inner-data-table">
                                    <thead>
                                        <tr>
                                            <th>Primary Sourcing Hub</th>
                                            <th>Material Core</th>
                                            <th>Disruption Impact Context</th>
                                            <th>Prescribed Alternate Node</th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                        {selectedReport?.sourcing_vector?.map((row, idx) => (
                                            <tr key={idx}>
                                                <td className="font-semibold text-brand">{row.hub}</td>
                                                <td>{row.material}</td>
                                                <td className="text-critical font-semibold">{row.impact}</td>
                                                <td className="text-success font-semibold">{row.alternate}</td>
                                            </tr>
                                        ))}
                                    </tbody>
                                </table>
                            </div>
                        </section>

                        {/* Silo Inventory Analysis Metric Allocations */}
                        <section className="er-doc-content-section">
                            <h3 className="er-doc-section-title-heading">VI. Silo Inventory & Buffer Analysis</h3>
                            <div className="er-doc-key-value-grid columns-4">
                                <div className="er-doc-kv-cell"><span className="er-doc-lbl">Current Stock Balance</span><p className="font-mono">{selectedReport?.silo_inventory?.stock}</p></div>
                                <div className="er-doc-kv-cell"><span className="er-doc-lbl">Safety Stock Target</span><p className="font-mono text-secondary">{selectedReport?.silo_inventory?.safety}</p></div>
                                <div className="er-doc-kv-cell"><span className="er-doc-lbl">Remaining Operating Horizon</span><p className="text-critical font-semibold">{selectedReport?.silo_inventory?.horizon}</p></div>
                                <div className="er-doc-kv-cell"><span className="er-doc-lbl">Critical Material Flag</span><p className="text-critical font-semibold">{selectedReport?.silo_inventory?.material}</p></div>
                            </div>
                        </section>

                        {/* Comprehensive Financial Cost Estimation Variables */}
                        <section className="er-doc-content-section">
                            <h3 className="er-doc-section-title-heading">VII. Financial Impact & Sourcing Cost Analysis</h3>
                            <div className="er-doc-key-value-grid columns-4">
                                <div className="er-doc-kv-cell"><span className="er-doc-lbl">Estimated Baseline Loss</span><p className="font-mono">{selectedReport?.financial_analysis?.baseline_loss}</p></div>
                                <div className="er-doc-kv-cell"><span className="er-doc-lbl">Recovery Cycle Cost</span><p className="font-mono">{selectedReport?.financial_analysis?.recovery_cost}</p></div>
                                <div className="er-doc-kv-cell"><span className="er-doc-lbl">Mitigation Structural Cost</span><p className="font-mono">{selectedReport?.financial_analysis?.mitigation_cost}</p></div>
                                <div className="er-doc-kv-cell"><span className="er-doc-lbl">Net Saved Value Matrix</span><p className="text-success font-semibold font-mono">{selectedReport?.financial_analysis?.net_saved}</p></div>
                            </div>
                        </section>

                        {/* Network Latency and Expected Delay Realizations */}
                        <section className="er-doc-content-section">
                            <h3 className="er-doc-section-title-heading">VIII. Network Delay & Logistics Latency Profiling</h3>
                            <div className="er-doc-key-value-grid columns-3">
                                <div className="er-doc-kv-cell"><span className="er-doc-lbl">Expected Transit Latency</span><p className="font-mono">{selectedReport?.logistics_latency?.latency}</p></div>
                                <div className="er-doc-kv-cell"><span className="er-doc-lbl">Recovery Window Time</span><p className="font-mono">{selectedReport?.logistics_latency?.recovery_window}</p></div>
                                <div className="er-doc-kv-cell"><span className="er-doc-lbl">Affected Fleet Deliveries</span><p className="font-semibold text-brand">{selectedReport?.logistics_latency?.deliveries}</p></div>
                            </div>
                        </section>

                        {/* Prescribed Strategic Multi-Agent Mitigation Execution Roadmap */}
                        <section className="er-doc-content-section">
                            <h3 className="er-doc-section-title-heading">IX. Autonomous Sourcing Mitigation Plan</h3>
                            <div className="er-doc-mitigation-bullet-stack">
                                {selectedReport?.mitigation_bullets?.map((bullet, idx) => (
                                    <div key={idx} className="er-doc-bullet-item">
                                        <strong>Directive Action Step {idx + 1}:</strong> {bullet}
                                    </div>
                                ))}
                                <div className="er-doc-bullet-item er-highlight-box">
                                    <strong>Autonomous Agent Recommendation:</strong> {selectedReport?.summary}
                                </div>
                            </div>
                        </section>

                        {/* Document Validation Footer Stamp Area */}
                        <footer className="er-doc-footer-signature-area">
                            <div className="er-doc-footer-row">
                                <span className="er-signature-lbl">Orchestration Pool Authorization:</span>
                                <span className="er-signature-val font-semibold">{selectedReport?.author || reportMeta?.generatedBy}</span>
                            </div>
                            <div className="er-doc-footer-row split">
                                <div><span className="er-signature-lbl">Generation Datetime:</span> <span className="font-mono er-signature-val">{selectedReport?.creationTime || reportMeta?.creationTime}</span></div>
                                <div><span className="er-signature-lbl">Autonomous Confidence:</span> <span className="font-mono text-success er-signature-val">{selectedReport?.confidence || reportMeta?.confidence}</span></div>
                            </div>
                        </footer>

                    </article>
                </div>

                {/* Right Panel Workspace: Report Meta Information, Metrics, Actions, and Audit Trails */}
                <div className="er-panel-column col-right-sidebar">

                    {/* Report Information Metadata Architecture Section */}
                    <div className="er-sidebar-widget-card">
                        <h3 className="er-widget-card-title">Report Meta Profile</h3>
                        <div className="er-meta-properties-stack">
                            <div className="er-property-row"><span>Report ID Identification</span><strong className="font-mono text-brand">{selectedReport?.id}</strong></div>
                            <div className="er-property-row"><span>System Generation Core</span><span className="er-txt-truncate">{selectedReport?.author || reportMeta?.generatedBy}</span></div>
                            <div className="er-property-row"><span>Creation Compiled Time</span><span className="font-mono">{selectedReport?.creationTime || reportMeta?.creationTime}</span></div>
                            <div className="er-property-row"><span>Report Build Version</span><span className="font-mono">{selectedReport?.version || reportMeta?.version}</span></div>
                            <div className="er-property-row"><span>AI Model Confidence</span><strong className="font-mono text-success">{selectedReport?.confidence || reportMeta?.confidence}</strong></div>
                            <div className="er-property-row"><span>Board Approval Status</span><span className="er-badge-status status-success">{selectedReport?.status || reportMeta?.status}</span></div>
                            <div className="er-property-row"><span>Enterprise Disruption Rank</span><span className="er-badge-status status-critical">{selectedReport?.priority || reportMeta?.priority}</span></div>
                            <div className="er-property-row"><span>Estimated Reading Time</span><span>{selectedReport?.readingTime || reportMeta?.readingTime}</span></div>
                        </div>
                    </div>

                    {/* AI Document Quality Metric Indicators Progress Panels */}
                    <div className="er-sidebar-widget-card">
                        <h3 className="er-widget-card-title">AI Report Evaluation Quality</h3>
                        <div className="er-metrics-bars-stack">
                            {qualityMetrics.map((metric, index) => (
                                <div key={index} className="er-metric-bar-item">
                                    <div className="er-metric-labels-row">
                                        <span className="er-metric-name-txt">{metric.label}</span>
                                        <span className="er-metric-value-txt font-mono font-semibold">{metric.score}%</span>
                                    </div>
                                    <div className="er-progress-track-frame">
                                        <span className="er-progress-fill-element" style={{ width: `${metric.score}%` }}></span>
                                    </div>
                                </div>
                            ))}
                        </div>
                    </div>

                    {/* Premium Enterprise Corporate Action Export Center */}
                    <div className="er-sidebar-widget-card">
                        <h3 className="er-widget-card-title">Corporate Export Center</h3>
                        <div className="er-export-actions-grid-layout">
                            <button className="er-btn-action-trigger primary-brand" onClick={handleExportPDF}>
                                <FileDown size={14} /> <span>Export Board PDF</span>
                            </button>
                            <button className="er-btn-action-trigger secondary-outline" onClick={() => handleExportMarkdown(selectedReport)}>
                                <FileText size={14} /> <span>Export Markdown</span>
                            </button>
                            <button className="er-btn-action-trigger secondary-outline" onClick={fetchExecutiveReports}>
                                <RefreshCw size={14} /> <span>Regenerate Analysis</span>
                            </button>
                            <button className="er-btn-action-trigger secondary-outline" onClick={() => handleShareReport(selectedReport)}>
                                <Share2 size={14} /> <span>Share Report Pipeline</span>
                            </button>
                        </div>
                    </div>

                    {/* Multi-Agent Sequential Timeline Activity Trail */}
                    <div className="er-sidebar-widget-card">
                        <h3 className="er-widget-card-title">Recent Report Ingestion Activity</h3>
                        <div className="er-sequential-timeline-track">
                            {timelineActivity.map((activity, index) => (
                                <div key={activity.id || index} className="er-timeline-activity-node-row">
                                    <div className="er-timeline-left-icon-pillar">
                                        <span className="er-timeline-node-dot"></span>
                                        <span className="er-timeline-pillar-line"></span>
                                    </div>
                                    <div className="er-timeline-node-content-box">
                                        <div className="er-timeline-node-header">
                                            <strong className="er-timeline-event-name">{activity.event}</strong>
                                            <span className="er-timeline-node-time font-mono">{activity.time}</span>
                                        </div>
                                        <p className="er-timeline-node-description">{activity.desc}</p>
                                    </div>
                                </div>
                            ))}
                        </div>
                    </div>

                </div>
            </div>

            {/* Bottom Section Layout Panel: Comprehensive Enterprise Historical Report Log Table */}
            <section className="er-historical-report-log-table-section">
                <div className="er-section-title-wrapper border-bottom-sync">
                    <Layers size={16} className="er-section-title-icon" />
                    <h2 className="er-section-title">Historical Report Compilation Registry</h2>
                </div>

                <div className="er-responsive-table-scroll-window">
                    <table className="er-enterprise-data-table-element">
                        <thead>
                            <tr>
                                <th>Report ID</th>
                                <th>Compilation Date</th>
                                <th>Disruption Incident Scope</th>
                                <th>Severity Tier</th>
                                <th>Registry Status</th>
                                <th>Responsible Agent Core</th>
                                <th>Build Version</th>
                                <th className="text-right">Enterprise Document Actions</th>
                            </tr>
                        </thead>
                        <tbody>
                            {reportHistory.map((row, index) => (
                                <tr key={row.id || index} className={row.id === selectedReportId ? 'er-row-state-active-selected' : ''}>
                                    <td className="font-semibold text-brand font-mono">{row.id}</td>
                                    <td className="font-mono text-secondary">{row.date}</td>
                                    <td className="er-table-incident-cell-truncate" title={row.incident}>{row.incident}</td>
                                    <td>
                                        <span className={`er-table-tag-badge severity-${(row.severity || '').toLowerCase()}`}>
                                            {row.severity}
                                        </span>
                                    </td>
                                    <td>
                                        <span className="er-table-status-cell-flex">
                                            <span className={`er-table-status-dot state-${(row.status || '').toLowerCase()}`}></span>
                                            <span className="font-semibold">{row.status}</span>
                                        </span>
                                    </td>
                                    <td className="text-secondary">{row.author}</td>
                                    <td className="font-mono text-secondary">{row.version}</td>
                                    <td className="text-right">
                                        <div className="er-table-actions-flex-wrapper">
                                            <button className="er-table-btn-icon-link" title="View Document Preview" onClick={() => setSelectedReportId(row.id)}>
                                                <Eye size={13} />
                                            </button>
                                            <button className="er-table-btn-icon-link" title="Download Payload Bundle" onClick={() => handleDownloadPayload(row)}>
                                                <Download size={13} />
                                            </button>
                                            <button className="er-table-btn-icon-link" title="Duplicate Constraints Structure" onClick={handleDuplicateReport}>
                                                <Copy size={13} />
                                            </button>
                                            <button className="er-table-btn-icon-link" title="Share Enterprise Vector" onClick={handleShareVector}>
                                                <Share2 size={13} />
                                            </button>
                                        </div>
                                    </td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </div>
            </section>

        </div>
    );
}