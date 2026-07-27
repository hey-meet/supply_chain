import React from 'react';
import '../../styles/common-components.css';

export default function SkeletonLoader({ type = 'card', count = 1 }) {
    const renderSkeleton = (key) => {
        switch (type) {
            case 'card':
                return (
                    <div key={key} className="skeleton-card">
                        <div className="skeleton-shimmer"></div>
                        <div className="skeleton-header">
                            <div className="skeleton-title"></div>
                            <div className="skeleton-badge"></div>
                        </div>
                        <div className="skeleton-body">
                            <div className="skeleton-line long"></div>
                            <div className="skeleton-line medium"></div>
                            <div className="skeleton-line short"></div>
                        </div>
                    </div>
                );

            case 'metrics':
                return (
                    <div key={key} className="skeleton-metric">
                        <div className="skeleton-shimmer"></div>
                        <div className="skeleton-icon-box"></div>
                        <div className="skeleton-metric-content">
                            <div className="skeleton-line short"></div>
                            <div className="skeleton-value"></div>
                        </div>
                    </div>
                );

            case 'table':
                return (
                    <div key={key} className="skeleton-table-wrapper">
                        <div className="skeleton-shimmer"></div>
                        <div className="skeleton-table-row header">
                            <div className="skeleton-cell"></div>
                            <div className="skeleton-cell"></div>
                            <div className="skeleton-cell"></div>
                            <div className="skeleton-cell"></div>
                        </div>
                        {[1, 2, 3, 4].map((i) => (
                            <div key={i} className="skeleton-table-row">
                                <div className="skeleton-cell"></div>
                                <div className="skeleton-cell"></div>
                                <div className="skeleton-cell"></div>
                                <div className="skeleton-cell"></div>
                            </div>
                        ))}
                    </div>
                );

            case 'list':
                return (
                    <div key={key} className="skeleton-list-item">
                        <div className="skeleton-shimmer"></div>
                        <div className="skeleton-avatar"></div>
                        <div className="skeleton-list-text">
                            <div className="skeleton-line medium"></div>
                            <div className="skeleton-line short"></div>
                        </div>
                    </div>
                );

            case 'chat':
                return (
                    <div key={key} className="skeleton-chat-bubble">
                        <div className="skeleton-shimmer"></div>
                        <div className="skeleton-avatar"></div>
                        <div className="skeleton-bubble-content">
                            <div className="skeleton-line long"></div>
                            <div className="skeleton-line medium"></div>
                        </div>
                    </div>
                );

            default:
                return (
                    <div key={key} className="skeleton-box">
                        <div className="skeleton-shimmer"></div>
                    </div>
                );
        }
    };

    return (
        <div className={`skeleton-loader-container skeleton-type-${type}`}>
            {Array.from({ length: count }).map((_, idx) => renderSkeleton(idx))}
        </div>
    );
}
