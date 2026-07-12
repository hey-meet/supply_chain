import React from 'react';
import '../styles/news-intelligence.css';

const NewsIntelligence = () => {
    return (
        <div className="fade-in">
            <div className="page-header">
                <h1 className="page-title">News Intelligence</h1>
                <p className="page-description">AI-scanned global feed monitoring industry events impacting components and logistics.</p>
            </div>

            <div className="search-bar-container">
                <input type="text" placeholder="Filter downstream news, geopolitical alerts, or tariff tracking..." className="wide-search" />
            </div>

            <div className="grid-3">
                <div className="panel-card">
                    <h3>AI Core News Summary</h3>
                    <div className="ai-summary-box">
                        "Global logistics operations see minor localized restrictions within the maritime corridor due to changing weather dynamics. No structural adjustments required for inventory holdings over the 7-day operational horizon."
                    </div>
                </div>
                <div className="panel-card">
                    <h3>Risk Classification Tiers</h3>
                    <p style={{ marginBottom: '8px' }}>Macro Market Indicators:</p>
                    <ul>
                        <li>Geopolitical Risk Index: <strong>Low</strong></li>
                        <li>Energy Price Impact Variance: <strong>Moderate</strong></li>
                        <li>Labor Framework Adjustments: <strong>Minimal</strong></li>
                    </ul>
                </div>
                <div className="panel-card">
                    <h3>Monitored Keywords</h3>
                    <div style={{ display: 'flex', gap: '8px', flexWrap: 'wrap', marginTop: '8px' }}>
                        <span className="badge" style={{ backgroundColor: 'var(--brand-primary)' }}>Semiconductors</span>
                        <span className="badge" style={{ backgroundColor: 'var(--brand-primary)' }}>Freight Costs</span>
                        <span className="badge" style={{ backgroundColor: 'var(--brand-primary)' }}>Border Crossings</span>
                    </div>
                </div>
            </div>

            <div className="panel-card">
                <h3>Latest Monitored Headlines</h3>
                <div className="headline-item">
                    <div className="headline-meta">
                        <span>Source: Global Logistics Hub</span>
                        <span>•</span>
                        <span>1 hour ago</span>
                        <span className="badge success">Informational</span>
                    </div>
                    <h4>Central Distribution Centers Complete Infrastructure Upgrades</h4>
                    <p style={{ color: 'var(--text-secondary)', fontSize: '0.9rem', marginTop: '4px' }}>Processing capacity expanded by fifteen percent across major sorting platforms.</p>
                </div>
                <div className="headline-item">
                    <div className="headline-meta">
                        <span>Source: Maritime Journal</span>
                        <span>•</span>
                        <span>3 hours ago</span>
                        <span className="badge warning">Watchlist</span>
                    </div>
                    <h4>Slight Container Availability Reductions Tracked In Major Eastern Ports</h4>
                    <p style={{ color: 'var(--text-secondary)', fontSize: '0.9rem', marginTop: '4px' }}>Equilibrium adjustments likely over standard multi-week reporting intervals.</p>
                </div>
            </div>
        </div>
    );
};

export default NewsIntelligence;