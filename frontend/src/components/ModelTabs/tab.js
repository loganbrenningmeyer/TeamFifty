import { useState } from 'react';
import './tab.css';
import Model from '../Model/Model';
import Data from '../Data/Data';
import Parameters from '../Parameters/Parameters';

function Tabs() {

    const [toggleState, setToggleState] = useState(1);

        const toggleTab = (index) => {
            setToggleState(index);
        }

    return (
    <div className="bg">
    

        <div className="container">

            <div className="bloc-tabs">
                <div className={toggleState === 1 ? "tabs active-tabs" : "tabs"}
                onClick={() => toggleTab(1)}
                >Model</div>
                <div 
                className={toggleState === 2 ? "tabs active-tabs" : "tabs"}
                onClick={() => toggleTab(2)}
                >Data</div>
                <div 
                className={toggleState === 3 ? "tabs active-tabs" : "tabs"}
                onClick={() => toggleTab(3)}
                >Parameters</div>
                
                {/* <div 
                className={toggleState === 4 ? "tabs active-tabs" : "tabs"}
                onClick={() => toggleTab(4)}
                >Train</div> */}
            </div>
            
            <div className="content-tabs">
            
                <div className={toggleState === 1 ? "content active-content" : "content"} >
                    <Model />
                </div>

                <div className={toggleState === 2 ? "content active-content" : "content"}>
                    <Data />
                </div>

                <div className={toggleState === 3 ? "content active-content" : "content"}>
                    <Parameters />
                </div>

                <div className={toggleState === 4 ? "content active-content" : "content"}>
                    <h2>Train</h2>
                    <hr />
                    <p>
                    Laggasgbnc,nbcvnbn 4
                 </p>
                </div>
            </div>
        </div>
        </div>
    )
}

export default Tabs;