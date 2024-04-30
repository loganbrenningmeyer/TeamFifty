import React, { useState } from 'react';
import axios from 'axios';
import './Parameters.css';

function Parameters() {

  const [clickedButtons, setClickedButtons] = useState({});
  const [inputValues, setInputValues] = useState({});

  // Output
  const [trainOutput, setTrainOutput] = useState('');
  const [testOutput, setTestOutput] = useState('');

  const handleButtonClick = (group, buttonName) => {
    // Toggle clicked state
    setClickedButtons({ ...clickedButtons, [group]: buttonName });
  };

  const handleInputChange = (event) => {
    const { name, value } = event.target;
    setInputValues({ ...inputValues, [name]: value });
  };

  const handleTrain = async () => {
    setTrainOutput('Training model...')
    const response = await axios.post('http://localhost:5000/train', {...clickedButtons, ...inputValues});
    const { training_loss, training_accuracy, validation_loss, validation_accuracy } = response.data;
    setTrainOutput(`Training Loss: ${training_loss[training_loss.length-1]}, Training Accuracy: ${training_accuracy[training_accuracy.length-1]}`);
    setTestOutput(`Validation Accuracy: ${validation_accuracy[validation_accuracy.length-1]}`);
  };

  return (
    <div style={{textAlign: 'center', padding: '20px'}}>
      {/*<h1>What parameters would you like for your model?</h1>
        <p>Select the parameters you would like to use to train your model</p>*/}
    
        <div class='param-grid-container' style={{background: '#23272D'}}>

            <div class='layers-container' style={{background: '#191D21'}}>
                <h2 class='layers'>Neurons Per Hidden Layer</h2>
                <input
                    class="layers_txt"
                    type="text"
                    name="layers"
                    value={inputValues.layers || ''}
                    onChange={handleInputChange}
                />
            </div>

            <div class='dropout-container' style={{background: '#191D21'}}>
                <h2 class='dropout'>Dropout Rate</h2>
                <input
                    class="dropout_txt"
                    type="number"
                    step="0.1"
                    min="0"
                    max="1"
                    name="dropout_rate"
                    value={inputValues.dropout_rate || ''}
                    onChange={handleInputChange}
                />
            </div>

            <div class='learning-rate-container' style={{background: '#191D21'}}>
                <h2 class='learning_rate'>Learning Rate</h2>
                <input
                    class="learning_rate_txt"
                    type="number"
                    step="0.0001"
                    min="0.0001"
                    max="1"
                    name="learning_rate"
                    value={inputValues.learning_rate || ''}
                    onChange={handleInputChange}
                />
            </div>

            <div class='batch-size-container' style={{background: '#191D21'}}>
                <h2 class='batch_size'>Batch Size</h2>
                <input
                    class="batch_size_txt"
                    type="number"
                    step="1"
                    min="1"
                    max="100"
                    name="batch_size"
                    value={inputValues.batch_size || ''}
                    onChange={handleInputChange}
                />
            </div>


            <div class='activation-container' style={{background: '#191D21'}}>
                
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

            <div class='loss-container' style={{background: '#191D21'}}>
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

            <div class='optimizer-container' style={{background: '#191D21'}}>
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


            <div class='regularization-container' style={{background: '#191D21'}}>
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


            <div class='batch-container' style={{background: '#191D21'}}>
                <h2 class='batch_normalization'>Batch Normalization</h2>
                <button 
                    class={clickedButtons.batch === 'on' ? 'clicked' : 'batch_norm_toggle'}
                    onClick={() => handleButtonClick('batch', clickedButtons.batch === 'on' ? 'off' : 'on')}
                >
                    
                </button>
            </div>

            <button className='train-button' onClick={handleTrain}>Train Model</button>

            <div class='train-container' style={{background: '#191D21'}}>
                <h2 class='train'>Training Statistics</h2>
                <p>{trainOutput}</p>
            </div>

            <div class='test-container' style={{background: '#191D21'}}>
                <h2 class='test'>Validation Statistics</h2>
                <p>{testOutput}</p>
            </div>

        </div>

        

    </div>
  );
}

export default Parameters;