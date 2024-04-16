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
import logo from '../images/football.jpg';
import axios from 'axios';
import { useLocation, useNavigate } from 'react-router-dom'; // Import useNavigate instead of useHistory

const Navbar = () => {
  const [loggedIn, setLoggedIn] = useState(false);
  const navigate = useNavigate(); // Use useNavigate for navigation

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
  }, [useLocation().pathname]); // React hooks should be called at the top level

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
              Leaderboard
            </NavLink>
            <NavLink to='/searchmodels' activeStyle>
              Search Models
            </NavLink>
            {loggedIn ? (
              <NavLink to='/createmodel' activeStyle>
                Create Model
              </NavLink>
            ) : (
              <NavLink to='/createmodel' activeStyle>
                Create Model
              </NavLink>
            )}
            {loggedIn ? (
              <NavLink to='/savedmodels' activeStyle>
                Saved Models
              </NavLink>
            ) : (
              <NavLink to='/savedmodels' activeStyle>
                Saved Models
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
