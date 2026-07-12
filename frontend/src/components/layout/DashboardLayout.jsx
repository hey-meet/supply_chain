import React from 'react';
import { Outlet } from 'react-router-dom';
import Sidebar from './Sidebar';
import Topbar from './Topbar';

const DashboardLayout = () => {
    return (
        <div className="app-container">
            <Sidebar />
            <div className="main-wrapper">
                <Topbar />
                <main className="page-content">
                    <Outlet />
                </main>
            </div>
        </div>
    );
};

export default DashboardLayout;