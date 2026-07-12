import React from 'react';
import { NavLink } from 'react-router-dom';

const Sidebar = () => {
    const menuItems = [
        { name: 'Executive Dashboard', path: '/' },
        { name: 'News Intelligence', path: '/news' },
        { name: 'Incident Center', path: '/incidents' },
        { name: 'Supply Chain Network', path: '/network' },
        { name: 'Plants & Inventory', path: '/plants' },
        { name: 'AI Decision Center', path: '/ai-center' },
        { name: 'Executive Reports', path: '/reports' },
        { name: 'Settings', path: '/settings' }
    ];

    return (
        <aside className="sidebar">
            <div className="sidebar-logo">
                SC INTELLIGENCE
            </div>
            <ul className="sidebar-menu">
                {menuItems.map((item, index) => (
                    <li key={index}>
                        <NavLink
                            to={item.path}
                            className={({ isActive }) => isActive ? 'sidebar-link active' : 'sidebar-link'}
                        >
                            {item.name}
                        </NavLink>
                    </li>
                ))}
            </ul>
        </aside>
    );
};

export default Sidebar;