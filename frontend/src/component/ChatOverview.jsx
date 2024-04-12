import React from "react";
import sort from "../images/sort.png";
import video from "../images/video.png";
import edit from "../images/edit.png";
import down from "../images/down.png";
import chatProfile from "../images/chat-profile.png";

export default function ChatOverview() {
    return (
        <section className="chatOverview-section">
            <div className="chat-overview-navigation">
                <h3>Chat</h3>                
                <div className="left-side flex">
                    <img src={sort} alt="" className="icon-size"/>
                    <div className="circular-icon-container">
                        <img src={video} alt="" className="icon-size"/>
                    </div>
                    <div className="circular-icon-colored-container">
                        <img src={edit} alt="" className="icon-sizes"/>
                    </div>
                </div>
            </div>
            <div className="chat-section">
                <div className="recent-container">
                    <img src={down} alt="" className="down-icon-container"/>
                    <p>recent</p>
                </div>
                <div className="individual-chat-container active-chat">
                    <div className="help-container profile-img ">
                            <img src={chatProfile} alt="" />
                    </div>
                    <p>AI assistance Chatbot</p>
                </div>
                <div className="individual-chat-container">
                    <div className="help-container profile-img ">
                            <img src={chatProfile} alt="" />
                    </div>
                    <p>AI assistance Chatbot demo 1</p>
                </div>
                <div className="individual-chat-container">
                    <div className="help-container profile-img ">
                            <img src={chatProfile} alt="" />
                    </div>
                    <p>AI assistance Chatbot demo 2</p>
                </div>
                

            </div>
        </section>
    );
}