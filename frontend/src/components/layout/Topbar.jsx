import React, { useState, useEffect } from "react";
// Absolute paths relative to project root
import maintenanceImg from "/src/assets/images/left.png";
import blueprintImg from "/src/assets/images/Right.png";
import "../../styles/topbar.css"

const Topbar = () => {
    // State to hold the current date/time object
    const [currentTime, setCurrentTime] = useState(new Date());

    useEffect(() => {
        // Set up a timer to update the clock every second
        const timer = setInterval(() => {
            setCurrentTime(new Date());
        }, 1000);

        // Clean up the interval when the component unmounts
        return () => clearInterval(timer);
    }, []);

    // Format options for the Time (e.g., "10:42 AM")
    const timeOptions = { hour: '2-digit', minute: '2-digit', hour12: true };
    const formattedTime = currentTime.toLocaleTimeString([], timeOptions);

    // Format options for the Date (e.g., "20 June 2026")
    const dateOptions = { day: 'numeric', month: 'long', year: 'numeric' };
    const formattedDate = currentTime.toLocaleDateString('en-GB', dateOptions);

    return (
        <header className="topbar">
            {/* BACKGROUND IMAGES */}
            <div className="topbar-bg-left">
                <img src={maintenanceImg} alt="" />
            </div>

            <div className="topbar-bg-right">
                <img src={blueprintImg} alt="" />
            </div>

            {/* LEFT SECTION - SYSTEM IDENTITY (Optimized short copy) */}
            <div className="topbar-left">

                <div className="system-status-group">
                    <div className="agent-status-indicator active">

                    </div>

                </div>
            </div>

            {/* CENTER SECTION - UNIFIED COMMAND DIRECTIVE (Condensed overview text) */}
            <div className="topbar-center">
                <p className="system-directive-statement">
                    Real-time monitoring of global logistics disruptions, inventory risks, and mitigation planning for cement operations.
                </p>
            </div>

            {/* RIGHT SECTION - METRICS & TELEMETRY */}
            <div className="topbar-right">
                <div className="telemetry-block border-right">
                    <span className="telemetry-label">LIVE TIME</span>
                    {/* Dynamic realistic time */}
                    <span className="telemetry-value text-glow">{formattedTime}</span>
                    {/* Dynamic realistic date */}
                    <span className="telemetry-subtext">{formattedDate}</span>
                </div>

                <div className="telemetry-block">
                    <span className="telemetry-label">SC HEALTH</span>
                    <span className="telemetry-value">96.8%</span>
                    <span className="telemetry-subtext">2s ago</span>
                    <div className="operational-status-tag">
                        <span className="pulse-dot"></span>
                        <span className="status-tag-text">AI MONITORING</span>
                    </div>
                </div>
            </div>
        </header>
    );
};

export default Topbar;