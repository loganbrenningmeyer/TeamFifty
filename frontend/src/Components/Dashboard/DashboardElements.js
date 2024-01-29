import styled from 'styled-components'
 
export const DashboardContainer = styled.div`
background: gray;
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

export const DashboardBg = styled.div`
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