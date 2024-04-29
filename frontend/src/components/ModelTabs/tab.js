import { useState } from 'react';
import './tab.css';
import Model from '../Model/Model';
import Data from '../Data/Data';
import Parameters from '../Parameters/Parameters';
import axios from 'axios';
import SVMParameters from '../Parameters/parameters_svm'; 

function Tabs() {
    axios.defaults.withCredentials = true;

    const [toggleState, setToggleState] = useState(1);
    const [modelName,setModelName] = useState('');
    const [selectedModelType, setSelectedModelType] = useState(null); // State to store the selected model type
    const [feedback, setFeedback] = useState(''); // Correct

    const toggleTab = (index) => {
        setToggleState(index);
    }

    const handleModelSelect = (modelType) => {
        console.log(`Model selected: ${modelType}`);
        setSelectedModelType(modelType); // Update the selected model type
        setFeedback(`Model selected: ${modelType}`); // Set feedback message
    };

    const renderParametersComponent = () => {
        console.log(`Rendering parameters for: ${selectedModelType}`);
        switch (selectedModelType) {
            case 'ANN':
                return <Parameters />;
            case 'SVM':
                return <SVMParameters />;
            // Add cases for any other models you have
            default:
                return <div>Select a model to see parameters</div>;
        }
    };
    const handleModelSave = async () => {
        const response = await axios.post('http://localhost:5000/save',{'model name':modelName});

    }
    return (
    <div className="bg">
    

        <div className="container">

            <div className="bloc-tabs">
                <div className={toggleState === 1 ? "tabs active-tabs" : "tabs"}
                onClick={() => toggleTab(1)}
                >Model</div>
                <div 
                className={toggleState === 2 ? "tabs active-tabs" : "tabs"}
                onClick={() => toggleTab(2)}
                >Data</div>
                <div 
                className={toggleState === 3 ? "tabs active-tabs" : "tabs"}
                onClick={() => toggleTab(3)}
                >Parameters</div>
                
                <div 
                className={toggleState === 4 ? "tabs active-tabs" : "tabs"}
                onClick={() => toggleTab(4)}
                >Save Model</div>
            </div>
            
            <div className="content-tabs">
            
                <div className={toggleState === 1 ? "content active-content" : "content"} >
                    <Model onModelSelect={handleModelSelect} />
                </div>

                <div className={toggleState === 2 ? "content active-content" : "content"}>
                    <Data />
                </div>

                <div className={toggleState === 3 ? "content active-content" : "content"}>
                    {renderParametersComponent()}
                </div>

                <div className={toggleState === 4 ? "content active-content" : "content"}>
                    <h2>Train</h2>
                    <input type='text' name='model name' id='modelName' onChange={(e) => setModelName(e.target.value)}/>
                    <button onClick={handleModelSave}>Save</button>
                </div>

            </div>
        </div>
        </div>
    )
}

export default Tabs;