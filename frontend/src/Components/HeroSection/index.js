import React, {useState} from 'react'
import { HeroContainer, HeroBg, VideoBg, HeroContent, HeroH1, HeroP, AboutRow, Column1, Column2, Herologo, HeroD, HeroGradient } from './HeroElements';
import { Provider } from 'react-redux'
import logo from '../../images/full_logo.png'

const HeroSection = () => {
    const [hover, setHover] = useState(false)

    const onHover = () => {
        setHover(!hover)
    }



    return (
        <HeroContainer id="home">
            <HeroBg>
            <HeroGradient />
  {/*               <VideoBg autoPlay loop muted src={Video} type='video/mp4' />*/}
            </HeroBg>
            {/* <AboutRow>
                <Column1 >
                <HeroH1>Cute Anime Girls</HeroH1>
                <HeroP>10,000 Randomly generated anime girls 0.08 ETH</HeroP>                    
                </Column1 >
                <Column2 >
                <Provider store={store}>
                    <App />
                </Provider>
                </Column2>
            </AboutRow> */}
            <HeroContent>
            <Herologo src={logo}></Herologo>
                <HeroD>Subtitle description text</HeroD>       
            </HeroContent>
        </HeroContainer>
        );
};

//Connect your wallet can be changed a lot look for normal import


export default HeroSection
