// import logo from './logo.svg';
import './App.css';
import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import About from './components/About';

function App() {
  return (
    <Router>
      <Routes>
        <Route exact path="/" element={<About/>} />
      </Routes>
    </Router>
  );
}

export default App;
