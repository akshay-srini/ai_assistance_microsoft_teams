import React from "react";
import SideNav from "./SideNav";
import ChatOverview from "./ChatOverview";
import MainChat from "./MainChat";
export default function MainContent() {
    return (
        <section className="mainContentContainer">
            <div className="sidenav-container">
                <SideNav />
            </div>
            <div className="chat-overview-section">
            <ChatOverview />
            </div>
            <div className="main-content-container">
            <MainChat />
            </div>

        </section>
    )
}