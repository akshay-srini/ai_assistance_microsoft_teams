import React from "react";
import bellRing from "../images/bell-ring.png";
import group from "../images/group.png";
import chat from "../images/chat.png";
import calender from "../images/calendar.png";
import help from "../images/help.png";
import download from "../images/download.png";

export default function SideNav() {
    return (
        <div className="sidenav-section">
            <div className="navigators-section">
            <div className="icon-container">
                <img src={bellRing} alt="" className="icon-size"/>
                <p>Activity</p>
            </div>
            <div className="icon-container ">
            <img src={group} alt="" className="icon-size"/>
                <p>Teams</p>
            </div>
            <div className="icon-container active">
            <img src={chat} alt="" className="icon-size"/>
                <p>Chat</p>
            </div>
            <div className="icon-container">
            <img src={calender} alt="" className="icon-size"/>
                <p>Calendar</p>
            </div>
        </div>
        <div className="help-section">
        <div className="icon-container">
            <img src={help} alt="" className="icon-size"/>
                <p>help</p>
            </div>
            <div className="download-icon-container icon-container">
            <img src={download} alt="" className="icon-size"/>
            </div>
        </div>
        
            
            
        </div>
    )
}