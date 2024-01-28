import styled from 'styled-components';
import { Link as LinkS } from 'react-scroll';
import { Link as LinkR } from 'react-router-dom';
import { FaTimes } from 'react-icons/fa';

export const SidebarContainer = styled.aside`
position: fixed;
z-index: 999;
width: 100%;
height: 100%;
background: #F7D0D9 ;
display: grid;
align-items: center;
top: 0;
left: 0;
transition: 0.3s ease-in-out;
opacity: ${({ isOpen }) => (isOpen ? '100%' : '0')};
top: ${({ isOpen }) => (isOpen ? '0' : '-100%')};
`;

export const CloseIcon = styled(FaTimes)`
color: #fff;
`;

export const Icon = styled.div`
position: absolute;
top: 1.2rem;
right: 1.5rem;
background: transparent;
font-size: 2rem;
cursor: pointer;
outline: none;
`;

export const SidebarWrapper = styled.div`
 color: #F7D0D9;
`;

export const SidebarMenu = styled.ul`
 display: grid;
 grid-template-columns: lfr;
 grid-template-rows: repeat(6, 80px);
 text-align: center;

 @media screen and (max-width: 480px) {
     grid-template-rows: repeat(6, 60px);
}
`;

//text in sidebar
export const SidebarLink = styled(LinkS)`
display: flex;
align-items: center;
justify-content: center;
font-size: 1.5rem;
text-decoration: none;
list-style: none;
transition: 0.2s ease-in-out;
text-decoration: none;
color: #fff;
cursor: pointer;
text-shadow: -1px -1px 0 #000, 1px -1px 0 #000, -1px 1px 0 #000, 1px 1px 0 #000;

&:hover {
    color: #01bf71
    transition: 0.2s ease-in-out;
}
`;

export const SideBtnWrap = styled.div`
 display: flex;
 justify-content: center;
 `

 export const SidebarRoute = styled(LinkR)`
  border-radius: 50px;
  background: #01bf71;
  white-space: nowrap;
  padding: 16px 48px;
  color: #010606;
  font-size: 16px;
  outline: none;
  border: none;
  cursor: pointer;
  transition: all 0.2s ease-in-out;
  text-decoration: none;

  &:hover {
    transition: 0.2s ease-in-out; 
    background: #fff;
    color: #010606; 
 `;

 export const SocialIcons = styled.div`
 display: flex;
 justify-content: center;
 align-left: -50px;
 align-items: center;
 width: 10px;
`;

export const SocialIconLink = styled.a`
color: #BD5857;
align-items: center;
border-radius: 15px;
margin-left: auto;
margin-right: auto;
margin-bottom: 48px;
display: flex;

&:hover {
  transition: all 0.2s ease-in-out;
  background: rgba(0,0,0,0.3);
`;

export const FaOpenSea = styled.img`
 height: 30px;
 width: 60px; 
 margin-top: auto;
 margin-left: auto;
 margin-right: auto;
 margin-bottom: auto;
`

export const FTwitter = styled.img`
 height: 26px;
 width: 60px; 
 margin-top: auto;
 margin-left: auto;
 margin-right: auto;
 margin-bottom: auto;
`

export const FDiscord = styled.img`
 height: 26px;
 width: 60px; 
 margin-top: auto;
 margin-left: auto;
 margin-right: auto;
 margin-bottom: auto;
`
// fra

