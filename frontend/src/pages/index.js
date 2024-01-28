import React, {useState} from 'react'
import Sidebar from '../Components/Sidebar'
import Navbar from '../Components/NavBar'
import HeroSection from '../Components/HeroSection'
import AboutSection from '../Components/AboutSection/index.js'
import {homeObjOne} from '../Components/AboutSection/Data'
import Footer from '../Components/Footer'
import Organizer from '../Components/Accordion2/Organizer'
import Products from '../Components/Plans/index'
import { productData } from '../Components/Plans/data'

const Home = () => {
 const [isOpen, setIsOpen] = useState(false)
 
 const toggle = () => {
     setIsOpen(!isOpen)
 } 

    return (
        <>
         <Sidebar isOpen={isOpen} toggle={toggle}/>
         <Navbar toggle={toggle} />
         <HeroSection />
         <AboutSection {...homeObjOne} />
         {/*<Products heading='Choose your plan' data={productData}/>*/}
       {/*  <DemoRarity /> */}
        {/*  <VideoMap /> */}
         <Organizer />
        {/* <Services /> */}
         <Footer />
        </>
    )
}

export default Home