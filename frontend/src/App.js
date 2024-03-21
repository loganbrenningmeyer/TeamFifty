// import logo from './logo.svg';
import './App.css';
import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import About from './components/About/About';
import Home from './components/Home/Home';
import Model from './components/Model/Model';

function App() {
  return (
    <Router>
      <Routes>
        <Route exact path="/about" element={<About/>} />
        <Route exact path="/" element={<Home/>} />
        <Route exact path="/model" element={<Model/>} />
      </Routes>
    </Router>
  );
}

export default App;
