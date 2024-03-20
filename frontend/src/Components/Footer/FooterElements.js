import styled from 'styled-components'
import {Link} from 'react-router-dom'

export const FooterContainer = styled.footer`
 background-color: #6D6270  ;
`

export const FooterWrap = styled.div`
 padding: 4px 80px;
 display: flex;
 flex-direction: column;
 justify-content: center;
 align-items: center;
 max-width: 1800px
 margin: 0 auto;
`

export const SocialMedia = styled.section`
 max-width: 1800;
 width: 100%;
`
export const SocialMediaWrap = styled.div`
display: flex;
 justify-content: space-between;
 align-items: center;
 max-width: 2444px;
 margin: 0px auto 10 auto;

  @media screen and (max-width: 820px) {
      flex-direction: column;
  }
`

export const SocialLogo = styled(Link)`
 color: #fff;
 justify-self: start;
 cursor: pointer;
 text-decoration: none;
 font-size: 1.25rem;
 display: flex;
 align-items: center;
 margin-bottom: 0px;
 font-weight: bold;
`

export const WebsiteRights = styled.small`
 color: #fff;
 margin-bottom: 0px;
`

export const SocialIcons = styled.div`
display: flex;
justify-content: space-between;
align-left: -50px;
align-items: center;
width: 140px;
`;

export const SocialIconLink = styled.a`
color: #BD5157;
font-size: 25px;
border-radius: 25px;

&:hover {
  transition: all 0.2s ease-in-out;
  background: rgba(255,255,255,0.4);
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
