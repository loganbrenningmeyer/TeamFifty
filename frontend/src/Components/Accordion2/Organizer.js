import Accordion from './Accordion'
import TAccordion from './TogAccordion'
import React from 'react'
import { AccordianSection2, AccordianContainer, AccHeader, HeaderContainer, } from './AccorElements'
import AboutPic from '../../images/faq.png'

const Organizer = () => {
    return (
        
        <AccordianSection2 id='faq'>
            <HeaderContainer>
                        <AccHeader  src={AboutPic}></AccHeader>
            </HeaderContainer>
            <AccordianContainer>
    <TAccordion 
    title="Why should I buy?"
    content="Yep"/>
    <Accordion title="How does it work?"
    content="Placeholder"/>
    <Accordion title="What are the benefits?"
    content="Empty."/>
    <Accordion title="How do I buy?"
    content="Blank."/>
    <Accordion title="When is delivery?"
    content="Yippee!."/>
    </AccordianContainer>
</AccordianSection2>
    )
}

export default Organizer



