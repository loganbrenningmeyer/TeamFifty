import styled from 'styled-components'
import {Link as LinkS} from 'react-scroll'
import {Link as LinkR} from 'react-router-dom'


//for transparent nav bar change second pink to 'transparent'
export const Nav = styled.nav`
 background: ${({ scrollNav }) => (scrollNav ? '#F7D0D9' : '#transparent')};
 height: 50px;
 margin-top: -50px;
 display: flex;
 justify-content: center;
 align-items: center;
 font-size: 1rem;
 position: sticky;
 top: 0;
 z-index: 10;

 transition: 0.5s all ease;

@media screen and (max-width: 960px) {
    transition: 0.8s all ease;

}
`;

export const NavbarContainer = styled.div`
 display: flex;
 justify-content: space-between;
 height: 50px;
 z-index: 1;
 width: 100%;
 padding: 0 24px;
 max-width: 1800px;
`;

export const NavLogo = styled.img`
color: #F7F4EF;
justify-self: flex-Start;
cursor: pointer;
display: flex;
font-size: 1rem;
align-items: center;
margin-left: 24px;
font-weight: bold;
text-decoration: none;
height: 90%;
margin-top: 2px;
`;

//three bar icons
export const MobileIcon = styled.div`
display: none;

@media screen and (max-width: 768px) {
    display: block;
    position: absolute;
    top: -12px;
    right: 0;
    transform: translate(-100%, 60%);
    font-size: 1.8rem;
    cursor: pointer;
    color: #6D6470;
}
`

export const NavMenu = styled.ul`
display: flex;
align-items: center;
list-style: none;
text-align: center;
margin-right: -22px;

 @media screen and (max-width: 768px) {
    display: none;
 }
`

export const NavItem = styled.li`
 height: 50px;
`

//these are the header buttons
export const NavLinks = styled(LinkS)`
 color: ${({ scrollNav }) => (scrollNav ? '#5E577B  ' : '#F7F4EF')};
 display: flex;
 align-items: center;
 text-decoration: none;
 padding: 0 1rem;
 height: 100%;
 cursor: pointer;
 font-weight: bold;
 font-size: 1rem;
 text-shadow: ${({ scrollNav }) => (scrollNav ? '' : '-1px -1px 0 #000, 1px -1px 0 #000, -1px 1px 0 #000, 1px 1px 0 #000')};
 transition: 0.5s all ease;

 &.active {
    border-bottom: 4px solid #CBF2FD;
 }
`;


export const NavBtn = styled.nav`
 display: flex;
 align-items: center;

 @media screen and (max-width: 768px) {
    display: none;
 }
`

//below is sign in button

export const SocialIcons = styled.div`
 display: flex;
 justify-content: space-between;
 align-left: -50px;
 align-items: center;
 width: 140px;
`;

export const SocialIconLink = styled.a`
 color: #BD5857;
 font-size: 25px;
 border-radius: 25px;

 &:hover {
   transition: all 0.2s ease-in-out;
   background: rgba(0,0,0,0.4);
`;

export const FaOpenSea = styled.img`
 height: 26px;
 width: 50px; 
 margin-bottom: -5px;
`

export const FTwitter = styled.img`
 height: 24px;
 width: 50px; 
 margin-bottom: -4px;
`

export const FDiscord = styled.img`
 height: 24px;
 width: 50px; 
 margin-bottom: -4px;
`

export const NavBtnLink = styled(LinkR)`
   border-radius: 50px;
   background: #01bf71;
   white-space: nowrap;
   padding: 10px 22px;
   color: #010606;
   font-size: 16px;
   outline: none;
   border: none;
   cursor: pointer;
   transition: all 0.2s ease-in-out;
   text-decoration: none;

   &:hover {
      transition: all 0.2s ease-in-out;
      background: #fff;
      color: #010606;
}
`