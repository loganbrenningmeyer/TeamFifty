import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import './Home.css';

function Home() {

  const navigate = useNavigate();

  const handleButtonClick = () => {
    navigate('/createmodel');
  }

  return (
    <h1>Hello World!</h1>
    /*
    <div style={{textAlign: 'center', padding: '20px'}}>
      <h1>Ballgorithm</h1>
      <p>Create custom machine learning sports models</p>
      <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', margin: '20px'}}>
        <button className='create-model' onClick={handleButtonClick}>Create Model</button>
      </div>
    </div>
    */
  );
}

export default Home;