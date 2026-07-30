import React, { useState, useEffect, useRef } from 'react';
import {
    Bot,
    User,
    Send,
    Plus,
    Trash2,
    Copy,
    Check,
    ThumbsUp,
    ThumbsDown,
    Sparkles,
    Search,
    ChevronLeft,
    ChevronRight,
    RotateCcw,
    ShieldAlert,
    MessageSquare,
    Info,
    SlidersHorizontal,
    Activity
} from 'lucide-react';
import '../styles/ai-assistant.css';
import aiService from '../services/aiService';
import incidentService from '../services/incidentService';

const ACTIONS_CATEGORIES = [
    {
        name: "Critical Disruption & Analysis",
        actions: [
            { key: "explain_critical_disruptions", label: "Explain Today's Critical Disruptions" },
            { key: "root_cause_analysis", label: "Root Cause Analysis" },
            { key: "why_critical", label: "Why was this incident classified as Critical?" },
            { key: "executive_summary", label: "Executive Summary" }
        ]
    },
    {
        name: "Operational & Node Exposure",
        actions: [
            { key: "affected_plants", label: "Which plants are affected?" },
            { key: "affected_suppliers", label: "Which suppliers are impacted?" },
            { key: "analyze_plant_risks", label: "Analyze Plant Risks" },
            { key: "analyze_inventory_risks", label: "Analyze Inventory Risks" },
            { key: "explain_route_disruption", label: "Explain Route Disruption" },
            { key: "explain_supplier_impact", label: "Explain Supplier Impact" }
        ]
    },
    {
        name: "Strategic AI Mitigation & Reports",
        actions: [
            { key: "explain_ai_decision", label: "Explain AI Decision" },
            { key: "explain_mitigation_strategy", label: "Explain Mitigation Strategy" },
            { key: "explain_executive_report", label: "Explain Executive Report" },
            { key: "explain_knowledge_graph_dependencies", label: "Explain Knowledge Graph Dependencies" },
            { key: "digital_twin_analysis", label: "Digital Twin Impact Analysis" }
        ]
    }
];

export default function AIAssistant() {
    const [conversations, setConversations] = useState(() => {
        try {
            const saved = localStorage.getItem('sc_ai_conversations');
            return saved ? JSON.parse(saved) : [];
        } catch {
            return [];
        }
    });

    const [activeConvId, setActiveConvId] = useState(() => {
        try {
            const saved = localStorage.getItem('sc_ai_active_conv_id');
            return saved && conversations.some(c => c.id === saved) ? saved : (conversations[0]?.id || 'conv-1');
        } catch {
            return 'conv-1';
        }
    });

    const [searchQuery, setSearchQuery] = useState('');
    const [isTyping, setIsTyping] = useState(false);
    const [typingStage, setTypingStage] = useState('');
    const [copiedMsgId, setCopiedMsgId] = useState(null);
    const [feedbackMap, setFeedbackMap] = useState({});
    const [sidebarCollapsed, setSidebarCollapsed] = useState(false);
    const [pageContext, setPageContext] = useState('incident_center');
    const [isInitializingCache, setIsInitializingCache] = useState(false);

    const messagesEndRef = useRef(null);
    const lastTriggeredActionRef = useRef(null);

    useEffect(() => {
        try {
            localStorage.setItem('sc_ai_conversations', JSON.stringify(conversations));
        } catch (err) {
            console.error('Failed to save conversations to localStorage', err);
        }
    }, [conversations]);

    useEffect(() => {
        try {
            localStorage.setItem('sc_ai_active_conv_id', activeConvId);
        } catch (err) {
            console.error('Failed to save active conversation ID', err);
        }
    }, [activeConvId]);

    const activeConversation = conversations.find(c => c.id === activeConvId) || {
        id: activeConvId,
        title: 'New Executive Session',
        messages: []
    };

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    };

    useEffect(() => {
        scrollToBottom();
    }, [activeConversation.messages, isTyping]);

    const handleNewChat = () => {
        const newId = `conv-${Date.now()}`;
        const newConv = {
            id: newId,
            title: 'New Executive Session',
            updatedAt: 'Just now',
            messages: []
        };
        setConversations(prev => [newConv, ...prev]);
        setActiveConvId(newId);
    };

    const handleDeleteConv = (e, id) => {
        e.stopPropagation();
        const updated = conversations.filter(c => c.id !== id);
        setConversations(updated);
        if (activeConvId === id) {
            if (updated.length > 0) {
                setActiveConvId(updated[0].id);
            } else {
                handleNewChat();
            }
        }
    };

    const handleClearCurrentChat = () => {
        setConversations(prev =>
            prev.map(c => (c.id === activeConvId ? { ...c, messages: [] } : c))
        );
    };

    const executeActionRequest = async (actionKey, actionLabel) => {
        setIsTyping(true);
        setTypingStage('Connecting to BuildCem Operational Intelligence...');

        setTimeout(() => {
            setTypingStage('Retrieving active supply chain state cache...');
        }, 800);

        setTimeout(() => {
            setTypingStage('Formulating structured briefing...');
        }, 1600);

        try {
            const response = await aiService.executeAction(actionKey, pageContext);

            const aiMsg = {
                id: `msg-${Date.now()}`,
                sender: 'ai',
                text: '',
                structuredData: response.data,
                sources: response.data.sources || [],
                timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
            };

            setConversations(prev =>
                prev.map(c => {
                    if (c.id === activeConvId) {
                        const newTitle = c.messages.length === 0 ? actionLabel : c.title;
                        return {
                            ...c,
                            title: newTitle,
                            updatedAt: 'Just now',
                            messages: [...c.messages, aiMsg]
                        };
                    }
                    return c;
                })
            );
        } catch (error) {
            console.error("Action execution error:", error);
            const errorData = error.response?.data;
            if (errorData?.cache_status === "uninitialized" || error.response?.status === 400) {
                setConversations(prev =>
                    prev.map(c => {
                        if (c.id === activeConvId) {
                            return {
                                ...c,
                                messages: [...c.messages, {
                                    id: `err-${Date.now()}`,
                                    sender: 'ai',
                                    text: 'NO_CONTEXT_FALLBACK',
                                    timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
                                }]
                            };
                        }
                        return c;
                    })
                );
            } else {
                setConversations(prev =>
                    prev.map(c => {
                        if (c.id === activeConvId) {
                            return {
                                ...c,
                                messages: [...c.messages, {
                                    id: `err-${Date.now()}`,
                                    sender: 'ai',
                                    text: `System Error: ${errorData?.message || error.message || "Failed to contact operational database."}`,
                                    timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
                                }]
                            };
                        }
                        return c;
                    })
                );
            }
        } finally {
            setIsTyping(false);
            setTypingStage('');
        }
    };

    const handleTriggerAction = (actionKey, actionLabel) => {
        if (isTyping || isInitializingCache) return;

        lastTriggeredActionRef.current = { key: actionKey, label: actionLabel };

        const userMsg = {
            id: `msg-${Date.now()}`,
            sender: 'user',
            text: `Executive Command: ${actionLabel}`,
            timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
        };

        setConversations(prev => {
            const exists = prev.some(c => c.id === activeConvId);
            if (!exists) {
                const newConv = {
                    id: activeConvId,
                    title: actionLabel,
                    updatedAt: 'Just now',
                    messages: [userMsg]
                };
                return [newConv];
            }
            return prev.map(c => {
                if (c.id === activeConvId) {
                    const newTitle = c.messages.length === 0 ? actionLabel : c.title;
                    return {
                        ...c,
                        title: newTitle,
                        updatedAt: 'Just now',
                        messages: [...c.messages, userMsg]
                    };
                }
                return c;
            });
        });

        executeActionRequest(actionKey, actionLabel);
    };

    const handleInitializeCache = async () => {
        setIsInitializingCache(true);
        setIsTyping(true);
        setTypingStage('Running autonomous news scan and threat assessment pipeline (LangGraph)...');
        try {
            await incidentService.getIncidentCenter("Rajasthan limestone route blockade");

            setConversations(prev =>
                prev.map(c => {
                    if (c.id === activeConvId) {
                        return {
                            ...c,
                            messages: [...c.messages, {
                                id: `init-${Date.now()}`,
                                sender: 'ai',
                                text: 'Operational context initialized successfully. Retrying executive briefing...',
                                timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
                            }]
                        };
                    }
                    return c;
                })
            );

            if (lastTriggeredActionRef.current) {
                const { key, label } = lastTriggeredActionRef.current;
                await executeActionRequest(key, label);
            }
        } catch (error) {
            console.error("Failed to execute baseline LangGraph scan:", error);
            setConversations(prev =>
                prev.map(c => {
                    if (c.id === activeConvId) {
                        return {
                            ...c,
                            messages: [...c.messages, {
                                id: `err-${Date.now()}`,
                                sender: 'ai',
                                text: 'Operational scan failed. Please check backend connection.',
                                timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
                            }]
                        };
                    }
                    return c;
                })
            );
        } finally {
            setIsInitializingCache(false);
            setIsTyping(false);
            setTypingStage('');
        }
    };

    const handleCopyMessage = (msgId, text) => {
        navigator.clipboard.writeText(text);
        setCopiedMsgId(msgId);
        setTimeout(() => setCopiedMsgId(null), 2000);
    };

    const handleToggleFeedback = (msgId, type) => {
        setFeedbackMap(prev => ({
            ...prev,
            [msgId]: prev[msgId] === type ? null : type
        }));
    };

    const filteredConversations = conversations.filter(c =>
        c.title.toLowerCase().includes(searchQuery.toLowerCase())
    );

    return (
        <div className="ai-assistant-page">
            {/* LEFT PANEL: Conversation History Drawer */}
            <aside className={`ai-history-sidebar ${sidebarCollapsed ? 'collapsed' : ''}`}>
                <div className="history-header">
                    <div className="history-title-row">
                        <div className="history-brand">
                            <Activity className="history-brand-icon" />
                            <h3 className="history-title">Executive Sessions</h3>
                        </div>
                        <button
                            type="button"
                            className="collapse-sidebar-btn"
                            onClick={() => setSidebarCollapsed(!sidebarCollapsed)}
                            title={sidebarCollapsed ? 'Expand sidebar' : 'Collapse sidebar'}
                            aria-label="Toggle history sidebar"
                        >
                            {sidebarCollapsed ? <ChevronRight /> : <ChevronLeft />}
                        </button>
                    </div>

                    {!sidebarCollapsed && (
                        <>
                            <button type="button" className="new-chat-btn" onClick={handleNewChat}>
                                <Plus className="btn-icon" />
                                <span>New Session</span>
                            </button>
                            <div className="history-search-box">
                                <Search className="search-icon" />
                                <input
                                    type="text"
                                    placeholder="Search history..."
                                    value={searchQuery}
                                    onChange={(e) => setSearchQuery(e.target.value)}
                                />
                            </div>
                        </>
                    )}
                </div>

                {!sidebarCollapsed && (
                    <div className="history-list" role="listbox" aria-label="Conversation History">
                        {filteredConversations.length === 0 ? (
                            <div className="no-history-text">No active sessions found</div>
                        ) : (
                            filteredConversations.map((conv) => (
                                <div
                                    key={conv.id}
                                    tabIndex={0}
                                    role="option"
                                    aria-selected={activeConvId === conv.id}
                                    className={`history-item ${activeConvId === conv.id ? 'active' : ''}`}
                                    onClick={() => setActiveConvId(conv.id)}
                                    onKeyDown={(e) => {
                                        if (e.key === 'Enter' || e.key === ' ') {
                                            e.preventDefault();
                                            setActiveConvId(conv.id);
                                        }
                                    }}
                                >
                                    <div className="history-item-content">
                                        <div className="history-item-title">{conv.title}</div>
                                        <div className="history-item-meta">{conv.updatedAt}</div>
                                    </div>
                                    <button
                                        type="button"
                                        className="delete-conv-btn"
                                        title="Delete conversation"
                                        onClick={(e) => handleDeleteConv(e, conv.id)}
                                    >
                                        <Trash2 className="trash-icon" />
                                    </button>
                                </div>
                            ))
                        )}
                    </div>
                )}
            </aside>

            {/* RIGHT PANEL: Main Chat Canvas */}
            <main className="ai-chat-main">
                {/* Header */}
                <header className="chat-header-bar">
                    <div className="chat-header-info">
                        {sidebarCollapsed && (
                            <button
                                type="button"
                                className="expand-sidebar-mobile-btn"
                                onClick={() => setSidebarCollapsed(false)}
                            >
                                <ChevronRight />
                            </button>
                        )}
                        <div className="chat-title-group">
                            <h2 className="chat-topic-title">{activeConversation.title}</h2>
                            <div className="model-status-badge">
                                <span className="status-pulse-dot"></span>
                                <Sparkles className="sparkle-icon" />
                                <span>BuildCem Executive Copilot</span>
                            </div>
                        </div>
                    </div>
                    <div className="chat-header-actions">
                        <button
                            type="button"
                            className="chat-action-btn"
                            onClick={handleClearCurrentChat}
                            title="Clear current messages"
                            disabled={activeConversation.messages.length === 0}
                        >
                            <RotateCcw className="action-icon" />
                            <span>Clear Session</span>
                        </button>
                    </div>
                </header>

                {/* Messages Stream */}
                <div className="chat-messages-container">
                    {activeConversation.messages.length === 0 ? (
                        <div className="chat-welcome-state">
                            <div className="welcome-avatar-wrapper">
                                <Bot className="welcome-avatar-icon" />
                            </div>
                            <h1 className="welcome-title">Executive Copilot Console</h1>
                            <p className="welcome-subtitle">
                                Formulate enterprise risk briefings, route optimization impact, and inventory forecasts based on real-time graph operations telemetry.
                            </p>

                            <div className="quick-prompts-grid">
                                {ACTIONS_CATEGORIES.flatMap(c => c.actions).slice(0, 4).map((item, idx) => (
                                    <button
                                        key={idx}
                                        type="button"
                                        className="quick-prompt-card"
                                        onClick={() => handleTriggerAction(item.key, item.label)}
                                    >
                                        <div className="prompt-card-header">
                                            <Sparkles className="prompt-icon" />
                                            <span className="prompt-category">Quick Command</span>
                                        </div>
                                        <p className="prompt-text">{item.label}</p>
                                    </button>
                                ))}
                            </div>
                        </div>
                    ) : (
                        <div className="messages-stream">
                            {activeConversation.messages.map((msg) => (
                                <div
                                    key={msg.id}
                                    className={`message-row ${msg.sender === 'user' ? 'user-row' : 'ai-row'}`}
                                >
                                    <div className="message-avatar">
                                        {msg.sender === 'user' ? <User /> : <Bot />}
                                    </div>
                                    <div className="message-bubble-wrapper">
                                        <div className="message-bubble-header">
                                            <span className="sender-name">
                                                {msg.sender === 'user' ? 'Executive Director' : 'SC Operations Intelligence'}
                                            </span>
                                            <span className="msg-timestamp">{msg.timestamp}</span>
                                        </div>

                                        {msg.text === "NO_CONTEXT_FALLBACK" ? (
                                            <div className="fallback-context-card">
                                                <div className="fallback-card-header">
                                                    <ShieldAlert className="fallback-warning-icon" />
                                                    <span>Operational Context Uninitialized</span>
                                                </div>
                                                <p className="fallback-card-text">
                                                    The backend's in-memory graph cache is uninitialized. To analyze specific operations, run a baseline supply chain disruption scan.
                                                </p>
                                                <button
                                                    type="button"
                                                    className="initialize-cache-btn"
                                                    onClick={() => handleInitializeCache()}
                                                    disabled={isInitializingCache}
                                                >
                                                    {isInitializingCache ? "Executing LangGraph Pipeline..." : "Execute Baseline Disruption Scan"}
                                                </button>
                                            </div>
                                        ) : msg.structuredData ? (
                                            <div className="structured-briefing-card">
                                                <div className="briefing-section summary">
                                                    <h4 className="section-title">Executive Summary</h4>
                                                    <p className="section-body">{msg.structuredData.executive_summary}</p>
                                                </div>

                                                <div className="briefing-section reasoning">
                                                    <h4 className="section-title">Business Reasoning</h4>
                                                    <p className="section-body">{msg.structuredData.business_reasoning}</p>
                                                </div>

                                                {msg.structuredData.affected_entities && msg.structuredData.affected_entities.length > 0 && (
                                                    <div className="briefing-section entities">
                                                        <h4 className="section-title">Affected Entities</h4>
                                                        <div className="entity-chips">
                                                            {msg.structuredData.affected_entities.map((ent, idx) => (
                                                                <span key={idx} className="entity-chip">{ent}</span>
                                                            ))}
                                                        </div>
                                                    </div>
                                                )}

                                                {msg.structuredData.knowledge_graph_dependencies && msg.structuredData.knowledge_graph_dependencies.length > 0 && (
                                                    <div className="briefing-section dependencies">
                                                        <h4 className="section-title">Knowledge Graph Dependencies</h4>
                                                        <ul className="dependency-list">
                                                            {msg.structuredData.knowledge_graph_dependencies.map((dep, idx) => (
                                                                <li key={idx}>{dep}</li>
                                                            ))}
                                                        </ul>
                                                    </div>
                                                )}

                                                {msg.structuredData.recommendations && msg.structuredData.recommendations.length > 0 && (
                                                    <div className="briefing-section recommendations">
                                                        <h4 className="section-title">AI Operational Recommendations</h4>
                                                        <ul className="recommendation-list">
                                                            {msg.structuredData.recommendations.map((rec, idx) => (
                                                                <li key={idx}>{rec}</li>
                                                            ))}
                                                        </ul>
                                                    </div>
                                                )}

                                                <div className="briefing-meta">
                                                    <span className="confidence-badge">Confidence Score: {msg.structuredData.confidence}</span>
                                                </div>
                                            </div>
                                        ) : (
                                            <div className="message-text">
                                                {(msg.text || '').split('\n').map((paragraph, pIdx) => (
                                                    <p key={pIdx}>{paragraph}</p>
                                                ))}
                                            </div>
                                        )}

                                        {msg.sources && msg.sources.length > 0 && (
                                            <div className="message-sources-block">
                                                <span className="sources-label">Verified Sources:</span>
                                                {msg.sources.map((src, sIdx) => (
                                                    <span key={sIdx} className="source-tag">
                                                        <Info className="info-icon" />
                                                        {src}
                                                    </span>
                                                ))}
                                            </div>
                                        )}

                                        {msg.sender === 'ai' && msg.text !== 'NO_CONTEXT_FALLBACK' && (
                                            <div className="message-footer-actions">
                                                <button
                                                    type="button"
                                                    className="msg-tool-btn"
                                                    onClick={() => handleCopyMessage(msg.id, msg.structuredData ? JSON.stringify(msg.structuredData, null, 2) : msg.text)}
                                                    title="Copy response JSON/Text"
                                                >
                                                    {copiedMsgId === msg.id ? (
                                                        <Check className="copied-icon" />
                                                    ) : (
                                                        <Copy />
                                                    )}
                                                    <span>{copiedMsgId === msg.id ? 'Copied' : 'Copy Payload'}</span>
                                                </button>
                                                <button
                                                    type="button"
                                                    className={`msg-tool-btn ${feedbackMap[msg.id] === 'up' ? 'active-up' : ''}`}
                                                    onClick={() => handleToggleFeedback(msg.id, 'up')}
                                                    title="Helpful"
                                                >
                                                    <ThumbsUp />
                                                </button>
                                                <button
                                                    type="button"
                                                    className={`msg-tool-btn ${feedbackMap[msg.id] === 'down' ? 'active-down' : ''}`}
                                                    onClick={() => handleToggleFeedback(msg.id, 'down')}
                                                    title="Unhelpful"
                                                >
                                                    <ThumbsDown />
                                                </button>
                                            </div>
                                        )}
                                    </div>
                                </div>
                            ))}

                            <div aria-live="polite" className="typing-live-region">
                                {isTyping && (
                                    <div className="message-row ai-row typing-row">
                                        <div className="message-avatar">
                                            <Bot />
                                        </div>
                                        <div className="message-bubble-wrapper typing-bubble">
                                            <div className="typing-indicator-dots">
                                                <span></span>
                                                <span></span>
                                                <span></span>
                                            </div>
                                            <span className="typing-stage-text">{typingStage}</span>
                                        </div>
                                    </div>
                                )}
                            </div>

                            <div ref={messagesEndRef} />
                        </div>
                    )}
                </div>

                {/* Unified Command Console Bottom Panel */}
                <footer className="executive-action-dashboard">
                    <div className="dashboard-controls-row">
                        <div className="context-selector-group">
                            <SlidersHorizontal className="control-icon" />
                            <span className="control-label">Active Page Context:</span>
                            <select
                                value={pageContext}
                                onChange={(e) => setPageContext(e.target.value)}
                                className="page-context-select"
                                disabled={isTyping || isInitializingCache}
                            >
                                <option value="incident_center">Incident Center</option>
                                <option value="plants_inventory">Plants & Inventory</option>
                                <option value="supply_chain_network">Supply Chain Network</option>
                                <option value="decision_center">AI Decision Center</option>
                                <option value="executive_reports">Executive Reports</option>
                                <option value="executive_dashboard">Executive Dashboard</option>
                            </select>
                        </div>
                        <span className="console-status-note">
                            Select an Executive Action below to trigger automated graph telemetry query.
                        </span>
                    </div>

                    <div className="action-categories-container">
                        {ACTIONS_CATEGORIES.map((cat, idx) => (
                            <div key={idx} className="action-category-group">
                                <h4 className="category-group-title">{cat.name}</h4>
                                <div className="category-actions-grid">
                                    {cat.actions.map((act) => (
                                        <button
                                            key={act.key}
                                            type="button"
                                            className="executive-action-btn"
                                            onClick={() => handleTriggerAction(act.key, act.label)}
                                            disabled={isTyping || isInitializingCache}
                                        >
                                            {act.label}
                                        </button>
                                    ))}
                                </div>
                            </div>
                        ))}
                    </div>
                </footer>
            </main>
        </div>
    );
}