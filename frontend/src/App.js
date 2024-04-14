// import logo from './logo.svg';
//import './App.css';
import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import About from './components/About/About';
import Home from './components/Home/Home';
import Model from './components/Model/Model';
import Data from './components/Data/Data';
import Parameters from './components/Parameters/Parameters';
import Dashboard from './components/Dashboard/Dashboard';
import Tabs from './components/ModelTabs/tab';
import Navbar from './components/Navbar/navbar';
import SignIn from './components/Signin';
import SignUp from './components/Signup';

function App() {
  return (
    
    <Router>
      <Navbar />
      <Routes>
        <Route exact path="/about" element={<About/>} />
        <Route exact path="/" element={<Dashboard/>} />
        <Route exact path="/model" element={<Model/>} />
        <Route exact path="/data" element={<Data/>} />
        <Route exact path="/signin" element={<SignIn/>} />
        <Route exact path="/signup" element={<SignUp/>} />
        <Route exact path="/parameters" element={<Parameters/>} />
        <Route exact path="/createmodel" element={<Tabs/>} />
      </Routes>
    </Router>
  );
}

export default App;
