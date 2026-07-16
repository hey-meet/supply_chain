// DashboardLayout.jsx
import React from 'react';
import { Outlet } from 'react-router-dom';
import Sidebar from './Sidebar';
import Topbar from './Topbar';
import '../../styles/dashboard-layout.css';


const DashboardLayout = () => {
    return (
        <div className="app-container">
            <Sidebar />
            <div className="main-wrapper">
                <Topbar />
                <main className="page-content">
                    <div className="page-container">
                        <Outlet />
                    </div>
                </main>
            </div>
        </div>
    );
};

export default DashboardLayout;