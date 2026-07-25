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
    TrendingUp,
    Factory,
    Layers,
    MessageSquare,
    Info
} from 'lucide-react';
import '../styles/ai-assistant.css';

const DEFAULT_CONVERSATIONS = [
    {
        id: 'conv-1',
        title: 'Red Sea Route Disruption Risk',
        updatedAt: '10 mins ago',
        messages: [
            {
                id: 'm1',
                sender: 'user',
                text: 'What is the operational impact of the Red Sea shipping route congestion on our Tier-1 electronics suppliers?',
                timestamp: '10:14 AM'
            },
            {
                id: 'm2',
                sender: 'ai',
                text: 'Based on real-time disruption telemetry and Knowledge Graph analysis:\n\n1. **Lead Time Increase**: Cape of Good Hope rerouting adds **10 to 14 days** to Asia-Europe transit.\n2. **Inventory Risk**: Plant 3 (Munich Assembly) holds **12 days of buffer stock** for semiconductor microcontrollers, putting production at high risk of disruption within 48 hours.\n3. **Recommended Action**: Expedite air-freight allocation for 4,500 critical units from Taiwan supplier TSMC.',
                sources: ['Shipment Telemetry #ST-9941', 'Knowledge Graph: Supplier-Tier1', 'Inventory Service'],
                timestamp: '10:15 AM'
            }
        ]
    },
    {
        id: 'conv-2',
        title: 'Semiconductor Stock Buffer Analysis',
        updatedAt: '2 hours ago',
        messages: [
            {
                id: 'm3',
                sender: 'user',
                text: 'Evaluate current inventory safety stock for Semiconductor Plant Alpha.',
                timestamp: '08:30 AM'
            },
            {
                id: 'm4',
                sender: 'ai',
                text: 'Semiconductor Plant Alpha is currently operating at **84% safety capacity**. Inventory buffers for silicon wafers are adequate for 21 days under standard burn rates. No immediate critical stockouts detected.',
                sources: ['Plant Inventory Service'],
                timestamp: '08:31 AM'
            }
        ]
    }
];

const QUICK_PROMPTS = [
    {
        icon: ShieldAlert,
        category: 'Risk Intelligence',
        prompt: 'Analyze supply chain risk alerts and disruption markers from the past 24 hours.'
    },
    {
        icon: Factory,
        category: 'Inventory Safety',
        prompt: 'Evaluate inventory safety stock levels and stockout risks across assembly plants.'
    },
    {
        icon: TrendingUp,
        category: 'Route Optimization',
        prompt: 'What are the alternative logistics routes to bypass current port congestion in Rotterdam?'
    },
    {
        icon: Layers,
        category: 'Mitigation Strategy',
        prompt: 'Generate an executive mitigation strategy for Tier-1 component supplier delays.'
    }
];

export default function AIAssistant() {
    // LocalStorage persistence for conversations
    const [conversations, setConversations] = useState(() => {
        try {
            const saved = localStorage.getItem('sc_ai_conversations');
            return saved ? JSON.parse(saved) : DEFAULT_CONVERSATIONS;
        } catch {
            return DEFAULT_CONVERSATIONS;
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

    const [inputText, setInputText] = useState('');
    const [searchQuery, setSearchQuery] = useState('');
    const [isTyping, setIsTyping] = useState(false);
    const [typingStage, setTypingStage] = useState('');
    const [copiedMsgId, setCopiedMsgId] = useState(null);
    const [feedbackMap, setFeedbackMap] = useState({});
    const [sidebarCollapsed, setSidebarCollapsed] = useState(false);

    const messagesEndRef = useRef(null);
    const inputRef = useRef(null);

    // Sync to localStorage
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
        title: 'New Conversation',
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
            title: 'New Conversation',
            updatedAt: 'Just now',
            messages: []
        };
        setConversations(prev => [newConv, ...prev]);
        setActiveConvId(newId);
        setTimeout(() => inputRef.current?.focus(), 100);
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
        setTimeout(() => inputRef.current?.focus(), 100);
    };

    const generateAIResponse = (userMsgText) => {
        setIsTyping(true);
        setTypingStage('Connecting to SC Intelligence Graph...');

        setTimeout(() => {
            setTypingStage('Analyzing supplier node dependencies and shipment streams...');
        }, 1000);

        setTimeout(() => {
            setTypingStage('Synthesizing executive recommendation...');
        }, 2200);

        setTimeout(() => {
            let responseText = '';
            let sources = [];

            const lower = userMsgText.toLowerCase();
            if (lower.includes('red sea') || lower.includes('route') || lower.includes('shipping')) {
                responseText = `### Route Disruption & Delay Breakdown\n\n- **Route Transit**: Vessels bypass Suez Canal via Cape of Good Hope, adding **+12 days** average shipping delay.\n- **Affected Cargo**: 14 maritime containers transporting high-density battery cells and active component kits.\n- **Mitigation Strategy**: Reroute upcoming priority shipments through West Coast air corridor and activate regional safety buffers in Munich.`;
                sources = ['Maritime Telemetry Stream', 'Suez Routing Monitor', 'Knowledge Graph'];
            } else if (lower.includes('inventory') || lower.includes('plant') || lower.includes('stock')) {
                responseText = `### Plant Safety Stock Assessment\n\n- **Plant 1 (Silicon Valley)**: 28 days safety stock available (**Low Risk**).\n- **Plant 3 (Munich)**: 9 days safety stock available (**High Vulnerability**).\n- **Action Item**: Trigger automated inter-facility inventory balancing from Plant 1 to Plant 3 to prevent line stoppage.`;
                sources = ['Inventory Service v2', 'SAP ERP Connector'];
            } else {
                responseText = `### AI Supply Chain Analysis\n\nBased on real-time graph queries and operational telemetry:\n\n1. **System Health**: All critical logistics corridors are currently monitored with zero severity-1 outages.\n2. **Predictive Risk**: Moderate risk detected around Tier-2 copper suppliers due to weather disruptions.\n3. **Recommended Next Steps**: Review **Incident Center** for real-time status updates or query specific plant nodes.`;
                sources = ['Supply Chain Decision Orchestrator', 'Telemetry Stream'];
            }

            const aiMsg = {
                id: `msg-${Date.now()}`,
                sender: 'ai',
                text: responseText,
                sources: sources,
                timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
            };

            setConversations(prev =>
                prev.map(c => {
                    if (c.id === activeConvId) {
                        const newTitle =
                            c.messages.length === 0
                                ? userMsgText.slice(0, 32) + (userMsgText.length > 32 ? '...' : '')
                                : c.title;
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

            setIsTyping(false);
            setTypingStage('');
            // Accessibility focus management: return focus to input
            setTimeout(() => inputRef.current?.focus(), 100);
        }, 3200);
    };

    const handleSendMessage = (textToSend) => {
        const queryText = textToSend || inputText;
        if (!queryText.trim() || isTyping) return;

        const userMsg = {
            id: `msg-${Date.now()}`,
            sender: 'user',
            text: queryText.trim(),
            timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
        };

        setConversations(prev =>
            prev.map(c => {
                if (c.id === activeConvId) {
                    const newTitle =
                        c.messages.length === 0
                            ? queryText.slice(0, 32) + (queryText.length > 32 ? '...' : '')
                            : c.title;
                    return {
                        ...c,
                        title: newTitle,
                        updatedAt: 'Just now',
                        messages: [...c.messages, userMsg]
                    };
                }
                return c;
            })
        );

        setInputText('');
        generateAIResponse(queryText);
    };

    const handleKeyDown = (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            handleSendMessage();
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
                            <MessageSquare className="history-brand-icon" />
                            <h3 className="history-title">Conversations</h3>
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
                                <span>New Conversation</span>
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
                            <div className="no-history-text">No conversations found</div>
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
                                <span>SC-Orchestrator AI v4.2</span>
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
                            <span>Clear Chat</span>
                        </button>
                    </div>
                </header>

                {/* Messages Body */}
                <div className="chat-messages-container">
                    {activeConversation.messages.length === 0 ? (
                        /* Welcome / Empty State */
                        <div className="chat-welcome-state">
                            <div className="welcome-avatar-wrapper">
                                <Bot className="welcome-avatar-icon" />
                            </div>
                            <h1 className="welcome-title">Supply Chain AI Assistant</h1>
                            <p className="welcome-subtitle">
                                Ask queries about real-time supplier risks, shipment telemetry, safety stock levels, or operational mitigation pathways.
                            </p>

                            <div className="quick-prompts-grid">
                                {QUICK_PROMPTS.map((item, idx) => {
                                    const IconComp = item.icon;
                                    return (
                                        <button
                                            key={idx}
                                            type="button"
                                            className="quick-prompt-card"
                                            onClick={() => handleSendMessage(item.prompt)}
                                        >
                                            <div className="prompt-card-header">
                                                <IconComp className="prompt-icon" />
                                                <span className="prompt-category">{item.category}</span>
                                            </div>
                                            <p className="prompt-text">{item.prompt}</p>
                                        </button>
                                    );
                                })}
                            </div>
                        </div>
                    ) : (
                        /* Conversation Messages Stream */
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
                                                {msg.sender === 'user' ? 'Executive User' : 'SC Decision Assistant'}
                                            </span>
                                            <span className="msg-timestamp">{msg.timestamp}</span>
                                        </div>
                                        <div className="message-text">
                                            {msg.text.split('\n').map((paragraph, pIdx) => (
                                                <p key={pIdx}>{paragraph}</p>
                                            ))}
                                        </div>

                                        {msg.sources && msg.sources.length > 0 && (
                                            <div className="message-sources-block">
                                                <span className="sources-label">Sources:</span>
                                                {msg.sources.map((src, sIdx) => (
                                                    <span key={sIdx} className="source-tag">
                                                        <Info className="info-icon" />
                                                        {src}
                                                    </span>
                                                ))}
                                            </div>
                                        )}

                                        {msg.sender === 'ai' && (
                                            <div className="message-footer-actions">
                                                <button
                                                    type="button"
                                                    className="msg-tool-btn"
                                                    onClick={() => handleCopyMessage(msg.id, msg.text)}
                                                    title="Copy response"
                                                >
                                                    {copiedMsgId === msg.id ? (
                                                        <Check className="copied-icon" />
                                                    ) : (
                                                        <Copy />
                                                    )}
                                                    <span>{copiedMsgId === msg.id ? 'Copied' : 'Copy'}</span>
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

                            {/* Typing / Processing Live Region for Accessibility */}
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

                {/* Input Bar */}
                <footer className="chat-input-footer">
                    <div className="input-box-wrapper">
                        <textarea
                            ref={inputRef}
                            className="chat-textarea"
                            placeholder="Ask SC Intelligence Assistant... (Press Enter to send, Shift+Enter for new line)"
                            rows={1}
                            value={inputText}
                            onChange={(e) => setInputText(e.target.value)}
                            onKeyDown={handleKeyDown}
                        />
                        <button
                            type="button"
                            className="send-msg-btn"
                            disabled={!inputText.trim() || isTyping}
                            onClick={() => handleSendMessage()}
                            title="Send Message"
                        >
                            <Send className="send-icon" />
                        </button>
                    </div>
                    <div className="input-disclaimer">
                        AI Decision Assistant provides predictive guidance based on real-time graph telemetry. Verify critical inventory allocations before dispatch.
                    </div>
                </footer>
            </main>
        </div>
    );
}
