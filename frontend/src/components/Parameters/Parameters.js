import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import './Parameters.css';

function Parameters() {

  const [clickedButtons, setClickedButtons] = useState({});

  const handleButtonClick = (group, buttonName) => {
    // Toggle clicked state
    setClickedButtons({ ...clickedButtons, [group]: buttonName });
  };

  const handleTrain = () => {
    axios.post('http://localhost:5000/train', clickedButtons);
  };

  return (
    <div style={{textAlign: 'center', padding: '20px'}}>
      <h1>What parameters would you like for your model?</h1>
        <p>Select the parameters you would like to use to train your model</p>
    
        <div class='param-grid-container'>

            {/* <div class='hidden-layers'>

            </div> */}


            <div class='layer1-container'>
                <h2 class='layer1'>Layer 1</h2>
                <text class='layer1_txt'></text>
            </div>

            <div class='layer2-container'>
                <h2 class='layer2'>Layer 2</h2>
                <text class='layer2_txt'></text>
            </div>

            <div class='layer3-container'>
                <h2 class='layer3'>Layer 3</h2>
                <text class='layer3_txt'></text>
            </div>

            <div class='dropout-container'>
                <h2 class='dropout'>Dropout</h2>
                <text class='dropout_txt'></text>
            </div>

            <div class='learning-rate-container'>
                <h2 class='learning_rate'>Learning Rate</h2>
                <text class='learning_rate_txt'></text>
            </div>

            <div class='batch-size-container'>
                <h2 class='batch_size'>Batch Size</h2>
                <text class='batch_size_txt'></text>
            </div>


            <div class='activation-container'>
                
                <h2 class='activation_fx'>Activation Function</h2>
                <button 
                    class={clickedButtons.activation === 'relu' ? 'clicked' : 'relu'}
                    onClick={() => handleButtonClick('activation', 'relu')}
                >
                    ReLU
                </button>

                <button 
                    class={clickedButtons.activation === 'tanh' ? 'clicked' : 'tanh'}
                    onClick={() => handleButtonClick('activation', 'tanh')}
                >
                    Tanh
                </button>
            </div>

            <div class='loss-container'>
                <h2 class='loss_function'>Loss Function</h2>
                <button 
                    class={clickedButtons.loss === 'MSELoss' ? 'clicked' : 'MSELoss'}
                    onClick={() => handleButtonClick('loss', 'MSELoss')}
                >
                    MSELoss
                </button>

                <button 
                    class={clickedButtons.loss === 'BCELoss' ? 'clicked' : 'BCELoss'}
                    onClick={() => handleButtonClick('loss', 'BCELoss')}
                >
                    BCELoss
                </button>
            </div>

            <div class='optimizer-container'>
                <h2 class='optimizer'>Optimizer</h2>
                <button 
                    class={clickedButtons.optimizer === 'SGD' ? 'clicked' : 'SGD'}
                    onClick={() => handleButtonClick('optimizer', 'SGD')}
                >
                    SGD
                </button>
                
                <button 
                    class={clickedButtons.optimizer === 'Adam' ? 'clicked' : 'Adam'}
                    onClick={() => handleButtonClick('optimizer', 'Adam')}  
                >
                    Adam
                </button>
            </div>


            <div class='regularization-container'>
                <h2 class='regularization'>Regularization</h2>
                <button 
                    class={clickedButtons.regularization === 'L1' ? 'clicked' : 'L1'}
                    onClick={() => handleButtonClick('regularization', 'L1')}
                >
                    L1
                </button>
                
                <button 
                    class={clickedButtons.regularization === 'L2' ? 'clicked' : 'L2'}
                    onClick={() => handleButtonClick('regularization', 'L2')}
                >
                    L2
                </button>
            </div>


            <div class='batch-container'>
                <h2 class='batch_normalization'>Batch Normalization</h2>
                <button 
                    class={clickedButtons.batch === 'on' ? 'clicked' : 'batch_norm_toggle'}
                    onClick={() => handleButtonClick('batch', clickedButtons.batch === 'on' ? 'off' : 'on')}
                >
                    On/Off
                </button>
            </div>

            <button className='train-button' onClick={handleTrain}>Train Model</button>

        </div>

        

    </div>
  );
}

export default Parameters;