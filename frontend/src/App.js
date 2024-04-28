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
import SavedModels from './components/SavedModels/savedmodel';
import Leaderboard from './components/Leaderboard/Leaderboard';
import SearchModels from './components/SearchModels/searchmodels';

function App() {
  return (
    
    <Router>
      <Navbar />
      <Routes>
        <Route exact path="/about" element={<Dashboard/>} />
        <Route exact path="/" element={<About/>} />
        <Route exact path="/model" element={<Model/>} />
        <Route exact path="/data" element={<Data/>} />
        <Route exact path="/signin" element={<SignIn/>} />
        <Route exact path="/signup" element={<SignUp/>} />
        <Route exact path="/savedmodels" element={<SavedModels/>} />
        <Route exact path="/parameters" element={<Parameters/>} />
        <Route exact path="/leaderboard" element={<Leaderboard/>} />
        <Route exact path="/createmodel" element={<Tabs/>} />
        <Route exact path="searchmodels" element={<SearchModels/>}/>
      </Routes>
    </Router>
  );
}

export default App;
