// ExecutiveReports.jsx
import React, { useState } from 'react';
import {
    FileText, AlertTriangle, Clock, ThumbsUp, ChevronRight, Download,
    FileDown, RefreshCw, Share2, Eye, Copy, CheckCircle2,
    Layers, TrendingUp, BarChart2, Shield, Calendar, User
} from 'lucide-react';
import '../styles/executive-reports.css';

// --- ENTERPRISE STATIC MOCK DATA ---
const kpiData = [
    { id: 1, title: 'Reports Generated', value: '1,248', trend: '+12% this month', status: 'success', icon: FileText },
    { id: 2, title: 'Critical Reports', value: '14 Active', trend: '2 resolved today', status: 'critical', icon: AlertTriangle },
    { id: 3, title: 'Avg Generation Time', value: '4.2s', desc: 'Real-time optimization', status: 'brand', icon: Clock },
    { id: 4, title: 'Executive Approval', value: '98.6%', trend: '0% override fallback', status: 'success', icon: ThumbsUp }
];

const mockReportMeta = {
    id: 'REP-2026-NX48',
    generatedBy: 'Autonomous News Intelligence & Mitigation Agent Pool',
    creationTime: '2026-07-17 10:32:15',
    version: 'v3.4.1 (Stable)',
    confidence: '96.4%',
    status: 'Approved for Board Review',
    priority: 'Critical / Tier 1 Risk',
    readingTime: '3 min read'
};

const qualityMetrics = [
    { label: 'Report Completeness', score: 100 },
    { label: 'Data Accuracy Vector', score: 98 },
    { label: 'Business Readiness Matrix', score: 96 },
    { label: 'Empirical Evidence Score', score: 94 },
    { label: 'Knowledge Graph Intersect', score: 100 }
];

const timelineActivity = [
    { id: 1, event: 'Report Generated', desc: 'AI agent pool finalized clinker mitigation parameters.', time: '10:32:15' },
    { id: 2, event: 'Manager Reviewed', desc: 'Automated verification against historical constraints.', time: '10:34:02' },
    { id: 3, event: 'AI Updated Graph', desc: 'Knowledge database re-indexed regional transit vectors.', time: '10:34:10' },
    { id: 4, event: 'Shared with Operations', desc: 'Secure payload broadcast to dispatch control towers.', time: '10:35:00' },
    { id: 5, event: 'Executive Board Approved', desc: 'System baseline digital signature authorized.', time: '10:36:44' }
];

const reportHistory = [
    { id: 'REP-2026-NX48', date: '2026-07-17', incident: 'NH-48 Monsoon Inundation Corridor Anomaly', severity: 'Critical', status: 'Approved', author: 'Mitigation Agent', version: 'v3.4.1' },
    { id: 'REP-2026-CL82', date: '2026-07-15', incident: 'Madhya Pradesh Off-Peak Grid Outage', severity: 'Medium', status: 'Archived', author: 'Sourcing Engine', version: 'v1.2.0' },
    { id: 'REP-2026-FL11', date: '2026-07-10', incident: 'Valsad Quarry Material Payload Variance', severity: 'High', status: 'Approved', author: 'Impact Agent', version: 'v2.1.0' },
    { id: 'REP-2026-GY04', date: '2026-07-04', incident: 'Terminal Port Wait Lane Diesel Overhead', severity: 'Low', status: 'Reviewed', author: 'News Intel Agent', version: 'v1.0.4' }
];

export default function ExecutiveReports() {
    const [selectedReportId, setSelectedReportId] = useState('REP-2026-NX48');

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
                        <span className="er-pill-val font-mono">10:37:43</span>
                    </div>
                    <div className="er-header-pill">
                        <span className="er-status-dot-active"></span>
                        <span className="er-pill-lbl">Status:</span>
                        <span className="er-pill-val text-success">Synced</span>
                    </div>
                    <div className="er-header-pill font-semibold text-brand">
                        <Shield size={13} />
                        <span>96.4% AI Conf</span>
                    </div>
                </div>
            </header>

            {/* Top Corporate KPI Row Section */}
            <section className="er-kpi-grid">
                {kpiData.map((kpi) => {
                    const KpiIcon = kpi.icon;
                    return (
                        <div key={kpi.id} className="er-kpi-card">
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
                                <h2 className="er-doc-main-heading">STRATEGIC RISK & MITIGATION REPORT</h2>
                                <p className="er-doc-sub-text">Evaluation of structural transit bottlenecks and inventory re-allocation protocols.</p>
                            </div>
                            <div className="er-doc-id-stamp">
                                <span className="font-mono font-semibold text-brand">{selectedReportId}</span>
                            </div>
                        </div>

                        {/* Executive Summary Section */}
                        <section className="er-doc-content-section">
                            <h3 className="er-doc-section-title-heading">I. Executive Summary</h3>
                            <p className="er-doc-paragraph-text">
                                Autonomous supply chain analytics clusters have detected structural disruptions on the NH-48 logistics vector via localized flash flooding.
                                Immediate structural impacts are projected across the Western Grinding Complex (Plant A).
                                This document outlines immediate mitigation protocols, emergency quarry sourcing contracts, and rail transport bypass allocation to sustain baseline clinker processing.
                            </p>
                        </section>

                        {/* Incident Summary Technical Section */}
                        <section className="er-doc-content-section">
                            <h3 className="er-doc-section-title-heading">II. Incident Diagnostic Summary</h3>
                            <div className="er-doc-key-value-grid columns-3">
                                <div className="er-doc-kv-cell"><span className="er-doc-lbl">Incident ID</span><p className="font-mono">INC-2026-FL08</p></div>
                                <div className="er-doc-kv-cell"><span className="er-doc-lbl">Severity Rank</span><p className="text-critical font-semibold">Critical / Tier 1 Risk</p></div>
                                <div className="er-doc-kv-cell"><span className="er-doc-lbl">Geographic Node</span><p>Gujarat East Corridor</p></div>
                                <div className="er-doc-kv-cell"><span className="er-doc-lbl">Detection Datetime</span><p className="font-mono">2026-07-17 10:32:15</p></div>
                                <div className="er-doc-kv-cell"><span className="er-doc-lbl">Orchestration Phase</span><p className="text-warning font-semibold">Mitigation Deployment Active</p></div>
                                <div className="er-doc-kv-cell"><span className="er-doc-lbl">Affected Network Vector</span><p>NH-48 Fleet Loop Bypass</p></div>
                            </div>
                        </section>

                        {/* Enterprise Business Impact Structural Matrix */}
                        <section className="er-doc-content-section">
                            <h3 className="er-doc-section-title-heading">III. Multi-Agent Business Impact Matrix</h3>
                            <div className="er-doc-key-value-grid columns-2">
                                <div className="er-doc-kv-cell">
                                    <span className="er-doc-lbl">Operational Constraint Impact</span>
                                    <p>Limestone bulk cargo haulage vector completely obstructed. Inbound pipeline latency scales by +36 hours until structural water recedes.</p>
                                </div>
                                <div className="er-doc-kv-cell">
                                    <span className="er-doc-lbl">Financial Impact Vector</span>
                                    <p>Estimated structural loss exposure capped at $42,500 without intervention. Prescribed mitigation reduces downstream asset exposure to negligible spot variance.</p>
                                </div>
                                <div className="er-doc-kv-cell">
                                    <span className="er-doc-lbl">Production Yield Impact</span>
                                    <p>Plant A clinker raw mill buffer drawdown down to 1.5 days. Risks complete operational stoppage if backup sourcing is delayed past the 24-hour safety threshold.</p>
                                </div>
                                <div className="er-doc-kv-cell">
                                    <span className="er-doc-lbl">Business Continuity Index</span>
                                    <p>Alternate inter-modal nodes retain 94% network resilience capacity. Strategic reserve triggers are fully operational across peripheral kilns.</p>
                                </div>
                            </div>
                        </section>

                        {/* Affected Industrial Infrastructure Assets */}
                        <section className="er-doc-content-section">
                            <h3 className="er-doc-section-title-heading">IV. Affected Plant Infrastructure Nodes</h3>
                            <div className="er-doc-key-value-grid columns-2">
                                <div className="er-doc-kv-cell border-left-critical">
                                    <h4 className="er-doc-node-title">Plant A - Western Grinding Complex</h4>
                                    <div className="er-doc-node-details"><span className="text-critical font-semibold">Critical Risk Exposure</span> | Buffer: 1.5 Days Remaining</div>
                                </div>
                                <div className="er-doc-kv-cell border-left-success">
                                    <h4 className="er-doc-node-title">Plant C - Southern Port Terminal</h4>
                                    <div className="er-doc-node-details"><span className="text-success font-semibold">Nominal Baseline</span> | Strategic Surplus: 10 Days Buffer</div>
                                </div>
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
                                        <tr>
                                            <td className="font-semibold text-brand">Valsad Quarry Hub</td>
                                            <td>Limestone Bulk</td>
                                            <td className="text-critical font-semibold">Complete Sourcing Obstruction</td>
                                            <td className="text-success font-semibold">Rajasthan Emergency Quarry</td>
                                        </tr>
                                        <tr>
                                            <td className="font-semibold text-brand">NTPC Cluster Node</td>
                                            <td>Fly Ash Matrix</td>
                                            <td className="text-success">Minor Route Flow Latency</td>
                                            <td>Baseline Retained</td>
                                        </tr>
                                    </tbody>
                                </table>
                            </div>
                        </section>

                        {/* Silo Inventory Analysis Metric Allocations */}
                        <section className="er-doc-content-section">
                            <h3 className="er-doc-section-title-heading">VI. Silo Inventory & Buffer Analysis</h3>
                            <div className="er-doc-key-value-grid columns-4">
                                <div className="er-doc-kv-cell"><span className="er-doc-lbl">Current Stock Balance</span><p className="font-mono">6,200 T</p></div>
                                <div className="er-doc-kv-cell"><span className="er-doc-lbl">Safety Stock Target</span><p className="font-mono text-secondary">15,000 T</p></div>
                                <div className="er-doc-kv-cell"><span className="er-doc-lbl">Remaining Operating Horizon</span><p className="text-critical font-semibold">1.5 Days</p></div>
                                <div className="er-doc-kv-cell"><span className="er-doc-lbl">Critical Material Flag</span><p className="text-critical font-semibold">Limestone</p></div>
                            </div>
                        </section>

                        {/* Comprehensive Financial Cost Estimation Variables */}
                        <section className="er-doc-content-section">
                            <h3 className="er-doc-section-title-heading">VII. Financial Impact & Sourcing Cost Analysis</h3>
                            <div className="er-doc-key-value-grid columns-4">
                                <div className="er-doc-kv-cell"><span className="er-doc-lbl">Estimated Baseline Loss</span><p className="font-mono">$42,500</p></div>
                                <div className="er-doc-kv-cell"><span className="er-doc-lbl">Recovery Cycle Cost</span><p className="font-mono">$8,400</p></div>
                                <div className="er-doc-kv-cell"><span className="er-doc-lbl">Mitigation Structural Cost</span><p className="font-mono">$4,820</p></div>
                                <div className="er-doc-kv-cell"><span className="er-doc-lbl">Net Saved Value Matrix</span><p className="text-success font-semibold font-mono">+$29,280</p></div>
                            </div>
                        </section>

                        {/* Network Latency and Expected Delay Realizations */}
                        <section className="er-doc-content-section">
                            <h3 className="er-doc-section-title-heading">VIII. Network Delay & Logistics Latency Profiling</h3>
                            <div className="er-doc-key-value-grid columns-3">
                                <div className="er-doc-kv-cell"><span className="er-doc-lbl">Expected Transit Latency</span><p className="font-mono">+45 mins cycle</p></div>
                                <div className="er-doc-kv-cell"><span className="er-doc-lbl">Recovery Window Time</span><p className="font-mono">4.5 Hours Post-Drain</p></div>
                                <div className="er-doc-kv-cell"><span className="er-doc-lbl">Affected Fleet Deliveries</span><p className="font-semibold text-brand">2 Freight Vectors</p></div>
                            </div>
                        </section>

                        {/* Prescribed Strategic Multi-Agent Mitigation Execution Roadmap */}
                        <section className="er-doc-content-section">
                            <h3 className="er-doc-section-title-heading">IX. Autonomous Sourcing Mitigation Plan</h3>
                            <div className="er-doc-mitigation-bullet-stack">
                                <div className="er-doc-bullet-item">
                                    <strong>Immediate Strategic Action Directive:</strong> Deploy real-time route rerouting sequence parameters to inbound clinker freight vehicles before local junction saturation checkpoints.
                                </div>
                                <div className="er-doc-bullet-item">
                                    <strong>Inter-Modal Inventory Transfer Protocol:</strong> Relocate 1,200 T Limestone bulk cargo reserves from the Plant C Southern Terminal surplus using active secondary rail loop allocations.
                                </div>
                                <div className="er-doc-bullet-item">
                                    <strong>Alternative Routing Protocol:</strong> Activate the immediate out-of-band bypass loop via the NH-48 peripheral logistics link to bypass broken infrastructure vectors.
                                </div>
                                <div className="er-doc-bullet-item">
                                    <strong>Backup Sourcing Activation:</strong> Execute emergency standby contract terms with secondary Rajasthan Quarry nodes to bridge raw mill requirements.
                                </div>
                                <div className="er-doc-bullet-item er-highlight-box">
                                    <strong>Autonomous Agent Recommendation:</strong> Authorize inter-modal rail transfer immediately. Sourcing cost metrics confirm this as the optimal matrix solution to avoid structural clinker drawdown stop conditions while containing spot premium costs.
                                </div>
                            </div>
                        </section>

                        {/* Document Validation Footer Stamp Area */}
                        <footer className="er-doc-footer-signature-area">
                            <div className="er-doc-footer-row">
                                <span className="er-signature-lbl">Orchestration Pool Authorization:</span>
                                <span className="er-signature-val font-semibold">{mockReportMeta.generatedBy}</span>
                            </div>
                            <div className="er-doc-footer-row split">
                                <div><span className="er-signature-lbl">Generation Datetime:</span> <span className="font-mono er-signature-val">{mockReportMeta.creationTime}</span></div>
                                <div><span className="er-signature-lbl">Autonomous Confidence:</span> <span className="font-mono text-success er-signature-val">{mockReportMeta.confidence}</span></div>
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
                            <div className="er-property-row"><span>Report ID Identification</span><strong className="font-mono text-brand">{mockReportMeta.id}</strong></div>
                            <div className="er-property-row"><span>System Generation Core</span><span className="er-txt-truncate">{mockReportMeta.generatedBy}</span></div>
                            <div className="er-property-row"><span>Creation Compiled Time</span><span className="font-mono">{mockReportMeta.creationTime}</span></div>
                            <div className="er-property-row"><span>Report Build Version</span><span className="font-mono">{mockReportMeta.version}</span></div>
                            <div className="er-property-row"><span>AI Model Confidence</span><strong className="font-mono text-success">{mockReportMeta.confidence}</strong></div>
                            <div className="er-property-row"><span>Board Approval Status</span><span className="er-badge-status status-success">{mockReportMeta.status}</span></div>
                            <div className="er-property-row"><span>Enterprise Disruption Rank</span><span className="er-badge-status status-critical">{mockReportMeta.priority}</span></div>
                            <div className="er-property-row"><span>Estimated Reading Time</span><span>{mockReportMeta.readingTime}</span></div>
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
                            <button className="er-btn-action-trigger primary-brand">
                                <FileDown size={14} /> <span>Export Board PDF</span>
                            </button>
                            <button className="er-btn-action-trigger secondary-outline">
                                <FileText size={14} /> <span>Export Markdown</span>
                            </button>
                            <button className="er-btn-action-trigger secondary-outline">
                                <RefreshCw size={14} /> <span>Regenerate Analysis</span>
                            </button>
                            <button className="er-btn-action-trigger secondary-outline">
                                <Share2 size={14} /> <span>Share Report Pipeline</span>
                            </button>
                        </div>
                    </div>

                    {/* Multi-Agent Sequential Timeline Activity Trail */}
                    <div className="er-sidebar-widget-card">
                        <h3 className="er-widget-card-title">Recent Report Ingestion Activity</h3>
                        <div className="er-sequential-timeline-track">
                            {timelineActivity.map((activity) => (
                                <div key={activity.id} className="er-timeline-activity-node-row">
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
                            {reportHistory.map((row) => (
                                <tr key={row.id} className={row.id === selectedReportId ? 'er-row-state-active-selected' : ''}>
                                    <td className="font-semibold text-brand font-mono">{row.id}</td>
                                    <td className="font-mono text-secondary">{row.date}</td>
                                    <td className="er-table-incident-cell-truncate" title={row.incident}>{row.incident}</td>
                                    <td>
                                        <span className={`er-table-tag-badge severity-${row.severity.toLowerCase()}`}>
                                            {row.severity}
                                        </span>
                                    </td>
                                    <td>
                                        <span className="er-table-status-cell-flex">
                                            <span className={`er-table-status-dot state-${row.status.toLowerCase()}`}></span>
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
                                            <button className="er-table-btn-icon-link" title="Download Payload Bundle">
                                                <Download size={13} />
                                            </button>
                                            <button className="er-table-btn-icon-link" title="Duplicate Constraints Structure">
                                                <Copy size={13} />
                                            </button>
                                            <button className="er-table-btn-icon-link" title="Share Enterprise Vector">
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