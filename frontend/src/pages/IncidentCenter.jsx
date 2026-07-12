import React from 'react';
import '../styles/incident-center.css';

const IncidentCenter = () => {
    return (
        <div className="fade-in">
            <div className="page-header">
                <h1 className="page-title">Incident Center</h1>
                <p className="page-description">Real-time resolution desk tracking logistical blockages, shortages, or asset disruptions.</p>
            </div>

            <div className="grid-3">
                <div className="panel-card">
                    <h3>Active Incident Volumetrics</h3>
                    <div style={{ fontSize: '2.5rem', fontWeight: 'bold', color: 'var(--status-critical)' }}>1</div>
                    <p style={{ color: 'var(--text-secondary)', fontSize: '0.9rem' }}>Critical issue requiring escalation routing</p>
                </div>
                <div className="panel-card">
                    <h3>Mitigated Incidents</h3>
                    <div style={{ fontSize: '2.5rem', fontWeight: 'bold', color: 'var(--status-success)' }}>42</div>
                    <p style={{ color: 'var(--text-secondary)', fontSize: '0.9rem' }}>Successfully rerouted within standard SLAs</p>
                </div>
                <div className="panel-card">
                    <h3>Mean Resolution Time</h3>
                    <div style={{ fontSize: '2.5rem', fontWeight: 'bold', color: 'var(--brand-primary)' }}>1.4h</div>
                    <p style={{ color: 'var(--text-secondary)', fontSize: '0.9rem' }}>System-assisted automation performance</p>
                </div>
            </div>

            <div className="grid-2">
                <div>
                    <h3>Active Incidents Registry</h3>
                    <div className="incident-card" style={{ borderLeft: '5px solid var(--status-critical)' }}>
                        <div className="incident-header">
                            <h4>INC-2026-881: Raw Material Bottleneck</h4>
                            <span className="badge critical">Critical</span>
                        </div>
                        <p>Component block matching standard lead matrices failed at entry checkpoint.</p>
                        <div className="incident-details">
                            <span>Location Context: Global Portal Hub Alpha</span>
                            <br />
                            <span>Timestamp: 12-Jul-2026 14:15 UTC</span>
                        </div>
                    </div>

                    <div className="incident-card" style={{ borderLeft: '5px solid var(--status-warning)' }}>
                        <div className="incident-header">
                            <h4>INC-2026-879: Custom Clearance Delay</h4>
                            <span className="badge warning">Warning</span>
                        </div>
                        <p>Regulatory paper variant matches require technical signature confirmation.</p>
                        <div className="incident-details">
                            <span>Location Context: Border Station Zone D</span>
                            <br />
                            <span>Timestamp: 12-Jul-2026 09:30 UTC</span>
                        </div>
                    </div>
                </div>

                <div className="panel-card">
                    <h3>Incident Remediation Timeline</h3>
                    <div className="timeline-placeholder">
                        <div className="timeline-node">
                            <strong>14:15 UTC</strong> - Incident identified via automated threshold monitoring.
                        </div>
                        <div className="timeline-node">
                            <strong>14:20 UTC</strong> - AI Model generated secondary shipping lane options.
                        </div>
                        <div className="timeline-node">
                            <strong>14:35 UTC</strong> - Operations supervisor notified via intelligence alerts.
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default IncidentCenter;