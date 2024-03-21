import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import './Model.css';

function Model() {

  const navigate = useNavigate();
  const [isClicked, setIsClicked] = useState(false);

  const handleButtonClick = () => {
    // Toggle clicked state
    setIsClicked(!isClicked);
  }

  const handleContinue = () => {
    navigate('/data');
  }

  return (
    <div style={{textAlign: 'center', padding: '20px'}}>
      <h1>Which model would you like to create?</h1>
      <p>Select the type of model you would like to customize</p>
      <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', margin: '20px'}}>
        <button className={`select-nn ${isClicked ? 'clicked' : ''}`} onClick={handleButtonClick}>Neural Network</button>
      </div>
      <button className='continue-button' onClick={handleContinue}>Continue</button>
    </div>
  );
}

export default Model;