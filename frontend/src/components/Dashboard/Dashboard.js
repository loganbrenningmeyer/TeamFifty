import React, { useState} from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import './Dashboard.css';

const ITEM_WIDTH = 1920;
 
function Dashboard(){
    const example = [1,2,3,4,5,6,7,8,9,10]

    const navigate = useNavigate();

    const [scrollPosition,setScrollPosition] = useState(0);

    //function to handle scrolling when the button is clicked
    const handleScroll = (scrollAmount) => {
        var slider = document.getElementById('slider');

        //calculates new scroll position
        const newScrollPos = scrollPosition + scrollAmount;

        //makes sure scroll value doesnt go over limit because we use the scroll amount to calculate index of model being looked at
        if(newScrollPos < 0 || newScrollPos > (ITEM_WIDTH * (example.length-1)))
        {

        }
        else
        {
            //updates the state with new scroll position
            setScrollPosition(newScrollPos);

            //access the container element and set its scrollLeft property
            slider.scrollLeft = newScrollPos;
        }

    };
    
    const handleLeaderboard = () => {
        //navigate('/leaderboard')
    }
    const handleSearchModels = () => {
        //navigate('/searchModels')
    }
    const handleCreateModel = () => {
        navigate('/model')
    }

    return(
    <div className='container'>
        <div className='header'>
            <div className='logo'>
                <img src={require('./football.jpg')} alt='Logo' width={45} height={38}/>
            </div>
            <button onClick={handleLeaderboard}>Leaderboard</button>
            <button onClick={handleSearchModels}>Search Models</button>
            <button onClick={handleCreateModel}>Create Model</button>
            <div className='account'> 
                <img src={require('./account.jpg')} alt='accountImage' width={45} height={38}/>
            </div>
        </div>
        <div className='action-buttons'>
            <button onClick={() =>handleScroll(-ITEM_WIDTH)}>Left</button>
            <button onClick={() => handleScroll(ITEM_WIDTH)}>Right</button>
        </div>
        <div id='slider' style={{
            width:"100vw",
            overflowX:"hidden",
            scrollBehavior:'smooth',
        }}>
            <div className='content-box'>
            { 
                example.map((item,index) => {
                    return(
                    <div className='entry' style={{backgroundColor:"lightblue"}}>
                    <p>{item} {scrollPosition}</p>
                    </div>
                    )
                })}
                <div className='lastElement'>
                    
                </div>
            </div>
        </div>
    </div>
    );
}

export default Dashboard;