import React, { useState } from 'react';
import axios from 'axios'; 
import { useNavigate } from 'react-router-dom';
import './Model.css';

function Model({ onModelSelect }) { // onModelSelect function passed as a prop
  // The handler now calls onModelSelect with the model type
  const handleButtonClick = (modelType) => {
    console.log('Model selected: ', modelType)
    onModelSelect(modelType); // This will be handleModelSelection in Tabs.js
    console.log('Set model state', modelType)
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
            className="select-nn"
            onClick={() => handleButtonClick('ANN')}> {/* Updated model type */}
            Neural Network
          </button>
          <button
            className="select-nn"
            onClick={() => handleButtonClick('SVM')}> {/* Updated model type */}
            Support Vector
          </button>
          <button
            className="select-nn"
            onClick={() => handleButtonClick('GradientBoosting')}> {/* Updated model type */}
            Gradient Boosting
          </button>
        </div>
      </div>
    </div>
  );
}

export default Model;
