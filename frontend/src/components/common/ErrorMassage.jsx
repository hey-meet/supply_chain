import React, { useState } from 'react';
import { AlertTriangle, RefreshCw, ChevronDown, ChevronUp } from 'lucide-react';
import '../../styles/common-components.css';

export default function ErrorMessage({
    title = 'System Error Encountered',
    message = 'An unexpected issue occurred while processing your request.',
    details = null,
    onRetry = null,
    compact = false
}) {
    const [showDetails, setShowDetails] = useState(false);

    return (
        <div className={`error-message-container ${compact ? 'compact' : ''}`} role="alert">
            <div className="error-message-header">
                <div className="error-icon-badge">
                    <AlertTriangle className="error-icon" />
                </div>
                <div className="error-text-content">
                    <h4 className="error-title">{title}</h4>
                    <p className="error-description">{message}</p>
                </div>
                {onRetry && (
                    <button type="button" className="error-retry-btn" onClick={onRetry}>
                        <RefreshCw className="retry-icon" />
                        <span>Retry</span>
                    </button>
                )}
            </div>

            {details && (
                <div className="error-details-wrapper">
                    <button
                        type="button"
                        className="error-toggle-details-btn"
                        onClick={() => setShowDetails(!showDetails)}
                    >
                        <span>{showDetails ? 'Hide technical details' : 'Show technical details'}</span>
                        {showDetails ? <ChevronUp className="chevron-icon" /> : <ChevronDown className="chevron-icon" />}
                    </button>
                    {showDetails && (
                        <pre className="error-details-code">
                            <code>{typeof details === 'object' ? JSON.stringify(details, null, 2) : String(details)}</code>
                        </pre>
                    )}
                </div>
            )}
        </div>
    );
}
