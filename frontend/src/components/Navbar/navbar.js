import React from 'react';
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

const Navbar = () => {
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
          <NavLink to='/' activeStyle>
            Search Models
          </NavLink>
          <NavLink to='/createmodel' activeStyle>
            Create Model
          </NavLink>
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