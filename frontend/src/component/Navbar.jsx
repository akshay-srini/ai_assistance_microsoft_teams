import React from "react";
import search from "../images/search.png"
// import help from "../images/help.png"
// import leftArrow from "../images/left-arrow.png"
// import rightArrow from "../images/right-arrow.png"
// import clock from "../images/clock.png"
import more from "../images/more.png"
import me from "../images/me.png"

export default function mainPage() {
    return (
        <section className="navbar-section">
            <div className="navbar-container">
                <div className="navigation-menu">
                    <div className="red-close"></div>
                    <div className="yellow-min"></div>
                    <div className="green-full"></div>
                </div>
                <div className="prev-next-nav-search-combine-container">
                    <div className="prev-next-nav-components">
                        {/* <img src={leftArrow}></img> */}
                        {/* <img src={rightArrow}></img> */}
                        {/* <img src={clock}></img> */}
                    </div>
                    <div className="searchbar">
                        <img src={search}></img>
                        Search
                    </div>
                </div>
                <div className="flex">
                    <img src={more} alt="" className="more-container"/>
                    <div className="help-container profile-img ">
                        <img src={me} alt="" />
                        <div className="green-online"></div>
                    </div>
                </div>
                </div>

        
        </section>
    )
}