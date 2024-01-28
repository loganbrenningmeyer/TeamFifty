import styled from 'styled-components'

export const AccordianSection2 = styled.div`
 display: flex;
 flex-direction: column;
 align-items: center;
 position: relative;
 height: 100%;
 background: #F7D0D9;
 transition: all 0.4s ease;
 
 @media screen and (min-width: 768px) {
    display: flex;
    min-height: 800px;

 @media screen and (max-width: 768px) {
    display: flex;
    min-height: 100px;
`;


export const AccordianContainer = styled.div` 
 width: 100%;
 max-width: 768px;
 margin: 0 auto;
 padding-top: 90px;
 font-size: 1rem;
 transition: all 0.4s ease;

`;

export const HeaderContainer = styled.div`
width: 100%;
height: 200px;
display: flex; 
`

export const AccHeader = styled.img`
display: flex;
margin-left: auto;
margin-right: auto;
margin-bottom: 75px;
margin-top: 100px;
height: 65%;
min-height: 30px;
`