import React from 'react';
import '../styles/ai-decision-center.css';

const AIDecisionCenter = () => {
    return (
        <div className="fade-in">
            <div className="page-header">
                <h1 className="page-title">AI Decision Center</h1>
                <p className="page-description">Prescriptive execution proposals, asset risk prediction modeling, and systemic suggestions.</p>
            </div>

            <div className="grid-2">
                <div className="panel-card ai-recommendation-card">
                    <span className="badge warning" style={{ marginBottom: '8px' }}>High Value Strategy Suggestion</span>
                    <h3>Reallocate Contingency Stock - Semiconductor Modules</h3>
                    <p style={{ fontSize: '0.9rem', color: 'var(--text-secondary)' }}>
                        Model output shows localized inventory drawdowns in central depots. Proactive allocation adjustment shifts safety inventory from Node 8 to Node 2 to preserve balance matrix.
                    </p>
                    <button className="action-btn">Accept Recommendation</button>
                </div>

                <div className="panel-card ai-recommendation-card">
                    <span className="badge success" style={{ marginBottom: '8px' }}>Transit Optimization Plan</span>
                    <h3>Consolidate Inbound Ocean Freight Lanes</h3>
                    <p style={{ fontSize: '0.9rem', color: 'var(--text-secondary)' }}>
                        Consolidating secondary supplier shipments into single heavy vessels reduces greenhouse profile variables and cuts pipeline fee configurations by roughly four percent.
                    </p>
                    <button className="action-btn">Accept Recommendation</button>
                </div>
            </div>

            <div className="grid-3">
                <div className="panel-card">
                    <h3>Risk Horizons Predictive Model</h3>
                    <p style={{ fontSize: '0.9rem', marginBottom: '8px' }}>Predictive metrics accuracy tracking targets:</p>
                    <ul>
                        <li>Demand Forecast Accuracy: <strong>94.2%</strong></li>
                        <li>Lead Time Precision: <strong>91.0%</strong></li>
                        <li>Supplier Failure Index: <strong>0.02%</strong></li>
                    </ul>
                </div>
                <div className="panel-card">
                    <h3>Model Health & Vector Status</h3>
                    <div className="model-metric"><span>Engine Version</span><strong>v4.2.1-prod</strong></div>
                    <div className="model-metric"><span>Last Weights Refresh</span><strong>04:00 AM Today</strong></div>
                    <div className="model-metric"><span>Inference Latency</span><strong>14ms</strong></div>
                </div>
                <div className="panel-card">
                    <h3>Agentic Controls Config</h3>
                    <p style={{ fontSize: '0.85rem', color: 'var(--text-secondary)' }}>
                        Operational thresholds are configured inside manual human-in-the-loop validation configurations. Automatic fallback pipelines remain active.
                    </p>
                </div>
            </div>
        </div>
    );
};

export default AIDecisionCenter;