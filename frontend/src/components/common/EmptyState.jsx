import React from 'react';
import { Database, RefreshCw, AlertCircle } from 'lucide-react';
import '../../styles/common-components.css';

export default function EmptyState({
    title = 'No Data Available',
    description = 'There are currently no records to display.',
    icon: Icon = Database,
    actionLabel,
    onAction,
    compact = false
}) {
    return (
        <div className={`empty-state-container ${compact ? 'compact' : ''}`}>
            <div className="empty-state-icon-wrapper">
                <Icon className="empty-state-icon" />
            </div>
            <h4 className="empty-state-title">{title}</h4>
            <p className="empty-state-description">{description}</p>
            {actionLabel && onAction && (
                <button type="button" className="empty-state-action-btn" onClick={onAction}>
                    <RefreshCw className="btn-icon" />
                    <span>{actionLabel}</span>
                </button>
            )}
        </div>
    );
}
