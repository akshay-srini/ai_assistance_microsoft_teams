import React from "react";
import chatProfile from "../images/chat-profile.png";
import moreBlack from "../images/more-black.png";
import addGroup from "../images/add-group.png";
import call from "../images/telephone.png"
import Chatbot from "./Chabot"
export default function MainChat() {
    return (
        <section className="main-chat-section">
            <div className="chat-main-navigation">
                <div className="main-chat-heading active-chat">
                    <div className="help-container profile-img ">
                            <img src={chatProfile} alt="" />
                    </div>
                    <p className="spacing">AI assistance Chatbot</p>
                </div>               
                <div className="left-side flex">
                    <img src={call} alt="" className="main-content-icon-sizes"/>
                    <img src={addGroup} alt="" className="main-content-icon-size"/>
                    <img src={moreBlack} alt="" className="main-content-icon-size"/>
                </div>
            </div>
        <div className="chatbot-section">
            <Chatbot />
        </div>
    </section>
    );

}