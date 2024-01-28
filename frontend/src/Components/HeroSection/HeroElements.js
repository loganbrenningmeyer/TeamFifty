import styled from 'styled-components'
 
export const HeroContainer = styled.div`
background: #F7D0D9;
display: flex;
justify-content: center;
align-items: center;
height: 100vh;
width: 100%;
padding: 0 30px;
position: relative;
z-index: 1;

:before {
    content: '';
    postition: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: linear-gradient(180deg, rgba(0,0,0,0.2) 0%, rgba(0,0,0,0.6) 100%), linear-gradient(180deg, rgba(0,0,0,0.2) 0%, transparent 100%)
    z-index: 2

}
`
// ^add before styles
//^^also made darker at 1:40:30

export const HeroBg = styled.div`
 position: absolute;
 top: 0;
 right: 0;
 bottom: 0;
 left: 0;
 width: 100%;
 height: 100%;
 overflow: hidden;
 object-fit: cover;
`;

export const VideoBg = styled.video`
 width: 100%;
 height: 100%;
 -o-object-fit: cover;
 object-fit: cover;
 background: #F7D0D9;
`

export const HeroContent = styled.div`
 z-index: 3;
 max-width: 1920px;
 position: absolute;
 padding: 8 24px;
 display: flex;
 flex-direction: column;
 align-items: center;
`;

export const HeroH1 = styled.h1`
 color: #fff;
 font-size: 48px;
 text-align: center;

@media screen and (max-width: 768px) {
    font-size: 40px;
}

@media screen and (max-width: 768px) {
    font-size: 40px;
}
@media screen and (max-width: 480pc) {
    font-size: 32px;
}    
`
//text on video
export const HeroP = styled.p`
margin-top: 24px;
color: #fff;
font-size: 24px;
text-align: center;
max-width: 600px;

@media screen and (max-width: 768px) {
    font-size: 24px;
 }

@media screen and (max-width: 480pc) {
    font-size: 18px;
 }    
`

export const HeroD = styled.p`
margin-top: 24px;
color: #6D6470;
font-size: 5rem;
text-align: center;
max-width: 60%;
line-height: 1.4;
font-weight: 600;

@media screen and (max-width: 768px) {
    font-size: 24px;
 }

@media screen and (max-width: 480pc) {
    font-size: 18px;
 }    
`
 
//frankenstein below:

export const AboutRow = styled.div`
 z-index: 3;
 max-width: 1920px;
 position: absolute;
 padding: 8 24px;
 display: flex;
 flex-direction: column;
 align-items: center;
 display: grid;
 grid-auto-columns: minmax(auto, 1fr);
 align-items: center;
 grid-template-areas: 'col1 col2';

 @media screen and (max-width: 768px) {
     grid-template-areas: 'col1 col1' 'col2 col2';
 }
`;

export const Column1 = styled.div`
 margin-bottom: 15px;
 padding: 0 15px;
 grid-area: col1;
`

export const Column2 = styled.div`
 margin-bottom: 15px;
 padding: 0 15px;
 grid-area: col2;
`

export const Herologo = styled.img`
width: 80%;
margin: 0 0 10px 0;
padding-right: 0;
`

export const HeroGradient = styled.div`
position: absolute;
z-index: 5;
width: 100%;
bottom: 0px;
height: 100px;
width: 100%;
background:linear-gradient(0deg, rgba(247,208,214,50),transparent);
  background-color: transparent;
`