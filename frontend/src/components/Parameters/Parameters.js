import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import './Parameters.css';

function Parameters() {
  return (
    <div style={{textAlign: 'center', padding: '20px'}}>
      <h1>What parameters would you like for your model?</h1>
        <p>Select the parameters you would like to use to train your model</p>
    
        <div class='grid-container'>

            <div class='hidden-layers'>

            </div>


            <div class='col1-container'>
              
            </div>


            <div class='col2-container'>

                <h2 class='activation_fx'>Activation Fx</h2>
                <button class='sigmoid'>Sigmoid</button>
                <button class='relu'>Relu</button>
                <button class='tanh'>Tanh</button>
            
                <div class='loss_function'>
                    <h2>Loss Function</h2>
                </div>
                <button class='MSELoss'>MSELoss</button>
                <button class='BCELoss'>BCELoss</button>

                <div class='optimizer'>
                    <h2>Optimizer</h2>
                </div>
                <button class='SGD'>SGD</button>
                <button class='adam'>Adam</button>

                <div class='regularization'>
                    <h2>Regularization</h2>
                </div>
                <button class='L1'>L1</button>
                <button class='L2'>L2</button>

                <div class='batch_normalization'>
                    <h2>Batch Normalization</h2>
                </div>
                <button class='batch_norm_toggle'>On/Off</button>

            </div>

        </div>

        <button className='continue-button'>Continue</button>

    </div>
  );
}

export default Parameters;