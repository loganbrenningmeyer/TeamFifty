import React from 'react';
import './App.css';
import {BrowserRouter as Router, Routes, Route} from 'react-router-dom';
import Home from './pages';
import SigninPage from './pages/signin';
import SignupPage from './pages/signup';
import RecoveryPage from './pages/recovery';
import DashboardPage from './pages/dashboard';

function App() {
  return (
    <Router>
      <Routes>
          <Route exact path="/" element={<Home/>}  />
          <Route exact path="/signin" element={<SigninPage/>}  />
          <Route exact path="/signup" element={<SignupPage/>}  />
          <Route exact path="/account-recovery" element={<RecoveryPage/>}  />
          <Route exact path='/dashboard' element={<DashboardPage/>} />
      </Routes>
    </Router>
  );
}

export default App;