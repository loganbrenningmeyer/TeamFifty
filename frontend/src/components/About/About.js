import React, { useState } from 'react';
import axios from 'axios';
import './About.css';


function About() {

  const [data, setData] = useState(null);
  
  const handleButtonClick = async () => {
    try {
        const response = await axios.get('http://localhost:5000/test');
        setData(response.data.result);
    } catch (error) {
        console.error(error);
    }
  };

  return (
    <div>
      <h1>About Page</h1>
      <p>This is the About page of my React app.</p>
      <button className='create-model' onClick={handleButtonClick}>Create Model</button>
      {data && <p>Result from Python: {data}</p>}
    </div>
  );
}

export default About;