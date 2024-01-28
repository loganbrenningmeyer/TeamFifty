import React from 'react';
import './App.css';
import {BrowserRouter as Router, Routes, Route} from 'react-router-dom';
import Home from './pages';
import SigninPage from './pages/signin';
import RegisterPage from './pages/register';

function App() {
  return (
    <Router>
      <Routes>
          <Route exact path="/" element={<Home/>}  />
          <Route exact path="/register" element={<RegisterPage/>}  />
          <Route exact path="/signin" element={<SigninPage/>}  />
      </Routes>
    </Router>
  );
}

export default App;