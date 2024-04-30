import React, { useState } from 'react';
import axios from 'axios';
import './About.css';
import { Img } from './AboutElements';
import squid from '../images/brady.jpg';

function About() {
  return (

    <div className="flex relative justify-center h-[1000px] lg:h-[970px] bg-bg-grey" id="Landing">
      <div className="bottom-0 absolute z-[2] translate-y-[6.9px] select-none">
        {/* <Image quality={100} priority={true} src={bg}/> */}
      </div>
      <div className="z-[4] grid grid-cols-1 h-[900px] lg:grid-cols-2 gap-0 lg:gap-20">
        <div className="mx-auto mt-20 xs:mt-32 lg:m-auto w-[200px] xs:w-[300px] sm:w-[400px] md:w-[400px] lg:w-[580px] xl:w-[650px] flex justify-center drop-shadow-[15px_10px_10px_rgba(0,0,0,0.4)]">
          <div>
            <Img src={squid} />
          </div>
        </div>
        <div className="m-auto px-10 lg:p-0 flex flex-col text-white">
          <div className="m-auto lg:m-0 text-4xl lg:text-7xl text-center lg:text-left font-bold pb-8">Play Ball</div>
          <div className="max-w-[700px] text-center lg:text-left text-md xs:text-lg lg:text-2xl pb-8">Ballgorithm is a public platform for creating/sharing custom sports betting machine learning models</div>
          <div className="hidden lg:block max-w-[700px] text-center lg:text-left text-md xs:text-lg lg:text-2xl pb-8">To get started you can hit the sign up button below or log in above.</div>
          <div className="grid xs:block gap-5 xs:gap-0 m-auto lg:m-0">
            <a href="/signup" className="m-auto">
              <button className="transition-all duration-500 ease-in-out inline-block text-2xl px-6 py-3 leading-none rounded font-bold text-white bg-button-blue hover:bg-button-blue-hover drop-shadow hover:drop-shadow-sm">Sign Up</button>
            </a>

          </div>
        </div>
      </div>
    </div>


    
  );
}

export default About;