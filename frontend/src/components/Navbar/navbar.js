import React, { useEffect, useState } from 'react';
import {
  Nav,
  NavLink,
  Bars,
  NavMenu,
  NavBtn,
  NavBtnLink,
  NavLogo,
  NavbarContainer
} from './navbarElements';
import logo from '../images/Logo.svg';
import LeaderboardLogo from '../images/Leaderboards.svg';
import SearchLogo from '../images/Search.svg';
import CreateLogo from '../images/Create.svg';
import SavedLogo from '../images/Saved.svg';
import axios from 'axios';
import { useLocation, useNavigate } from 'react-router-dom'; // Import useNavigate instead of useHistory

const Navbar = () => {
  const [loggedIn, setLoggedIn] = useState(false);
  const navigate = useNavigate(); // Use useNavigate for navigation
  const location = useLocation(); // Define location here

  const checkAuth = async () => {
    try {
      let response = await axios.get('http://localhost:3000/auth');
      if (response.status === 206) {
        setLoggedIn(false);
      } else {
        setLoggedIn(true);
      }
    } catch (error) {
      console.error('Authentication check failed:', error);
      setLoggedIn(false);
    }
  };

  useEffect(() => {
    checkAuth();
  }, [location.pathname]); // React hooks should be called at the top level

  const handleSignOut = async () => {
    try {
      await axios.get('http://localhost:3000/logout'); // Assuming your backend has a logout endpoint
      setLoggedIn(false);
      navigate('/signin'); // Use navigate to redirect to sign-in page after logging out
    } catch (error) {
      console.error('Logout failed:', error);
    }
  };

  return (
    <>
      <Nav>
        <NavbarContainer>
          <NavLink to='/'>
            <NavLogo src={logo} />
          </NavLink>
          <Bars />
          <NavMenu>
            <NavLink to='/leaderboard' activeStyle>
              <img src={LeaderboardLogo} alt='LeaderboardLogo' style={{height: '75%'}}/>
            </NavLink>
            <NavLink to='/searchmodels' activeStyle>
              <img src={SearchLogo} alt='SearchLogo' style={{height: '80%'}}/>
            </NavLink>
            {loggedIn ? (
              <NavLink to='/createmodel' activeStyle>
                <img src={CreateLogo} alt='CreateLogo' style={{height: '65%'}}/>
              </NavLink>
            ) : (
              <NavLink activeStyle>
                
              </NavLink>
            )}
            {loggedIn ? (
              <NavLink to='/savedmodels' activeStyle>
                <img src={SavedLogo} alt='SavedLogo' style={{height: '50%'}}/>
              </NavLink>
            ) : (
              <NavLink activeStyle>
                
              </NavLink>
            )}
          </NavMenu>
          <NavBtn>
            {loggedIn ? (
              <NavBtnLink as="button" onClick={handleSignOut}>Log Out</NavBtnLink> // Use as="button" if NavBtnLink renders a link by default
            ) : (
              <NavBtnLink to='/signin'>Sign In</NavBtnLink>
            )}
          </NavBtn>
        </NavbarContainer>
      </Nav>
    </>
  );
};

export default Navbar;
