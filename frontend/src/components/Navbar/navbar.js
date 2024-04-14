import React, {useEffect, useState} from 'react';
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
import { useLocation } from 'react-router-dom';


const Navbar = () => {
  
  const [loggedIn,setLoggedIn] = useState(false)
  const [userInfo,setUserInfo] = useState()

  let checkAuth = async () => {
    let response = await axios.get('http://localhost:3000/auth');
    console.log(response.status);
    if(response.status === 206)
    {
      console.log("alskdjf;lasdf");
      setLoggedIn(false);
      return false;
    }
    else
    {
      setLoggedIn(true);
      return true;
      
    }
  };
  
    const url = useLocation()
    useEffect(() => {
      checkAuth();
    },[url.pathname]);

  return (
    <>
      <Nav>
        <NavbarContainer>
        <NavLink to='/'>
          <NavLogo src={logo} to='/' />
        </NavLink>
        <Bars />
        <NavMenu>
          <NavLink to='/about' activeStyle>
            Leaderboard
          </NavLink>
          <NavLink to='/' activeStyle >
            Search Models
          </NavLink>
          {loggedIn ? (<NavLink to='/createmodel' activeStyle>
            Create Model
          </NavLink>) : (<NavLink  activeStyle>
            Create Model
          </NavLink>)}
        </NavMenu>
        <NavBtn>
          <NavBtnLink to='/signin'>Sign In</NavBtnLink>
        </NavBtn>
        {/* Temporary double button to handle sing up and sign in page */}
        <NavBtn>
          <NavBtnLink to='/signup'>Sign Up</NavBtnLink>
        </NavBtn>
        </NavbarContainer>
      </Nav>
    </>
  );
};

export default Navbar;