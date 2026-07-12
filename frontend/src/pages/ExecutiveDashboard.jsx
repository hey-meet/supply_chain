import React from 'react';
import '../styles/executive-dashboard.css';

const ExecutiveDashboard = () => {
    return (
        <div className="fade-in">
            <div className="page-header">
                <h1 className="page-title">Executive Dashboard</h1>
                <p className="page-description">High-level enterprise overview of global supply operations and system state.</p>
            </div>

            <div className="grid-4">
                <div className="summary-card">
                    <span className="label">Global Network Risk</span>
                    <span className="value">Minimal</span>
                    <span className="status" style={{ color: 'var(--status-success)' }}>Stable Operational Index</span>
                </div>
                <div className="summary-card">
                    <span className="label">Active Transits</span>
                    <span className="value">1,240</span>
                    <span className="status" style={{ color: 'var(--brand-primary)' }}>Across 14 lanes</span>
                </div>
                <div className="summary-card">
                    <span className="label">Pending Alerts</span>
                    <span className="value">3</span>
                    <span className="status" style={{ color: 'var(--status-warning)' }}>Requires operational review</span>
                </div>
                <div className="summary-card">
                    <span className="label">AI Recommendations</span>
                    <span className="value">98%</span>
                    <span className="status" style={{ color: 'var(--status-success)' }}>Model confidence score</span>
                </div>
            </div>

            <div className="grid-2">
                <div className="panel-card">
                    <h3>Recent System Activity</h3>
                    <div className="activity-list">
                        <div className="activity-item">
                            <span>Route optimization calculated for EMEA Node 4</span>
                            <span className="activity-time">10m ago</span>
                        </div>
                        <div className="activity-item">
                            <span>Weather warning processed for North Sea transit</span>
                            <span className="activity-time">45m ago</span>
                        </div>
                        <div className="activity-item">
                            <span>Inventory thresholds updated for Plant Austin</span>
                            <span className="activity-time">2h ago</span>
                        </div>
                    </div>
                </div>

                <div className="panel-card">
                    <h3>Risk Overview Matrix</h3>
                    <div className="risk-indicator critical">
                        <strong>Critical:</strong> Port Congestion detected at Terminal West (Delay estimate +48h).
                    </div>
                    <div className="risk-indicator warning">
                        <strong>Warning:</strong> Raw material allocation variant high in APAC Sector.
                    </div>
                    <div className="risk-indicator success">
                        <strong>Nominal:</strong> Domestic transport pipelines performing at optimal margins.
                    </div>
                </div>
            </div>

            <div className="grid-1">
                <div className="panel-card">
                    <h3>System Status Architecture</h3>
                    <p style={{ color: 'var(--text-secondary)' }}>All data collection agents operating normally. No pipeline latency detected.</p>
                </div>
            </div>
        </div>
    );
};

export default ExecutiveDashboard;