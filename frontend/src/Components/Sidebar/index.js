import React from 'react'
import { 
    SidebarContainer, 
    Icon, 
    CloseIcon, 
    SidebarWrapper, 
    SidebarMenu, 
    SidebarLink, 
    SideBtnWrap, 
    SocialIconLink,
    FTwitter,
    FDiscord,
    SidebarRoute
} from './SidebarElements';
import TwitterSVG from '../../images/TwitterSVG.svg'
import DiscordSVG from '../../images/DiscordSVG.svg'

const Sidebar = ({ isOpen, toggle }) => {
    return (
        <SidebarContainer isOpen={isOpen} onClick={toggle}>
            <Icon onClick={toggle}>
                <CloseIcon />
            </Icon>
            <SidebarWrapper>
                
                <SidebarMenu>
                    <SidebarLink to="about" onClick={toggle}
                                                                
                                                                exact='true'
                                                                offset={+100}
                    >REGISTER</SidebarLink>
                    <SidebarLink to="" onClick={toggle}
                                                                
                                                                exact='true'
                                                                offset={+0}
                    >BLANK</SidebarLink>
                    <SidebarLink to="" onClick={toggle}
                                                                
                                                                exact='true'
                                                                offset={+0}>BLANK</SidebarLink>
                    <SidebarLink to="faq" onClick={toggle}
                                            
                                            exact='true'
                                            offset={+0}
                    >BLANK</SidebarLink>
                    <SidebarLink to="team" onClick={toggle}                         
                     
                        exact='true'
                        offset={+300}
                        >BLANK</SidebarLink>
            <SocialIconLink href='//twitter.com/' target='_blank' aria-label='Twitter'>
                <FTwitter src={TwitterSVG} />
            </SocialIconLink>
                                    <SocialIconLink href='//discord.gg/' target='_blank'aria-label='Discord'>
                                        <FDiscord src={DiscordSVG} />
                                    </SocialIconLink>



                </SidebarMenu>
                <SideBtnWrap>
                <SidebarRoute to="/register">Register</SidebarRoute>
                    <SidebarRoute to="/signin">Sign In</SidebarRoute>
                </SideBtnWrap>
            </SidebarWrapper>
        </SidebarContainer>
    )
}

export default Sidebar
