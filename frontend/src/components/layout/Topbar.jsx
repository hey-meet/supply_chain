import React from 'react';
import { useLocation } from 'react-router-dom';

const Topbar = () => {
    const location = useLocation();

    const getPageTitle = (path) => {
        switch (path) {
            case '/': return 'Executive Dashboard';
            case '/news': return 'News Intelligence';
            case '/incidents': return 'Incident Center';
            case '/network': return 'Supply Chain Network';
            case '/plants': return 'Plants & Inventory';
            case '/ai-center': return 'AI Decision Center';
            case '/reports': return 'Executive Reports';
            case '/settings': return 'Settings';
            default: return 'Supply Chain Hub';
        }
    };

    return (
        <header className="topbar">
            <div className="topbar-title">
                {getPageTitle(location.pathname)}
            </div>
            <div className="topbar-actions">
                <input type="text" placeholder="Global system search..." className="search-box" />
                <div className="notification-icon">
                    🔔
                </div>
                <div className="avatar">
                    Admin
                </div>
            </div>
        </header>
    );
};

export default Topbar;