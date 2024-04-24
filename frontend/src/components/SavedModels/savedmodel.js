import React, { useRef, useState } from "react";
import { Swiper, SwiperSlide } from "swiper/react";
import "swiper/css";
import "swiper/css/navigation";
import "./styles.css";
import "swiper/css/pagination";
import { Navigation } from "swiper/modules";
import { Pagination } from "swiper/modules";
import 'swiper/css';
import axios from 'axios';


const swagArray = ["card 1", "card 2", "card 3", "card 4"];

const SavedModels = () => {
    const [isOpen, setIsOpen] = useState(false);
    const check = async () => 
    {
    const res = await axios.get('http://localhost:3000/retrieveModels');
    } 
        
const pagination = {
        clickable: true,
        renderBullet: function (index, className) {
          return '<span class="' + className + '">' + (index + 1) + '</span>';
        },
    };



  return (
    <div>
    <Swiper
      pagination={pagination}
      navigation={true}
      modules={[Pagination, Navigation]}
      slidesPerView={3}
      spaceBetween={30}
      className="mySwiper"
    >
      {swagArray.map((data) => (
        <SwiperSlide>Slide 1 {data}</SwiperSlide>
      ))}
    </Swiper>



    <div className="fixed inset-x-0 bottom-0">
      <button
        className={`w-full bg-blue-500 text-white p-4 text-center flex justify-center items-center group`}
        onClick={() => setIsOpen(!isOpen)}
      >
        Stats and Parameters
        <span className={`ml-2 transform transition-transform duration-150 ${isOpen ? 'group-hover:translate-y-1' : 'group-hover:-translate-y-1'}`}>
          <svg
            className="w-4 h-4 fill-current"
            xmlns="http://www.w3.org/2000/svg"
            viewBox="0 0 20 20"
          >
            <path d={`${isOpen ? "M5.293 7.293a1 1 0 0 1 1.414 0L10 10.586l3.293-3.293a1 1 0 0 1 1.414 0l.707.707a1 1 0 0 1 0 1.414l-4 4a1 1 0 0 1-1.414 0l-4-4a1 1 0 0 1 0-1.414l-.707-.707z" : "M14.707 11.707a1 1 0 0 1-1.414 0L10 8.414l-3.293 3.293a1 1 0 0 1-1.414 0l-.707-.707a1 1 0 0 1 0-1.414l4-4a1 1 0 0 1 1.414 0l4 4a1 1 0 0 1 0 1.414l.707.707z"}`}/>
          </svg>
        </span>
      </button>
      {isOpen && (
        <div className="bg-white p-4 shadow-lg absolute bottom-full w-full transform translate-y-1">
          <ul>
            <li className="p-2 hover:bg-gray-100" onClick={check}>Data 1</li>
            <li className="p-2 hover:bg-gray-100">Data Item 2</li>
            <li className="p-2 hover:bg-gray-100">Data Item 3</li>
          </ul>
        </div>
      )}
    </div>
    </div> 
  );
};


export default SavedModels;
