import { useCallback, useState, useEffect } from "react";

import { Swiper, SwiperSlide } from "swiper/react";



const SavedModels = () => {
  const [swiperRef, setSwiperRef] = useState();


  const handleLeftClick = useCallback(() => {
    if (!swiperRef) return;
    swiperRef.slidePrev();
  }, [swiperRef]);

  const handleRightClick = useCallback(() => {
    if (!swiperRef) return;
    swiperRef.slideNext();
  }, [swiperRef]);

  return (
    <Swiper
              onSwiper={setSwiperRef}
              slidesPerView={3}
              centeredSlides={true}
              spaceBetween={170}
              loop={true}
              className="w-[1492px] rounded-3xl select-none m-auto mt-16  text-white">
              <SwiperSlide>
                <div className="bg-slate-800 w-80 xl:w-96 rounded-3xl flex flex-col">
                  <div className="flex-grow text-5xl rounded-t-3xl m-auto">
                  </div>
                  <div className="flex flex-wrap w-full text-5xl bg-400-800 rounded-b-3xl bg-slate-800 pt-6 p-8">
                    <div className="text-[1.2rem] font-bold pb-4">FOMO Alerts</div>
                    <div className="text-[1rem] h-16">FOMO alerts are extremely useful and will notify you based on different market conditions surrounding trending projects.</div>
                  </div>
                </div>
              </SwiperSlide>
              <SwiperSlide>
                <div className="bg-slate-800 w-80 xl:w-96 rounded-3xl flex flex-col">
                  <div className="flex-grow text-5xl rounded-t-3xl m-auto">
                  </div>
                  <div className="flex flex-wrap w-full text-5xl bg-400-800 rounded-b-3xl bg-slate-800 pt-6 p-8">
                    <div className="text-[1.2rem] font-bold pb-4">Follow Alerts</div>
                    <div className="text-[1rem] h-16">Follow alerts will show you who important figures are following and can be useful for finding new projects before they blow up.</div>
                  </div>
                </div>
              </SwiperSlide>
              <SwiperSlide>
                <div className="bg-slate-800 w-80 xl:w-96 rounded-3xl flex flex-col">
                  <div className="flex-grow text-5xl rounded-t-3xl m-auto">
                  </div>
                  <div className="flex flex-wrap w-full text-5xl bg-400-800 rounded-b-3xl bg-slate-800 pt-6 p-8">
                    <div className="text-[1.2rem] font-bold pb-4">Contract Alerts</div>
                    <div className="text-[1rem] h-16">Contract alerts makes sure you have access to any lowkey mints or stealth drops that fly under the radar since not every mint is announced.</div>
                  </div>
                </div>
              </SwiperSlide>
            </Swiper>
  )
};

export default SavedModels;