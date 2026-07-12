import React from 'react';
import '../styles/settings.css';

const Settings = () => {
    return (
        <div className="fade-in">
            <div className="page-header">
                <h1 className="page-title">Settings</h1>
                <p className="page-description">Manage systemic parameters, notification bounds, agent controls, and user profiles.</p>
            </div>

            <div className="grid-2">
                <div className="panel-card">
                    <h3>User Profile Administration</h3>
                    <div className="settings-form-group" style={{ marginTop: '12px' }}>
                        <label>Full Operational Name</label>
                        <input type="text" defaultValue="Enterprise Admin Operator" readOnly />
                    </div>
                    <div className="settings-form-group">
                        <label>Security Clearance Email</label>
                        <input type="email" defaultValue="admin.supplychain@enterprise.internal" readOnly />
                    </div>
                    <div className="settings-form-group">
                        <label>Assigned Command Node</label>
                        <input type="text" defaultValue="Central HQ - Control Station Room 4" readOnly />
                    </div>
                    <button className="settings-save-btn">Update Profile Options</button>
                </div>

                <div className="panel-card">
                    <h3>Intelligence Engine Configuration</h3>
                    <div className="settings-form-group" style={{ marginTop: '12px' }}>
                        <label>AI Alert Sensitivity Threshold</label>
                        <select defaultValue="balanced">
                            <option value="high">High Sensitivity (Early Flags)</option>
                            <option value="balanced">Balanced Matrix (Recommended)</option>
                            <option value="low">Low Variance Suppression</option>
                        </select>
                    </div>
                    <div className="settings-form-group">
                        <label>Data Ingestion Sync Cadence</label>
                        <select defaultValue="15">
                            <option value="5">Realtime Streaming (5m chunks)</option>
                            <option value="15">Standard Interval (15m chunks)</option>
                            <option value="60">Hourly Consolidated Buffers</option>
                        </select>
                    </div>
                    <div className="settings-form-group">
                        <label>Interface System Theme Canvas</label>
                        <input type="text" defaultValue="Enterprise Premium Slate (Fixed Variable Configuration)" readOnly />
                    </div>
                </div>
            </div>
        </div>
    );
};

export default Settings;