import React, { useState } from 'react';
import axios from 'axios';
import './parameters_svm.css';

function SVMParameters() {
    const [inputValues, setInputValues] = useState({
      kernel: 'rbf', // Default kernel type
      C: 1.0,        // Default C value
      gamma: '(scale,auto,>0)' // Default gamma value
    });
    const [output, setOutput] = useState({
      accuracy: '',
      confusionMatrix: [],
      detailedReport: {}
    });

    const handleInputChange = (event) => {
      const { name, value } = event.target;
      setInputValues({ ...inputValues, [name]: value });
    };

    const handleTrain = async () => {
      try {
        const response = await axios.post('http://localhost:5000/train_SVM', inputValues);
        setOutput({
          accuracy: response.data.accuracy,
          confusionMatrix: response.data.confusion_matrix,
          detailedReport: response.data.detailed_report
        });
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
            value={inputValues.C}
            onChange={handleInputChange}
          />
        </div>

        <div className="form-group">
          <label className="label">Kernel Coefficient (gamma):</label>
          <input className="input"
            type="text"
            name="gamma"
            value={inputValues.gamma}
            onChange={handleInputChange}
          />
        </div>

        <button className="button" onClick={handleTrain}>Train Model</button>

        <div className="results-container">
          <h2>Training Statistics</h2>
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