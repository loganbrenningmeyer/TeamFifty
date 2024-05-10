import React, { useState } from 'react';
import axios from 'axios'; 
import { useNavigate } from 'react-router-dom';
import './Model.css';
import NNLogo from '../images/NeuralNetwork.svg';
import SVMLogo from '../images/SVM.svg';
import GBLogo from '../images/GB.svg';

function Model({ onModelSelect }) { // onModelSelect function passed as a prop
  // State to track the selected model
  const [selectedModel, setSelectedModel] = useState(null);

  // The handler now calls onModelSelect with the model type
  const handleButtonClick = (modelType) => {
    console.log('Model selected: ', modelType)
    setSelectedModel(modelType); // Update the state to highlight the button
    onModelSelect(modelType); // This will be handleModelSelection in Tabs.js
    console.log('Set model state', modelType)
  }

  // Removed for tab system
  // const handleContinue = () => {
  //   navigate('/data');
  // }

  return (
    //<div className='bg'>
      <div className='modelcontainer'>
        <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center'}}>
          <button
            className={`select-nn ${selectedModel === 'ANN' ? 'active' : ''}`}
            onClick={() => handleButtonClick('ANN')}> {/* Updated model type */}
            <img src={NNLogo} alt='NNLogo'/>
          </button>
          <button
            className={`select-nn ${selectedModel === 'SVM' ? 'active' : ''}`}
            onClick={() => handleButtonClick('SVM')}> {/* Updated model type */}
            <img src={SVMLogo} alt='SVMLogo'/>
          </button>
          <button
            className={`select-nn ${selectedModel === 'GB' ? 'active' : ''}`}
            onClick={() => handleButtonClick('GB')}> {/* Updated model type */}
            <img src={GBLogo} alt='GBLogo'/>
          </button>
        </div>
      </div>
    //</div>
  );
}

export default Model;
