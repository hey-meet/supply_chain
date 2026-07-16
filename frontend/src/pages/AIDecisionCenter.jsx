// AIDecisionCenter.jsx
import React, { useState, useEffect } from 'react';
import {
    Cpu, ShieldAlert, Zap, Layers, RefreshCw, CheckCircle2,
    Database, Activity, TrendingUp, HelpCircle, Network,
    Terminal, ArrowRight, MessageSquare, AlertTriangle, Clock
} from 'lucide-react';
import '../styles/ai-decision-center.css';

// --- ENTERPRISE STATIC MOCK DATA ---
const kpiData = [
    { id: 1, label: 'Active AI Agents', value: '3 / 3 Nominal', desc: 'Continuous orchestration', icon: Cpu, type: 'brand' },
    { id: 2, label: 'Current Decisions', value: '1 Active Run', desc: 'Evaluating NH-48 anomaly', icon: ShieldAlert, type: 'warning' },
    { id: 3, label: 'Average Confidence', value: '94.2%', desc: 'Safe margin threshold', icon: TrendingUp, type: 'success' },
    { id: 4, label: 'Average Execution Time', value: '1.84s', desc: 'Sub-second internal loops', icon: Clock, type: 'brand' },
    { id: 5, label: 'Total Tokens Processed', value: '2.4M', desc: 'Context efficient RAG windows', icon: Database, type: 'secondary' },
    { id: 6, label: 'Successful Decisions', value: '142 Today', desc: '0% override fallback rate', icon: CheckCircle2, type: 'success' }
];

const agentsData = [
    {
        id: 'agent-1',
        name: 'News Intelligence Agent',
        avatarColor: 'blue',
        attention: 'Reasoning',
        emotion: 'Focused',
        confidence: '98%',
        execTime: '0.45s',
        tokens: '142k',
        latestDecision: 'Ingestion of validated supply chain disruption report.',
        metrics: [
            { label: 'Current Task', value: 'Parsing logistics article pipeline...' },
            { label: 'Current Thought', value: 'Cross-referencing NH-48 flooding alerts with structural routes.' },
            { label: 'Processing Queue', value: '2 incoming events pending' },
            { label: 'Collected Sources', value: 'Ministry Transport Link, Regional RSS Feed' }
        ]
    },
    {
        id: 'agent-2',
        name: 'Supply Chain Impact Agent',
        avatarColor: 'amber',
        attention: 'Thinking',
        emotion: 'Analyzing',
        confidence: '93%',
        execTime: '0.62s',
        tokens: '280k',
        latestDecision: 'Identified Limestone cargo payload variance exposure.',
        metrics: [
            { label: 'Current Task', value: 'Calculating enterprise blast radius...' },
            { label: 'Current Thought', value: 'Mapping delay curves onto Western Grinding Complex buffer.' },
            { label: 'Affected Infrastructure', value: 'Plant A (Critical), Supplier Node 4' },
            { label: 'Knowledge Graph Match', value: '14 entity nodes connected' }
        ]
    },
    {
        id: 'agent-3',
        name: 'Mitigation Planning Agent',
        avatarColor: 'green',
        attention: 'Decision Ready',
        emotion: 'Confident',
        confidence: '96%',
        execTime: '0.77s',
        tokens: '410k',
        latestDecision: 'Formulated primary rail bypass loop protocol.',
        metrics: [
            { label: 'Current Task', value: 'Evaluating cost-benefit distribution matrix...' },
            { label: 'Current Thought', value: 'Synthesizing inventory buffer from Southern Terminal terminals.' },
            { label: 'Alternative Logistics', value: 'Emergency Rajasthan Quarry Core' },
            { label: 'Inventory Transfer Plan', value: '1,200 T Limestone allocation shift' }
        ]
    }
];

const waveTransmissions = [
    { id: 1, label: 'Data Packet', from: 'News Intel', to: 'Impact Engine' },
    { id: 2, label: 'Knowledge Update', from: 'Impact Engine', to: 'Mitigation Plan' },
    { id: 3, label: 'Decision Sent', from: 'Mitigation Plan', to: 'System Pipeline' }
];

const systemMetrics = [
    { label: 'Overall Agent Health', value: '100% Operational', type: 'success' },
    { label: 'Agent Synchronization', value: '12ms delta delay', type: 'brand' },
    { label: 'Memory Allocation Pool', value: '14.2 GB / 32 GB', type: 'secondary' },
    { label: 'Average System Latency', value: '45ms structural', type: 'brand' },
    { label: 'Knowledge Graph Nodes', value: '42,850 active connections', type: 'brand' },
    { label: 'LLM Multi-Cluster Status', value: 'Nominal baseline deployment', type: 'success' }
];

const queueItems = [
    { id: 'Q-1', label: 'NH-48 structural detour validation pipeline', type: 'reasoning' },
    { id: 'Q-2', label: 'Clinker inventory drawdown correlation analysis', type: 'reasoning' },
    { id: 'D-1', label: 'Authorize route allocation variant shift 4B', type: 'decision' },
    { id: 'D-2', label: 'Trigger alternative sourcing parameters contract terms', type: 'decision' }
];

const timelineStages = [
    { title: 'Input News', time: '14:32:10', agent: 'News Intel Agent', duration: '120ms', status: 'Completed', confidence: '99%' },
    { title: 'Classification', time: '14:32:11', agent: 'News Intel Agent', duration: '85ms', status: 'Completed', confidence: '98%' },
    { title: 'Knowledge Graph', time: '14:32:12', agent: 'Impact Agent', duration: '240ms', status: 'Completed', confidence: '95%' },
    { title: 'Risk Analysis', time: '14:32:13', agent: 'Impact Agent', duration: '190ms', status: 'Completed', confidence: '94%' },
    { title: 'Impact Analysis', time: '14:32:14', agent: 'Impact Agent', duration: '310ms', status: 'Completed', confidence: '93%' },
    { title: 'Mitigation', time: '14:32:15', agent: 'Mitigation Agent', duration: '420ms', status: 'Active', confidence: '96%' },
    { title: 'Executive Decision', time: 'Pending', agent: 'System Core Orchestration', duration: '---', status: 'Queued', confidence: '---' }
];

export default function AIDecisionCenter() {
    const [liveTime, setLiveTime] = useState('14:32:15');

    useEffect(() => {
        const timer = setInterval(() => {
            const now = new Date();
            setLiveTime(now.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', second: '2-digit' }));
        }, 1000);
        return () => clearInterval(timer);
    }, []);

    return (
        <div className="adc-content-scope">

            {/* Header Block Section */}
            <header className="adc-header-block">
                <div className="adc-header-left">
                    <h1 className="adc-page-title">AI Decision Center</h1>
                    <p className="adc-page-subtitle">Real-time autonomous multi-agent reasoning and enterprise decision orchestration.</p>
                </div>
                <div className="adc-header-right">
                    <div className="adc-status-pill">
                        <span className="adc-pulse-dot"></span>
                        <span className="adc-status-lbl">AI Status:</span>
                        <span className="adc-status-val font-semibold text-success">Running</span>
                    </div>
                    <div className="adc-meta-pill">
                        <Clock size={12} />
                        <span className="adc-meta-lbl">System Time:</span>
                        <span className="adc-meta-val font-mono">{liveTime}</span>
                    </div>
                </div>
            </header>

            {/* Executive KPI Grid Row */}
            <section className="adc-kpi-grid">
                {kpiData.map((kpi) => {
                    const IconComponent = kpi.icon;
                    return (
                        <div key={kpi.id} className="adc-kpi-card">
                            <div className="adc-kpi-header">
                                <span className="adc-kpi-lbl">{kpi.label}</span>
                                <IconComponent size={16} className={`adc-kpi-icon variant-${kpi.type}`} />
                            </div>
                            <h3 className="adc-kpi-val">{kpi.value}</h3>
                            <p className="adc-kpi-desc">{kpi.desc}</p>
                        </div>
                    );
                })}
            </section>

            {/* Live Communication Wave Transmission Track */}
            <section className="adc-wave-transmission-bar">
                <div className="adc-wave-track-title">
                    <Network size={12} /> Active Telemetry Transmissions:
                </div>
                <div className="adc-wave-track-fluid">
                    <div className="adc-wave-pulse-line"></div>
                    {waveTransmissions.map((packet) => (
                        <span key={packet.id} className="adc-wave-packet-badge">
                            <Zap size={10} /> {packet.label} ({packet.from} <ArrowRight size={8} /> {packet.to})
                        </span>
                    ))}
                </div>
            </section>

            {/* Core Multi-Agent and Monitor Layout Wrapper Grid */}
            <div className="adc-workspace-layout-grid">

                {/* Left/Center Space: The Three Dominant Agent Cards */}
                <div className="adc-agents-mainframe-column">
                    <div className="adc-column-header-row">
                        <Cpu size={16} className="color-brand" />
                        <h2 className="adc-column-section-title">Active AI Agents Infrastructure</h2>
                    </div>

                    <div className="adc-agents-cards-responsive-container">
                        {agentsData.map((agent) => (
                            <div key={agent.id} className={`adc-agent-orchestrator-card theme-${agent.avatarColor}`}>

                                {/* Top Badges Section */}
                                <div className="adc-agent-card-header-meta">
                                    <span className={`adc-attention-indicator state-${agent.attention.toLowerCase().replace(' ', '-')}`}>
                                        <span className="adc-state-ping"></span>
                                        {agent.attention}
                                    </span>
                                    <span className={`adc-emotion-badge rank-${agent.emotion.toLowerCase().replace(' ', '-')}`}>
                                        {agent.emotion}
                                    </span>
                                </div>

                                {/* Premium Animated Robotic Style Avatar Asset */}
                                <div className="adc-avatar-display-wrapper">
                                    <div className={`adc-futuristic-ai-robot-avatar avatar-${agent.avatarColor}`}>
                                        <div className="adc-robot-outer-ring"></div>
                                        <div className="adc-robot-head-frame">
                                            <div className="adc-robot-visor-glow">
                                                <div className="adc-robot-eye left-eye"></div>
                                                <div className="adc-robot-eye right-eye"></div>
                                            </div>
                                            <div className="adc-robot-mouth-matrix"></div>
                                        </div>
                                        <div className="adc-robot-core-pulse"></div>
                                    </div>
                                    <h3 className="adc-agent-display-name">{agent.name}</h3>
                                </div>

                                {/* System Telemetry Analytics Counters */}
                                <div className="adc-agent-telemetry-metrics-strip">
                                    <div className="adc-telemetry-cell">
                                        <span className="adc-t-lbl">Confidence</span>
                                        <span className="adc-t-val font-semibold color-brand">{agent.confidence}</span>
                                    </div>
                                    <div className="adc-telemetry-cell">
                                        <span className="adc-t-lbl">Latent Time</span>
                                        <span className="adc-t-val font-mono">{agent.execTime}</span>
                                    </div>
                                    <div className="adc-telemetry-cell text-right">
                                        <span className="adc-t-lbl">Context Window</span>
                                        <span className="adc-t-val font-mono text-secondary">{agent.tokens}</span>
                                    </div>
                                </div>

                                {/* Continuous Real-Time Live Terminal Reasoning Panel */}
                                <div className="adc-terminal-reasoning-window">
                                    <div className="adc-terminal-title-bar">
                                        <Terminal size={11} /> <span>Live Agent Reasoning Stream</span>
                                    </div>
                                    <div className="adc-terminal-body-content">
                                        <div className="adc-terminal-log-row text-brand">
                                            <span className="adc-prompt-char">&gt;</span> Latest Resolved Decision: {agent.latestDecision}
                                        </div>
                                        {agent.metrics.map((metric, idx) => (
                                            <div key={idx} className="adc-terminal-log-row">
                                                <span className="adc-prompt-char">$</span> <strong className="text-secondary">{metric.label}:</strong> {metric.value}
                                            </div>
                                        ))}
                                        <div className="adc-terminal-cursor-blink"></div>
                                    </div>
                                </div>

                            </div>
                        ))}
                    </div>
                </div>

                {/* Right Space Panel: Enterprise AI Operational Monitor */}
                <aside className="adc-enterprise-monitor-sidebar-column">
                    <div className="adc-column-header-row">
                        <Activity size={16} className="color-brand" />
                        <h2 className="adc-column-section-title">Enterprise AI Monitor</h2>
                    </div>

                    <div className="adc-monitor-properties-stack">
                        {systemMetrics.map((metric, idx) => (
                            <div key={idx} className="adc-monitor-metric-row">
                                <span className="adc-m-lbl">{metric.label}</span>
                                <span className={`adc-m-val font-semibold text-variant-${metric.type}`}>{metric.value}</span>
                            </div>
                        ))}
                    </div>

                    {/* Operational Reasoning & Decision Queue Subpanel */}
                    <div className="adc-monitor-queues-subpanel">
                        <h4 className="adc-subpanel-heading-title">System Ingestion & Resolution Queues</h4>
                        <div className="adc-queue-elements-stack">
                            {queueItems.map((item) => (
                                <div key={item.id} className={`adc-queue-item-card variant-${item.type}`}>
                                    <div className="adc-queue-item-top">
                                        <span className="adc-queue-tag">{item.type} token</span>
                                        <span className="adc-queue-id font-mono">{item.id}</span>
                                    </div>
                                    <p className="adc-queue-label-text">{item.label}</p>
                                </div>
                            ))}
                        </div>
                    </div>
                </aside>

            </div>

            {/* Bottom Section: Decision Flow Pipeline Timeline Grid */}
            <section className="adc-decision-flow-timeline-section">
                <div className="adc-section-title-wrapper border-bottom-sync">
                    <Layers size={16} className="adc-section-title-icon" />
                    <h2 className="adc-section-title">Decision Flow Execution Pipeline</h2>
                </div>

                <div className="adc-timeline-stages-fluid-row">
                    {timelineStages.map((stage, idx) => (
                        <div key={idx} className="adc-timeline-stage-node-container">
                            <div className={`adc-timeline-node-card status-${stage.status.toLowerCase()}`}>
                                <span className={`adc-timeline-status-dot state-${stage.status.toLowerCase()}`}></span>
                                <h4 className="adc-stage-title-text">{stage.title}</h4>
                                <div className="adc-stage-property-strip">
                                    <span>{stage.time}</span>
                                    <span className="font-mono text-brand">{stage.duration}</span>
                                </div>
                                <p className="adc-stage-owner-agent">{stage.agent}</p>
                                <span className="adc-stage-confidence-lbl">Conf: <strong className="font-mono">{stage.confidence}</strong></span>
                            </div>
                            {idx < timelineStages.length - 1 && (
                                <div className="adc-timeline-stage-wave-connector">
                                    <div className="adc-connector-pulse-dot"></div>
                                </div>
                            )}
                        </div>
                    ))}
                </div>
            </section>

            {/* Bottom Final Panel: Latest Executive Decision Platform Output */}
            <section className="adc-latest-decision-output-panel">
                <div className="adc-section-title-wrapper border-none">
                    <CheckCircle2 size={16} className="adc-section-title-icon color-success" />
                    <h2 className="adc-section-title">Latest Autonomous Executive Prescription</h2>
                </div>

                <div className="adc-recommendation-master-card">
                    <div className="adc-recommendation-header-grid">
                        <div className="adc-rec-cell"><span className="adc-r-lbl">Priority Level</span><span className="adc-rec-badge-pill variant-critical"><AlertTriangle size={11} /> Critical Priority</span></div>
                        <div className="adc-rec-cell"><span className="adc-r-lbl">Business Blast Radius Impact</span><span className="adc-rec-val font-semibold color-brand">Avoid Plant A Clinker Shutdown Completely</span></div>
                        <div className="adc-rec-cell"><span className="adc-r-lbl">Estimated Network Delay</span><span className="adc-rec-val font-mono color-critical">+2 hours net variance</span></div>
                        <div className="adc-rec-cell"><span className="adc-r-lbl">Operational Execution Cost</span><span className="adc-rec-val font-mono font-semibold">$4,820 structural buffer</span></div>
                        <div className="adc-rec-cell text-right"><span className="adc-r-lbl">Orchestration Confidence</span><span className="adc-rec-val font-semibold color-success">96.4% safe margin</span></div>
                    </div>

                    <div className="adc-prescribed-strategy-action-block">
                        <span className="adc-r-lbl">Prescribed Sourcing Optimization Strategy Action Directive:</span>
                        <p className="adc-prescribed-action-paragraph">
                            Transfer 1,200 T Limestone from Plant C reserves via secondary rail segment bypass loops.
                            Simultaneously activate alternative solid fuel contract terms with emergency Rajasthan Quarry suppliers
                            to hedge spot energy margin variance scales across the grinding complex.
                        </p>
                    </div>

                    <div className="adc-recommendation-sub-parameters-grid">
                        <div className="adc-sub-param-card"><h5>Alternative Sourcing Nodes</h5><p>Rajasthan Quarry Emergency Framework Contract</p></div>
                        <div className="adc-sub-param-card"><h5>Alternative Routing Protocols</h5><p>Rail segment bypass segment loop via terminal port waiting lanes</p></div>
                        <div className="adc-sub-param-card"><h5>Inventory Allocation Shifts</h5><p>1,200 T Limestone bulk cargo buffer relocation</p></div>
                    </div>
                </div>
            </section>

        </div>
    );
}