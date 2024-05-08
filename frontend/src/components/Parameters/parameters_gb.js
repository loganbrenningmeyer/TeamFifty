import React, { useState } from 'react';
import axios from 'axios';
import './parameters_gb.css';

function GBParameters() {
    const [clickedButtons, setClickedButtons] = useState({
        max_features: 'null'
    });//[
    const [inputValues, setInputValues] = useState({
    });

    const [inputValidity, setInputValidity] = useState({
        n_estimators: false,
        max_depth: false,
        gb_learning_rate: false,
        subsample: false,
        min_samples_split:false,
        min_samples_leaf: false
      });

    // Output
    const [trainOutput, setTrainOutput] = useState('');
    const [testOutput, setTestOutput] = useState('');

    const handleInputChange = (event) => {
        const { name, value } = event.target;
        setInputValues({ ...inputValues, [name]: value });
        setInputValidity({ ...inputValidity, [name]: value.trim() !== '' });
    };

    const handleButtonClick = (group, buttonName) => {
        // Toggle clicked state
        setClickedButtons({ ...clickedButtons, [group]: buttonName });
    };

    const handleTrain = async () => {
        try {
            const isValid = Object.values(inputValidity).every(valid => valid);
            if (isValid){
                setTrainOutput('Training model...')
                const response = await axios.post('http://localhost:5000/train_GB', {...clickedButtons, ...inputValues});
                console.log(response);
                const { training_loss, training_accuracy, validation_loss, validation_accuracy } = response.data;
                setTrainOutput(`Training Loss: ${training_loss[training_loss.length-1].toFixed(3)}, Training Accuracy: ${(training_accuracy[training_accuracy.length-1]*100).toFixed(2)}%`);
                setTestOutput(`Validation Accuracy: ${(validation_accuracy[validation_accuracy.length-1]*100).toFixed(2)}%`);
            }
            else{
                alert('Please fill in all required fields.');
                return;
            }
        } catch (error) {
            console.error('Error during training:', error);
        }
    };

    return (
        <div style={{textAlign: 'center', padding: '20px'}}>
            <div class='gb-param-grid-container' style={{background: '#23272D'}}>

                <div class='n_estimators_container' style={{background: '#191D21'}}>
                    <h2 class='n_estimators'>Number of Estimators</h2>
                    <input
                        class="n_estimators_txt"
                        type="number"
                        min="1"
                        name="n_estimators"
                        value={inputValues.n_estimators || ''}
                        onChange={handleInputChange}
                        placeholder='100'
                    />
                </div>

                <div class='max_depth_container' style={{background: '#191D21'}}>

                    <h2 class='max_depth'>Maximum Depth</h2>
                    <input
                        class="max_depth_txt"
                        type="number"
                        min="1"
                        name="max_depth"
                        value={inputValues.max_depth || ''}
                        onChange={handleInputChange}
                        placeholder='3'
                    />
                </div>

                <div class='gb_learning_rate_container' style={{background: '#191D21'}}>
                    <h2 class='gb_learning_rate'>Learning Rate</h2>
                    <input
                        class="gb_learning_rate_txt"
                        type="number"
                        step="0.0001"
                        min="0.0001"
                        max="1"
                        name="gb_learning_rate"
                        value={inputValues.gb_learning_rate || ''}
                        onChange={handleInputChange}
                        placeholder='0.1'
                    />
                </div>

                <div class='subsample_container' style={{background: '#191D21'}}>
                    <h2 class='subsample'>Subsample</h2>
                    <input
                        class="subsample_txt"
                        type="number"
                        step="0.1"
                        min="0.1"
                        max="1"
                        name="subsample"
                        value={inputValues.subsample || ''}
                        onChange={handleInputChange}
                        placeholder='1.0'
                    />
                </div>

                <div class='min_samples_split_container' style={{background: '#191D21'}}>
                    <h2 class='min_samples_split'>Minimum Samples Split</h2>
                    <input
                        class="min_samples_split_txt"
                        type="number"
                        min="2"
                        name="min_samples_split"
                        value={inputValues.min_samples_split || ''}
                        onChange={handleInputChange}
                        placeholder='2'
                    />
                </div>

                <div class='min_samples_leaf_container' style={{background: '#191D21'}}>
                    <h2 class='min_samples_leaf'>Minimum Samples Leaf</h2>
                    <input
                        class="min_samples_leaf_txt"
                        type="number"
                        min="1"
                        name="min_samples_leaf"
                        value={inputValues.min_samples_leaf || ''}
                        onChange={handleInputChange}
                        placeholder='1'
                    />
                </div>

                <div class='max_features_container' style={{background: '#191D21'}}>

                    <h2 class='max_features'>Maximum Features</h2>

                    <button
                        class={clickedButtons.max_features === 'sqrt' ? 'clicked' : 'sqrt'}
                        onClick={() => handleButtonClick('max_features', 'sqrt')}
                    >
                        Sqrt
                    </button>

                    <button
                        class={clickedButtons.max_features === 'log2' ? 'clicked' : 'log2'}
                        onClick={() => handleButtonClick('max_features', 'log2')}
                    >
                        Log2
                    </button>

                    <button
                        class={clickedButtons.max_features === 'null' ? 'clicked' : 'null'}
                        onClick={() => handleButtonClick('max_features', 'null')}
                    >
                        None
                    </button>
                </div>

                <button class="gb-train-button" onClick={handleTrain}>Train Model</button>
                
                <div class='gb-train-container' style={{background: '#191D21'}}>
                    <h2 class='gb-train'>Training Statistics</h2>
                    <p>{trainOutput}</p>
                </div>

                <div class='gb-test-container' style={{background: '#191D21'}}>
                    <h2 class='gb-test'>Validation Statistics</h2>
                    <p>{testOutput}</p>
                </div>

            </div>
        </div>
    );
}

export default GBParameters;