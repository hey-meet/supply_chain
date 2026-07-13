import React from 'react';
import '../styles/executive-reports.css';

const ExecutiveReports = () => {
    return (
        <div className="fade-in">
            <div className="page-header">
                <h1 className="page-title">Executive Reports</h1>
                <p className="page-description">Auditable regulatory reporting configurations, historical records, and compiled operations logs.</p>
            </div>

            <div className="grid-3">
                <div className="panel-card">
                    <h3>Standard Report Generators</h3>
                    <p style={{ fontSize: '0.85rem', color: 'var(--text-secondary)', marginBottom: '12px' }}>
                        Select standard configuration profiles to construct analytical outputs for distribution frameworks.
                    </p>
                    <button className="action-btn" style={{ marginTop: 0, width: '100%' }}>Configure Filter Variables</button>
                </div>
                <div className="panel-card">
                    <h3>Scheduled Exports</h3>
                    <p style={{ fontSize: '0.9rem' }}>• Monthly Operations Audit (Every 1st)</p>
                    <p style={{ fontSize: '0.9rem' }}>• Weekly Network Volatility Review (Fridays)</p>
                    <p style={{ fontSize: '0.9rem' }}>• Daily Inventory Snapshot (00:00 UTC)</p>
                </div>
                <div className="panel-card">
                    <h3>Compliance Filing Metrics</h3>
                    <p style={{ fontSize: '0.85rem', color: 'var(--text-secondary)' }}>
                        System generates fully traceable chain-of-custody data files corresponding perfectly to global cross-border reporting laws.
                    </p>
                </div>
            </div>

            <div className="panel-card">
                <h3>Available Archives & Documents</h3>

                <div className="report-row">
                    <div>
                        <strong>Supply_Chain_Risk_Assessment_Q2_2026.pdf</strong>
                        <div style={{ fontSize: '0.8rem', color: 'var(--text-secondary)' }}>Compiled by AI Analytics Node • 4.2 MB • 01-Jul-2026</div>
                    </div>
                    <span className="download-link">Download Document</span>
                </div>

                <div className="report-row">
                    <div>
                        <strong>Material_Allocation_Ledger_June_2026.csv</strong>
                        <div style={{ fontSize: '0.8rem', color: 'var(--text-secondary)' }}>System Generated Dump • 18.5 MB • 30-Jun-2026</div>
                    </div>
                    <span className="download-link">Download Document</span>
                </div>

                <div className="report-row">
                    <div>
                        <strong>Carbon_Compliance_and_Sustainability_Index_2026.pdf</strong>
                        <div style={{ fontSize: '0.8rem', color: 'var(--text-secondary)' }}>Calculated Scope 1-3 Model Run • 1.8 MB • 15-May-2026</div>
                    </div>
                    <span className="download-link">Download Document</span>
                </div>
            </div>
        </div>
    );
};

export default ExecutiveReports;