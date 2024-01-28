import styled from 'styled-components'

export const AboutContainer = styled.div`
 color: #fff;
 background: ${({ lightBg }) => (lightBg ? '#101833 ' : '#ACD3DE ')};
 
 @media screen and (max-width: 768px) {
     padding: 200px 0;
 }
`;

export const AboutWrapper = styled.div`
 display: grid;
 z-index: 1;
 height: 938px;
 width: 100%;
 max-width: 1920px;
 margin-right: auto;
 margin-left: auto;
 padding: 0 30px;
 justify-content: center;
`;

export const AboutRow = styled.div`
 display: grid;
 grid-auto-columns: minmax(auto, 1fr);
 align-items: center;
 max-width: 1600px;
 grid-template-areas: ${({ imgStart }) =>
  imgStart ? `'col2 col1'` : `'col1 col2'`};

 @media screen and (max-width: 768px) {
     grid-template-areas: ${({ imgStart }) => 
     imgStart ? `'col1' 'col2'` : `'col1 col1' 'col2 col2'`};
 }
`;

export const Column1 = styled.div`
 margin-bottom: 15px;
 grid-area: col1;
 padding: 0 15px;

`

export const Column2 = styled.div`
 margin-bottom: 15px;
 padding: 0 15px;
 grid-area: col2;
`

export const TextWrapper = styled.div`
 width: 100%; 
 padding-top: 0;
 padding-bottom: 20px;
 align-items: center;
 justify-content: center;
`

export const Subtitle = styled.p`
 max-width: 100%;
 font-size: 18px; 
 line-height: 24px;
 color: ${({ darkText }) => (darkText ? '#F7F4EF ' : '#F7F4EF')};
`

export const ImgWrap = styled.div`
 max-width: 100%;
 height: 100%;
 align-items: center;
 padding-bottom: 50px;
`
export const Img = styled.img`
 align-items: center;
 width: 100%;
 margin: 0 0 50px 0;
 padding-right: 0;
 padding-bottom: px;
`;

export const AboutBanner = styled.img`
color: #F7F4EF;
justify-content: center;
display: flex;
align-items: center;
margin-left: auto;
margin-right: auto;
width: 60%;
min-width: 300px;
padding-bottom: 120px;
`;

export const Textbox = styled.div`
color: black;
background: rgba(226, 135, 180, 1);
padding: 12px 20px 20px 12px;
border-radius: 12px;  
justify-content: center;
margin-right: 15px;
margin-left: 15px;
`