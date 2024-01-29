import React from 'react';
import './App.css';
import {BrowserRouter as Router, Routes, Route} from 'react-router-dom';
import Home from './pages';
import SigninPage from './pages/signin';
import SignupPage from './pages/signup';
import RecoveryPage from './pages/recovery';

function App() {
  return (
    <Router>
      <Routes>
          <Route exact path="/" element={<Home/>}  />
          <Route exact path="/signin" element={<SigninPage/>}  />
          <Route exact path="/signup" element={<SignupPage/>}  />
          <Route exact path="/account-recovery" element={<RecoveryPage/>}  />
      </Routes>
    </Router>
  );
}

export default App;