import React, { useState } from 'react';
import axios from 'axios';
import './parameters_svm.css';

function SVMParameters() {
    const [inputValues, setInputValues] = useState({
    });
    const [output, setOutput] = useState({
      training_accuracy: [],
      validation_accuracy: [],
      validation_loss: [],
      accuracy: '',
      confusionMatrix: [],
      detailedReport: {}
    });

    const [inputValidity, setInputValidity] = useState({
      C: false,
      gamma: false
    });

    const handleInputChange = (event) => {
      const { name, value } = event.target;
      setInputValues({ ...inputValues, [name]: value });
      setInputValidity({ ...inputValidity, [name]: value.trim() !== '' });
    };

    const handleTrain = async () => {
      try {
        const isValid = Object.values(inputValidity).every(valid => valid);
        if(isValid){
          const response = await axios.post('http://localhost:5000/train_SVM', inputValues);
          setOutput({
          training_accuracy: response.data.training_accuracy,
          validation_accuracy: response.data.validation_accuracy,
          validation_loss: response.data.validation_loss,
          accuracy: response.data.accuracy,
          confusionMatrix: response.data.confusion_matrix,
          detailedReport: response.data.detailed_report
          });
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
      <div className="parameters-container">
        <div className="form-group">
          <label className="label">Kernel Type:</label>
          <select className="select" name="kernel" value={inputValues.kernel} onChange={handleInputChange}>
            <option value="linear">Linear</option>
            <option value="poly">Polynomial</option>
            <option value="rbf">RBF</option>
            <option value="sigmoid">Sigmoid</option>
          </select>
        </div>

        <div className="form-group">
          <label className="label">Regularization Parameter (C):</label>
          <input className="input"
            type="number"
            step="0.1"
            min="0.01"
            max="1000"
            name="C"
            value={inputValues.C || ''}
            onChange={handleInputChange}
            placeholder={'1'}
          />
        </div>

        <div className="form-group">
          <label className="label">Kernel Coefficient (gamma):</label>
          <input className="input"
            type="text"
            name="gamma"
            value={inputValues.gamma || ''}
            onChange={handleInputChange}
            placeholder={'(scale,auto,>0)'}
          />
        </div>

        <button className="button" onClick={handleTrain}>Train Model</button>

        <div className="results-container">
          <h2>Training Statistics</h2>
          <p>Training Accuracy: {output.training_accuracy}</p>
          <p>Validation Accuracy: {output.validation_accuracy}</p>
          <p>Validation Loss: {output.validation_loss}</p>
          <p>Accuracy: {output.accuracy}</p>
          <p>Precision: {output.detailedReport.precision}</p>
          <p>Recall: {output.detailedReport.recall}</p>
          <p>F1-Score: {output.detailedReport['f1-score']}</p>
        </div>

        <div className="results-container">
          <h2>Confusion Matrix</h2>
          <table className="matrix-table">
            <tbody>
              {output.confusionMatrix.map((row, i) => (
                <tr key={i}>
                  {row.map((cell, j) => (
                    <td key={j}>{cell}</td>
                  ))}
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    );
  }

  export default SVMParameters;