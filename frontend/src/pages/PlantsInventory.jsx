import React from 'react';
import '../styles/plants-inventory.css';

const PlantsInventory = () => {
    return (
        <div className="fade-in">
            <div className="page-header">
                <h1 className="page-title">Plants & Inventory</h1>
                <p className="page-description">Asset allocations, safety reserves, warehouse telemetry, and production metrics.</p>
            </div>

            <div className="grid-4">
                <div className="panel-card">
                    <h3>Plant Austin</h3>
                    <p style={{ fontSize: '0.85rem', color: 'var(--text-secondary)' }}>Status: Optimal</p>
                    <div className="inventory-progress-bar">
                        <div className="inventory-progress-fill" style={{ width: '78%' }}></div>
                    </div>
                    <span style={{ fontSize: '0.8rem', display: 'block', marginTop: '6px' }}>78% Stock Capacity</span>
                </div>
                <div className="panel-card">
                    <h3>Plant Berlin</h3>
                    <p style={{ fontSize: '0.85rem', color: 'var(--text-secondary)' }}>Status: Supply Warning</p>
                    <div className="inventory-progress-bar">
                        <div className="inventory-progress-fill warning" style={{ width: '42%' }}></div>
                    </div>
                    <span style={{ fontSize: '0.8rem', display: 'block', marginTop: '6px' }}>42% Stock Capacity</span>
                </div>
                <div className="panel-card">
                    <h3>Plant Tokyo</h3>
                    <p style={{ fontSize: '0.85rem', color: 'var(--text-secondary)' }}>Status: Optimal</p>
                    <div className="inventory-progress-bar">
                        <div className="inventory-progress-fill" style={{ width: '91%' }}></div>
                    </div>
                    <span style={{ fontSize: '0.8rem', display: 'block', marginTop: '6px' }}>91% Stock Capacity</span>
                </div>
                <div className="panel-card">
                    <h3>Plant Monterrey</h3>
                    <p style={{ fontSize: '0.85rem', color: 'var(--text-secondary)' }}>Status: Optimal</p>
                    <div className="inventory-progress-bar">
                        <div className="inventory-progress-fill" style={{ width: '65%' }}></div>
                    </div>
                    <span style={{ fontSize: '0.8rem', display: 'block', marginTop: '6px' }}>65% Stock Capacity</span>
                </div>
            </div>

            <div className="panel-card">
                <h3>Warehouse Storage Allocation Schematics</h3>
                <p style={{ color: 'var(--text-secondary)', fontSize: '0.9rem' }}>Current structural distribution framework layout:</p>
                <div className="warehouse-grid">
                    <div className="warehouse-slot"><strong>Zone A-1</strong><br />Electronics</div>
                    <div className="warehouse-slot"><strong>Zone A-2</strong><br />Electronics</div>
                    <div className="warehouse-slot"><strong>Zone B-1</strong><br />Chassis Assembly</div>
                    <div className="warehouse-slot"><strong>Zone B-2</strong><br />Fasteners</div>
                    <div className="warehouse-slot"><strong>Zone C-1</strong><br />Raw Poly</div>
                    <div className="warehouse-slot"><strong>Zone C-2</strong><br />Packaging</div>
                </div>
            </div>
        </div>
    );
};

export default PlantsInventory;