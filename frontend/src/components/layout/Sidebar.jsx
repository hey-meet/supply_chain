import React from 'react';
import { NavLink } from 'react-router-dom';
import {
    MdOutlineHub,
    MdCrisisAlert
} from 'react-icons/md';
import {
    RiDashboardLine,
    RiRobot2Line
} from 'react-icons/ri';
import { FaRegNewspaper } from 'react-icons/fa6';
import {
    TbNetwork,
    TbReportAnalytics
} from 'react-icons/tb'; // 🟢 Changed from 'react-react-icons'
import { PiFactoryBold } from 'react-icons/pi';
import { FiSettings } from 'react-icons/fi';
import plantBg from '../../assets/images/plant.png';


const Sidebar = () => {
    const menuItems = [
        { name: 'Executive Dashboard', path: '/', icon: <RiDashboardLine /> },
        { name: 'News Intelligence', path: '/news', icon: <FaRegNewspaper /> },
        { name: 'Incident Center', path: '/incidents', icon: <MdCrisisAlert /> },
        { name: 'Supply Chain Network', path: '/network', icon: <TbNetwork /> },
        { name: 'Plants & Inventory', path: '/plants', icon: <PiFactoryBold /> },
        { name: 'AI Decision Center', path: '/ai-center', icon: <RiRobot2Line /> },
        { name: 'Executive Reports', path: '/reports', icon: <TbReportAnalytics /> },
        { name: 'Settings', path: '/settings', icon: <FiSettings /> }
    ];

    return (
        <>
            <style>{`
                /* Prevent parent layout layers leaking backgrounds or pseudo-overlays into the sidebar space */
                aside,
                .sidebar,
                .sidebar-container,
                [class*="sidebar"],
                [class*="Sidebar"],
                [class*="dashboard"] > aside,
                [class*="layout"] > aside {
                    background-color: transparent !important;
                    background: transparent !important;
                    box-shadow: none !important;
                }

                aside::before, aside::after,
                .sidebar::before, .sidebar::after,
                [class*="sidebar"]::before, [class*="sidebar"]::after {
                    content: none !important;
                    display: none !important;
                }

                /* 
                  CORE SIDEBAR CONTAINER
                */
                .ent-sidebar {
                    position: fixed;
                    top: 0;
                    left: 0;
                    width: 260px;
                    height: 100vh;
                    display: flex;
                    flex-direction: column;
                    
                    background-image: url(${plantBg}) !important;
                    background-repeat: no-repeat !important;
                    background-position: center center !important;
                    background-size: 100% 100% !important;
                    
                    border-top-right-radius: 16px;
                    border-bottom-right-radius: 16px;
                    box-sizing: border-box;
                    font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
                    z-index: 99999 !important;
                    overflow: hidden;
                    transition: width 0.25s ease-in-out;
                }

                .ent-sidebar-header {
                    height: 80px;
                    padding: 0 24px;
                    display: flex;
                    align-items: center;
                    gap: 12px;
                    box-sizing: border-box;
                    background: transparent !important;
                }

                .ent-sidebar-brand-icon {
                    font-size: 24px;
                    color: #ffffff;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    flex-shrink: 0;
                }

                .ent-sidebar-brand-text {
                    display: flex;
                    flex-direction: column;
                    overflow: hidden;
                    white-space: nowrap;
                }

                .ent-sidebar-title {
                    margin: 0;
                    font-size: 15px;
                    font-weight: 600;
                    color: #ffffff;
                    letter-spacing: 0.5px;
                    text-transform: uppercase;
                    line-height: 1.2;
                }

                .ent-sidebar-subtitle {
                    font-size: 10px;
                    font-weight: 400;
                    color: rgba(255, 255, 255, 0.7);
                    letter-spacing: 0.2px;
                    margin-top: 1px;
                }

                .ent-sidebar-divider {
                    height: 1px;
                    background-color: rgba(255, 255, 255, 0.1);
                    margin: 0 16px;
                    border: none;
                }

                .ent-sidebar-nav {
                    flex: 1;
                    padding: 24px 12px;
                    overflow-y: auto;
                    scrollbar-width: none;
                    background: transparent !important;
                }

                .ent-sidebar-nav::-webkit-scrollbar {
                    display: none;
                }

                .ent-sidebar-menu {
                    list-style: none;
                    padding: 0;
                    margin: 0;
                    display: flex;
                    flex-direction: column;
                    gap: 14px;
                    background: transparent !important;
                }

                .ent-sidebar-menu-item {
                    width: 100%;
                    background: transparent !important;
                }

                .ent-sidebar-link {
                    display: flex;
                    align-items: center;
                    gap: 14px;
                    padding: 10px 16px;
                    color: #ffffff;
                    text-decoration: none;
                    font-size: 14px;
                    font-weight: 500;
                    background: transparent !important;
                    background-color: transparent !important;
                    border: 1px solid transparent !important;
                    border-radius: 14px;
                    box-sizing: border-box;
                    white-space: nowrap;
                    opacity: 0.75;
                    transition: opacity 0.2s ease, background-color 0.2s ease, border-color 0.2s ease;
                }

                .ent-sidebar-link-icon {
                    font-size: 20px;
                    color: #ffffff;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    flex-shrink: 0;
                }

                .ent-sidebar-link-name {
                    letter-spacing: 0.2px;
                }

                .ent-sidebar-link:hover {
                    cursor: pointer;
                    opacity: 1;
                    background-color: rgba(255, 255, 255, 0.04) !important;
                    border-color: rgba(255, 255, 255, 0.08) !important;
                }

                /* Active state matching the clean, highly-rounded glass pill container from reference image 2 */
                .ent-sidebar-link.active {
                    opacity: 1;
                   
                   
                    border: 1px solid rgba(255, 255, 255, 0.18) !important;
                    -webkit-backdrop-filter: blur(8px);
                    font-weight: 500;
                }

                @media (max-width: 1024px) {
                    .ent-sidebar {
                        width: 72px;
                    }

                    .ent-sidebar-header {
                        justify-content: center;
                        padding: 0;
                    }

                    .ent-sidebar-brand-text {
                        display: none;
                    }

                    .ent-sidebar-brand-icon {
                        font-size: 26px;
                    }

                    .ent-sidebar-divider {
                        margin: 0 8px;
                    }

                    .ent-sidebar-nav {
                        padding: 20px 6px;
                    }

                    .ent-sidebar-menu {
                        gap: 16px;
                    }

                    .ent-sidebar-link {
                        justify-content: center;
                        padding: 12px;
                        border-radius: 12px;
                    }

                    .ent-sidebar-link-name {
                        display: none;
                    }

                    .ent-sidebar-link:hover {
                        transform: scale(1.03);
                    }
                }

                @media (max-width: 480px) {
                    .ent-sidebar {
                        width: 60px;
                    }
                    
                    .ent-sidebar-link {
                        padding: 10px;
                        border-radius: 10px;
                    }
                }
            `}</style>

            <aside
                className="sidebar ent-sidebar"
                style={{ backgroundImage: `url(${plantBg})` }}
            >
                <div className="ent-sidebar-header">
                    <div className="ent-sidebar-brand-icon">
                        <MdOutlineHub />
                    </div>
                    <div className="ent-sidebar-brand-text">
                        <h1 className="ent-sidebar-title">SC Intelligence</h1>
                        <span className="ent-sidebar-subtitle">AI Supply Chain Platform</span>
                    </div>
                </div>

                <hr className="ent-sidebar-divider" />

                <nav className="ent-sidebar-nav">
                    <ul className="ent-sidebar-menu">
                        {menuItems.map((item, index) => (
                            <li key={index} className="ent-sidebar-menu-item">
                                <NavLink
                                    to={item.path}
                                    className={({ isActive }) =>
                                        isActive ? 'ent-sidebar-link active' : 'ent-sidebar-link'
                                    }
                                >
                                    <span className="ent-sidebar-link-icon">{item.icon}</span>
                                    <span className="ent-sidebar-link-name">{item.name}</span>
                                </NavLink>
                            </li>
                        ))}
                    </ul>
                </nav>
            </aside>
        </>
    );
};

export default Sidebar;