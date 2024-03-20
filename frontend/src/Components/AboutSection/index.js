import React from 'react'
import { AboutContainer, Textbox, AboutWrapper, AboutRow, Column1, Column2, TextWrapper, Subtitle, ImgWrap, Img, AboutBanner} from './AboutElements'
import AboutPic from '../../images/about.png'

const AboutSection = ({lightBg, id, imgStart, img, alt, }) => {
    return (
        <>
        <AboutContainer lightBg={lightBg} id={id}>
            <AboutWrapper>
                <AboutRow imgStart={imgStart}>
                    <Column1>
                    <TextWrapper>
                        <AboutBanner src={AboutPic} />
                        <Textbox><Subtitle>Subtitle text</Subtitle>
                        </Textbox>
                    </TextWrapper>
                    </Column1>
                    <Column2>
                     <ImgWrap>
                     <Img src={img} alt={alt} /> 
                    </ImgWrap>
                    </Column2>  
                </AboutRow>
            </AboutWrapper>
        </AboutContainer>
        </>
    );
}

export default AboutSection
