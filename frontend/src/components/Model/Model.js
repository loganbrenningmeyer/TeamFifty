import React, { useState } from 'react';
import axios from 'axios'; 
import { useNavigate } from 'react-router-dom';
import './Model.css';

function Model() {

  const navigate = useNavigate();
  const [selectedModel, setSelectedModel] = useState('');

  const handleButtonClick = (model) => {
    setSelectedModel(model);
  }

  // Removed for tab system
  // const handleContinue = () => {
  //   navigate('/data');
  // }

  return (
    <div className='bg'>
      <div className='modelcontainer'>
        <h1>Which model would you like to create?</h1>
        <p>Select the type of model you would like to customize</p>
        <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', margin: '20px'}}>
          <button
            className={`select-nn ${selectedModel === 'Neural Network' ? 'clicked' : ''}`}
            onClick={() => handleButtonClick('Neural Network')}>
            Neural Network
          </button>
          <button
            className={`select-nn ${selectedModel === 'Support Vector' ? 'clicked' : ''}`}
            onClick={() => handleButtonClick('Support Vector')}>
            Support Vector
          </button>
          <button
            className={`select-nn ${selectedModel === 'Gradient Boosting' ? 'clicked' : ''}`}
            onClick={() => handleButtonClick('Gradient Boosting')}>
            Gradient Boosting
          </button>
        </div>
        {/* <button className='continue-button' onClick={handleContinue}>Continue</button> */}
      </div>
    </div>
  );
}

export default Model;
