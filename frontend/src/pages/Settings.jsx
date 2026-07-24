// Settings.jsx
import React, { useState, useEffect } from 'react';
import {
    CheckCircle2, Sliders, Database, Network, Bell, Globe, Terminal,
    Download, Upload, Save, AlertTriangle, Activity, Settings as SettingsIcon
} from 'lucide-react';
import '../styles/settings.css';
import { getSettingsData, saveSettingsData } from '../services/settingsService';

// --- ENTERPRISE MOCK REGISTRY STACKS ---
const kpiData = [
    { id: 1, title: 'AI Services Online', value: '8 / 8 Node', status: 'success', desc: 'All clusters nominal' },
    { id: 2, title: 'Connected APIs', value: '14 Active', status: 'success', desc: 'Zero data pipe latencies' },
    { id: 3, title: 'Active Config Profiles', value: '3 Active', status: 'brand', desc: 'Orchestrator v3.4.1 deployment' },
    { id: 4, title: 'System Health Status', value: '99.98%', status: 'success', desc: 'High-availability baseline' }
];

const networkConfig = [
    { id: 'c1', label: 'Manufacturing Plants Matrix', status: 'Healthy', sync: '2 mins ago', health: 'success' },
    { id: 'c2', label: 'Global Sourcing Suppliers', status: 'Healthy', sync: '5 mins ago', health: 'success' },
    { id: 'c3', label: 'Regional Clinker Warehouses', status: 'Healthy', sync: '1 min ago', health: 'success' },
    { id: 'c4', label: 'Freight Inter-Modal Routes', status: 'Attention', sync: '12 mins ago', health: 'warning' },
    { id: 'c5', label: 'Distribution Centers Base', status: 'Healthy', sync: '4 mins ago', health: 'success' }
];

const dataConfig = [
    { id: 'd1', label: 'Database Core Status', storage: '1.4 TB / 4 TB', sync: 'Synced', health: 'success' },
    { id: 'd2', label: 'Knowledge Graph Clusters', storage: '428k Entities', sync: 'Re-indexed', health: 'success' },
    { id: 'd3', label: 'Real-time News Cache', storage: '12.4 GB', sync: 'Streaming', health: 'success' }
];

const healthMetrics = [
    { id: 'h1', name: 'AI Sourcing Model Cluster', health: 'Healthy', latency: '42ms', check: 'Just now', status: 'success' },
    { id: 'h2', name: 'Knowledge Graph Router', health: 'Healthy', latency: '12ms', check: '1 min ago', status: 'success' },
    { id: 'h3', name: 'News Ingestion Pipeline', health: 'Healthy', latency: '110ms', check: 'Just now', status: 'success' }
];

export default function Settings() {
    // Gearbox Management State: 'stable' | 'unsaved' | 'saving' | 'updated' | 'restoring'
    const [engineState, setEngineState] = useState('stable');
    const [lastApplied, setLastApplied] = useState('10:42:18');

    // Configuration Parameter States
    const [aiModel, setAiModel] = useState('gpt-4o-cement-v3');
    const [temperature, setTemperature] = useState(0.15);
    const [confidence, setConfidence] = useState(0.85);
    const [maxTokens, setMaxTokens] = useState(8192);
    const [timeout, setTimeoutVal] = useState(30);
    const [reasoningMode, setReasoningMode] = useState('deep-graph-fallback');
    const [apiKey, setApiKey] = useState('tvly-••••••••••••••••••••A9');
    const [refreshInterval, setRefreshInterval] = useState(5);
    const [alertsEnabled, setAlertsEnabled] = useState(true);

    useEffect(() => {
        const loadSettings = async () => {
            try {
                const response = await getSettingsData();
                if (response && response.success && response.data) {
                    const config = response.data;
                    setAiModel(config.aiModel || 'gpt-4o-cement-v3');
                    setTemperature(config.temperature ?? 0.15);
                    setConfidence(config.confidence ?? 0.85);
                    setMaxTokens(config.maxTokens ?? 8192);
                    setTimeoutVal(config.timeout ?? 30);
                    setReasoningMode(config.reasoningMode || 'deep-graph-fallback');
                    setApiKey(config.apiKey || 'tvly-••••••••••••••••••••A9');
                    setRefreshInterval(config.refreshInterval ?? 5);
                    setAlertsEnabled(config.alertsEnabled ?? true);
                    setEngineState('stable');
                }
            } catch (error) {
                console.error("Failed to load settings from server:", error);
            }
        };
        loadSettings();
    }, []);

    const triggerFieldMutation = (setter, value) => {
        setter(value);
        if (engineState !== 'saving' && engineState !== 'restoring') {
            setEngineState('unsaved');
        }
    };

    const handleSaveChanges = async (e) => {
        e.preventDefault();
        if (engineState === 'stable' || engineState === 'saving' || engineState === 'restoring') return;

        setEngineState('saving');
        try {
            const payload = {
                aiModel,
                temperature,
                confidence,
                maxTokens,
                timeout,
                reasoningMode,
                apiKey,
                refreshInterval,
                alertsEnabled
            };
            const response = await saveSettingsData(payload);
            if (response && response.success) {
                const now = new Date();
                setLastApplied(now.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', second: '2-digit', hour12: false }));
                setEngineState('updated');

                setTimeout(() => {
                    setEngineState('stable');
                }, 3000);
            } else {
                setEngineState('unsaved');
                alert("Failed to save configuration parameters: " + (response?.message || "unknown error"));
            }
        } catch (err) {
            console.error("Failed to save settings:", err);
            setEngineState('unsaved');
            alert("API endpoint encountered an error while saving settings.");
        }
    };

    const handleResetDefaults = () => {
        setEngineState('restoring');
        setTimeout(() => {
            setAiModel('gpt-4o-cement-v3');
            setTemperature(0.15);
            setConfidence(0.85);
            setMaxTokens(8192);
            setTimeoutVal(30);
            setReasoningMode('deep-graph-fallback');
            setApiKey('tvly-••••••••••••••••••••A9');
            setRefreshInterval(5);
            setAlertsEnabled(true);
            setEngineState('unsaved');
        }, 1500);
    };

    const handleDiscard = async () => {
        setEngineState('restoring');
        try {
            const response = await getSettingsData();
            if (response && response.success && response.data) {
                const config = response.data;
                setAiModel(config.aiModel || 'gpt-4o-cement-v3');
                setTemperature(config.temperature ?? 0.15);
                setConfidence(config.confidence ?? 0.85);
                setMaxTokens(config.maxTokens ?? 8192);
                setTimeoutVal(config.timeout ?? 30);
                setReasoningMode(config.reasoningMode || 'deep-graph-fallback');
                setApiKey(config.apiKey || 'tvly-••••••••••••••••••••A9');
                setRefreshInterval(config.refreshInterval ?? 5);
                setAlertsEnabled(config.alertsEnabled ?? true);
            }
        } catch (e) {
            console.error("Failed to reload previous settings:", e);
        } finally {
            setEngineState('stable');
        }
    };

    // Calculate dynamic status strings for mechanical monitoring panel
    const getStatusLabel = () => {
        switch (engineState) {
            case 'unsaved': return 'Applying Configuration';
            case 'saving': return 'Saving Configuration';
            case 'updated': return 'Configuration Updated Successfully';
            case 'restoring': return 'Restoring Default Configuration...';
            default: return 'System Stable';
        }
    };

    return (
        <div className="sc-content-scope">

            {/* Top Workspace Page Header */}
            <header className="sc-header-block">
                <div className="sc-header-left">
                    <h1 className="sc-page-title">System Configuration</h1>
                    <p className="sc-page-subtitle">Configure AI models, enterprise settings and supply chain preferences.</p>
                </div>

                {/* Synchronized Mechanical Gearbox Widget */}
                <div className="sc-header-right">
                    <div className={`sc-gearbox-widget-assembly engine-${engineState}`}>

                        <div className="sc-gearbox-mechanical-cluster">
                            <div className="sc-gearbox-glow-ring"></div>

                            {/* Rotating Status LEDs surrounding assembly */}
                            <div className="sc-gearbox-led-ring">
                                <span className="sc-gearbox-led-node"></span>
                                <span className="sc-gearbox-led-node"></span>
                                <span className="sc-gearbox-led-node"></span>
                            </div>

                            {/* 1. Large Center Gear (AI Engine) */}
                            <div className="sc-gear-component gear-large-center">
                                <svg viewBox="0 0 100 100" className="sc-gear-svg">
                                    <circle cx="50" cy="50" r="32" className="sc-gear-body" />
                                    {[...Array(12)].map((_, i) => (
                                        <path key={i} d="M46 2 L54 2 L56 16 L44 16 Z" transform={`rotate(${i * 30} 50 50)`} className="sc-gear-tooth" />
                                    ))}
                                    <circle cx="50" cy="50" r="16" className="sc-gear-center-bore" />
                                </svg>
                                {engineState === 'updated' ? (
                                    <CheckCircle2 size={14} className="sc-gearbox-success-checkmark" />
                                ) : (
                                    <span className="sc-gearbox-ai-core-indicator"></span>
                                )}
                            </div>

                            {/* 2. Medium Gear (Data Pipeline) */}
                            <div className="sc-gear-component gear-medium-left">
                                <svg viewBox="0 0 70 70" className="sc-gear-svg">
                                    <circle cx="35" cy="35" r="22" className="sc-gear-body" />
                                    {[...Array(8)].map((_, i) => (
                                        <path key={i} d="M32 2 L38 2 L39 12 L31 12 Z" transform={`rotate(${i * 45} 35 35)`} className="sc-gear-tooth" />
                                    ))}
                                    <circle cx="35" cy="35" r="8" className="sc-gear-center-bore" />
                                </svg>
                            </div>

                            {/* 3. Small Gear (System Configuration) */}
                            <div className="sc-gear-component gear-small-right">
                                <svg viewBox="0 0 50 50" className="sc-gear-svg">
                                    <circle cx="25" cy="25" r="14" className="sc-gear-body" />
                                    {[...Array(6)].map((_, i) => (
                                        <path key={i} d="M22 1 L28 1 L29 8 L21 8 Z" transform={`rotate(${i * 60} 25 25)`} className="sc-gear-tooth" />
                                    ))}
                                    <circle cx="25" cy="25" r="5" className="sc-gear-center-bore" />
                                </svg>
                            </div>
                        </div>

                        {/* Status Label Interface Panel */}
                        <div className="sc-gearbox-text-panel">
                            <span className="sc-gearbox-status-lbl">Orchestration Transmission</span>
                            <div className="sc-gearbox-status-flex-row">
                                <strong className="sc-gearbox-status-value">{getStatusLabel()}</strong>
                                {engineState === 'saving' && <span className="sc-gearbox-progress-bar-ticker"></span>}
                            </div>
                            <span className="sc-gearbox-timestamp-tracker font-mono">Last Applied: {lastApplied}</span>
                        </div>
                    </div>
                </div>
            </header>

            {/* Top Operational Status Cards */}
            <section className="sc-kpi-grid">
                {kpiData.map((kpi) => (
                    <div key={kpi.id} className="sc-kpi-card">
                        <span className="sc-kpi-lbl">{kpi.title}</span>
                        <div className="sc-kpi-value-row">
                            <h3 className="sc-kpi-val-text">{kpi.value}</h3>
                            <span className={`sc-indicator-dot dot-${kpi.status}`}></span>
                        </div>
                        <p className="sc-kpi-desc-text">{kpi.desc}</p>
                    </div>
                ))}
            </section>

            {/* Configuration Split Panels Content Workspace */}
            <div className="sc-workspace-layout-grid">

                {/* Left Form Workspace Controls Stack */}
                <div className="sc-panel-column">

                    {/* SECTION: AI Configuration Card */}
                    <div className={`sc-configuration-card ${engineState === 'unsaved' ? 'section-mutated-highlight' : ''}`}>
                        <div className="sc-card-header-flex">
                            <div className="sc-card-title-block">
                                <Sliders size={16} className="color-brand" />
                                <h3 className="sc-card-heading">AI Core Engine Configuration</h3>
                            </div>
                            <span className="sc-health-badge healthy">Healthy Matrix</span>
                        </div>

                        <div className="sc-form-elements-vertical-stack">
                            <div className="sc-form-row-item">
                                <label className="sc-field-lbl">Target Foundation Large Language Model</label>
                                <select
                                    className="sc-select-element"
                                    value={aiModel}
                                    onChange={(e) => triggerFieldMutation(setAiModel, e.target.value)}
                                >
                                    <option value="gpt-4o-cement-v3">GPT-4o Supply Chain Specialization (v3.4)</option>
                                    <option value="claude-3-5-sonnet-enterprise">Claude 3.5 Sonnet Enterprise Matrix</option>
                                </select>
                            </div>

                            <div className="sc-form-row-double-columns">
                                <div className="sc-form-row-item">
                                    <div className="sc-slider-labels-flex">
                                        <label className="sc-field-lbl">Model Temperature Parameters</label>
                                        <span className="sc-slider-numerical-value font-mono">{temperature}</span>
                                    </div>
                                    <input
                                        type="range" min="0" max="1" step="0.05" className="sc-slider-element"
                                        value={temperature}
                                        onChange={(e) => triggerFieldMutation(setTemperature, parseFloat(e.target.value))}
                                    />
                                </div>
                                <div className="sc-form-row-item">
                                    <div className="sc-slider-labels-flex">
                                        <label className="sc-field-lbl">Mitigation Confidence Threshold</label>
                                        <span className="sc-slider-numerical-value font-mono">{Math.round(confidence * 100)}%</span>
                                    </div>
                                    <input
                                        type="range" min="0.5" max="0.99" step="0.01" className="sc-slider-element"
                                        value={confidence}
                                        onChange={(e) => triggerFieldMutation(setConfidence, parseFloat(e.target.value))}
                                    />
                                </div>
                            </div>

                            <div className="sc-form-row-double-columns">
                                <div className="sc-form-row-item">
                                    <label className="sc-field-lbl">Maximum Token Allocation Size</label>
                                    <input
                                        type="number" className="sc-input-element font-mono"
                                        value={maxTokens}
                                        onChange={(e) => triggerFieldMutation(setMaxTokens, parseInt(e.target.value))}
                                    />
                                </div>
                                <div className="sc-form-row-item">
                                    <label className="sc-field-lbl">Response Loop Timeout Threshold (s)</label>
                                    <input
                                        type="number" className="sc-input-element font-mono"
                                        value={timeout}
                                        onChange={(e) => triggerFieldMutation(setTimeoutVal, parseInt(e.target.value))}
                                    />
                                </div>
                            </div>

                            <div className="sc-form-row-item">
                                <label className="sc-field-lbl">Multi-Agent Strategic Reasoning Mode</label>
                                <select
                                    className="sc-select-element"
                                    value={reasoningMode}
                                    onChange={(e) => triggerFieldMutation(setReasoningMode, e.target.value)}
                                >
                                    <option value="deep-graph-fallback">Knowledge Graph Intersect + Multi-Agent Consensus</option>
                                    <option value="linear-speed-priority">Sub-second Latency Linear Sourcing Validation</option>
                                </select>
                            </div>
                        </div>
                    </div>

                    {/* SECTION: News Search Ingestion Card */}
                    <div className="sc-configuration-card">
                        <div className="sc-card-header-flex">
                            <div className="sc-card-title-block">
                                <Globe size={16} className="color-brand" />
                                <h3 className="sc-card-heading">News Ingestion & Search Configuration</h3>
                            </div>
                            <span className="sc-health-badge healthy">Healthy Pipe</span>
                        </div>

                        <div className="sc-form-elements-vertical-stack">
                            <div className="sc-form-row-item">
                                <label className="sc-field-lbl">Tavily Engine API Authorization Key</label>
                                <input
                                    type="text" className="sc-input-element font-mono"
                                    value={apiKey}
                                    onChange={(e) => triggerFieldMutation(setApiKey, e.target.value)}
                                />
                            </div>

                            <div className="sc-form-row-double-columns">
                                <div className="sc-form-row-item">
                                    <label className="sc-field-lbl">Pipeline Refresh Interval (Mins)</label>
                                    <input
                                        type="number" className="sc-input-element font-mono"
                                        value={refreshInterval}
                                        onChange={(e) => triggerFieldMutation(setRefreshInterval, parseInt(e.target.value))}
                                    />
                                </div>
                                <div className="sc-form-row-item">
                                    <label className="sc-field-lbl">Real-time Audio Alert Dispatcher</label>
                                    <label className="sc-toggle-switch-element">
                                        <input
                                            type="checkbox" checked={alertsEnabled}
                                            onChange={(e) => triggerFieldMutation(setAlertsEnabled, e.target.checked)}
                                        />
                                        <span className="sc-toggle-slider-nob"></span>
                                    </label>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

                {/* Right Panel Workspace Columns */}
                <div className="sc-panel-column">

                    {/* SECTION: Supply Chain Network Matrix */}
                    <div className="sc-configuration-card">
                        <div className="sc-card-header-flex">
                            <div className="sc-card-title-block">
                                <Network size={16} className="color-brand" />
                                <h3 className="sc-card-heading">Supply Chain Network Topology</h3>
                            </div>
                            <span className="sc-health-badge healthy">Nominal Arrays</span>
                        </div>

                        <div className="sc-network-topology-vertical-list">
                            {networkConfig.map((item) => (
                                <div key={item.id} className="sc-topology-list-item-row">
                                    <div className="sc-topology-left-cell">
                                        <span className={`sc-status-dot dot-${item.health}`}></span>
                                        <span className="sc-topology-node-name">{item.label}</span>
                                    </div>
                                    <div className="sc-topology-right-cell">
                                        <span className="sc-topology-status-txt font-semibold">{item.status}</span>
                                        <span className="sc-topology-sync-txt font-mono">{item.sync}</span>
                                    </div>
                                </div>
                            ))}
                        </div>
                    </div>

                    {/* SECTION: Database Storage Footprints */}
                    <div className="sc-configuration-card">
                        <div className="sc-card-header-flex">
                            <div className="sc-card-title-block">
                                <Database size={16} className="color-brand" />
                                <h3 className="sc-card-heading">Storage & Data Management Registry</h3>
                            </div>
                            <span className="sc-health-badge healthy">Active Cache</span>
                        </div>

                        <div className="sc-data-registry-vertical-table">
                            <div className="sc-registry-table-header-row">
                                <span>Core Segment</span>
                                <span>Storage Allocation</span>
                                <span className="text-right">State Cluster</span>
                            </div>
                            {dataConfig.map((item) => (
                                <div key={item.id} className="sc-registry-table-data-row">
                                    <span className="sc-reg-name font-semibold">{item.label}</span>
                                    <span className="sc-reg-storage font-mono">{item.storage}</span>
                                    <span className={`sc-reg-status text-right font-semibold text-${item.health}`}>{item.sync}</span>
                                </div>
                            ))}
                        </div>
                    </div>
                </div>
            </div>

            {/* Bottom Panel Infrastructure Node Health Matrix */}
            <section className="sc-system-health-dashboard-panel">
                <div className="sc-panel-title-wrapper-border">
                    <Activity size={16} className="color-brand" />
                    <h2 className="sc-section-title-heading">Infrastructure Component Health Relays</h2>
                </div>

                <div className="sc-health-dashboard-fluid-grid">
                    {healthMetrics.map((metric) => (
                        <div key={metric.id} className="sc-health-metric-card-node">
                            <div className="sc-health-metric-header">
                                <strong className="sc-metric-component-name font-semibold">{metric.name}</strong>
                                <span className={`sc-health-pill-tag status-${metric.status}`}>{metric.health}</span>
                            </div>
                            <div className="sc-health-metric-meta-strip">
                                <div className="sc-meta-item"><span className="sc-meta-lbl">Latency Response</span><span className="sc-meta-val font-mono font-semibold">{metric.latency}</span></div>
                                <div className="sc-meta-item text-right"><span className="sc-meta-lbl">Audit Interval</span><span className="sc-meta-val font-mono">{metric.check}</span></div>
                            </div>
                        </div>
                    ))}
                </div>
            </section>

            {/* Bottom Actions Execution Toolbar */}
            <div className="sc-bottom-fixed-actions-toolbar">
                <div className="sc-toolbar-left-side-text-panel">
                    {engineState === 'unsaved' && (
                        <p className="sc-toolbar-warning-alert font-semibold">
                            <AlertTriangle size={14} /> System variables modified. Gearbox calibration pending sync.
                        </p>
                    )}
                </div>
                <div className="sc-toolbar-buttons-flex-stack">
                    <button type="button" className="sc-btn-utility-link border-outline" onClick={handleResetDefaults}>Reset Defaults</button>
                    <button type="button" className="sc-btn-utility-link border-outline" onClick={() => alert("Action has no backend implementation. Export function is disabled.")} disabled><Download size={13} /> Export Configuration</button>
                    <button type="button" className="sc-btn-utility-link border-outline" onClick={() => alert("Action has no backend implementation. Import function is disabled.")} disabled><Upload size={13} /> Import Patch</button>

                    <button
                        type="button"
                        className="sc-btn-utility-link border-outline-secondary"
                        disabled={engineState === 'saving' || engineState === 'stable' || engineState === 'restoring'}
                        onClick={handleDiscard}
                    >
                        Discard Changes
                    </button>

                    <button
                        type="button"
                        className="sc-btn-utility-link action-primary-brand"
                        disabled={engineState === 'saving' || engineState === 'stable' || engineState === 'restoring'}
                        onClick={handleSaveChanges}
                    >
                        <Save size={14} /> <span>{engineState === 'saving' ? 'Calibrating Transmission...' : 'Save Configuration'}</span>
                    </button>
                </div>
            </div>

        </div>
    );
}