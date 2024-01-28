import React, {useState, useEffect} from 'react'
import { FaBars } from 'react-icons/fa'
import {Nav, NavbarContainer, NavLogo, MobileIcon, NavMenu, NavItem, NavLinks, NavBtn, NavBtnLink, SocialIconLink, FTwitter, FaOpenSea, FDiscord, } from './NavbarElements';
import {animateScroll as scroll} from 'react-scroll'
import TwitterSVG from '../../images/TwitterSVG.svg'
import DiscordSVG from '../../images/DiscordSVG.svg'
import Logo from '../../images/full_logo2.png'


const toggleHome = () => {
    scroll.scrollToTop();
};

const Navbar = ({ toggle }) => {
    const [scrollNav, setScrollNav] = useState(false)

    const changeNav = ()=> {
        if(window.scrollY >= 80) {
            setScrollNav(true)
        } else {
            setScrollNav(false)
        }

    }

    useEffect(() => {
        window.addEventListener('scroll', changeNav)
    }, [])

    return (
        <>
        <Nav scrollNav={scrollNav}>
            <NavbarContainer>
                <NavLogo src={Logo} to='/' onClick={toggleHome}
                duration={250} />
                <MobileIcon onClick={toggle}>
                    <FaBars />
                </MobileIcon >
                <NavMenu>
                    <NavItem>
                        <NavLinks to='about'
                        smooth={true}
                        duration={300}
                        spy={true}
                        exact='true'
                        offset={-50}
                        scrollNav={scrollNav}
                        >BLANK</NavLinks>
                    </NavItem>
                    <NavItem>
                        <NavLinks to='rarity'
                        smooth={true}
                        duration={300}
                        spy={true}
                        exact='true'
                        offset={-50}
                        scrollNav={scrollNav}
                        >BLANK</NavLinks>
                    </NavItem>
                    <NavItem>
                        <NavLinks to='roadmap'
                        smooth={true}
                        duration={300}
                        spy={true}
                        exact='true'
                        offset={-50}
                        scrollNav={scrollNav}
                        >BLANK</NavLinks>
                    </NavItem>
                    <NavItem>
                        <NavLinks to='faq'
                        smooth={true}
                        duration={300}
                        spy={true}
                        exact='true'
                        offset={-50}
                        scrollNav={scrollNav}
                        >Blank</NavLinks>
                    </NavItem>
                    <NavItem>
                        <NavLinks to='team'
                        smooth={true}
                        duration={300}
                        spy={true}
                        exact='true'
                        offset={-50}
                        scrollNav={scrollNav}
                        >BLANK</NavLinks>
                    </NavItem>
                </NavMenu>
                <NavBtn>
                            <SocialIconLink href='//twitter.com/' target='_blank'
                            aria-label='Twitter'>
                                <FTwitter src={TwitterSVG} />
                            </SocialIconLink>
                            <SocialIconLink href='//discord.gg/' target='_blank'
                            aria-label='Discord'>
                                <FDiscord src={DiscordSVG} />
                            </SocialIconLink>
                            <NavBtnLink to="/register">Register</NavBtnLink>

                            <NavBtnLink to="/signin">Sign In</NavBtnLink>
                </NavBtn>
            </NavbarContainer>          
        </Nav>
        </>
    );
};

export default Navbar
