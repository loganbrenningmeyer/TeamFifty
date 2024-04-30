import React, { useEffect, useRef, useState } from "react";
import { Swiper, SwiperSlide } from "swiper/react";
import "swiper/css";
import "swiper/css/navigation";
import "./styles.css";
import "swiper/css/pagination";
import { Navigation } from "swiper/modules";
import { Pagination } from "swiper/modules";
import 'swiper/css';
import axios from 'axios';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js';
import { Line } from 'react-chartjs-2';

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
);

const SavedModels = () => {
  const [models, setModels] = useState([]);
  const [activeModelName, setActiveModelName] = useState('');
  const [activeModelType, setActiveModelType] = useState('');
  const [activeModelVis, setActiveModelVis] = useState('');
  const [activeTrainingData, setActiveTrainingData] = useState({});
  const [activeValidationData, setActiveValidationData] = useState({});

  const [isOpen, setIsOpen] = useState(false);

  useEffect(() => {
    const fetchModels = async () => {
      try {
        const response = await axios.get('http://localhost:3000/retrieveModels');
        setModels(response.data);
        // Optionally set the name of the first model as the initial active model
        if (response.data.length > 0) {
          setActiveModelName(response.data[0].model_name);
          setActiveModelType(response.data[0].model_type);
          setActiveModelVis(response.data[0].model_vis);

          console.log(response.data[0].training_loss)
          console.log(response.data[0].training_accuracy)

          /* Set training loss data */
          const training_data = {
            labels: Array.from(Array(100).keys()),
            datasets: [
              {
                label: 'Training Loss',
                data: response.data[0].training_loss,
                borderColor: 'rgb(255, 99, 132)',
                backgroundColor: 'rgba(255, 99, 132, 0.5)'
              },
              {
                label: 'Training Accuracy',
                data: response.data[0].training_accuracy,
                borderColor: 'rgb(0, 204, 102)',
                backgroundColor: 'rgba(0, 204, 102, 0.5)'
              }
            ]
          }

          /* Set validation loss data */
          const validation_data = {
            labels: Array.from(Array(100).keys()),
            datasets: [
              {
                label: 'Validation Loss',
                data: response.data[0].validation_loss,
                borderColor: 'rgb(255, 99, 132)',
                backgroundColor: 'rgba(255, 99, 132, 0.5)'
              },
              {
                label: 'Validation Accuracy',
                data: response.data[0].validation_accuracy,
                borderColor: 'rgb(0, 204, 102)',
                backgroundColor: 'rgba(0, 204, 102, 0.5)'
              }
            ]
          }

          setActiveTrainingData(training_data);
          setActiveValidationData(validation_data);

          /* Get model visualizations from backend */

        }
      } catch (error) {
        console.error('Failed to retrieve models:', error);
        setModels([]);
      }
    };

    fetchModels();
  }, []);

  const handleSlideChange = (swiper) => {
    const currentModel = models[swiper.activeIndex / 3];
    console.log(currentModel)
    console.log(currentModel.model_name)
    console.log(currentModel.model_type)
    if (currentModel) {
      setActiveModelName(currentModel.model_name);
      setActiveModelType(currentModel.model_type);
      setActiveModelVis(currentModel.model_vis);
      
      /* Set training loss data */
      const training_data = {
        labels: Array.from(Array(100).keys()),
        datasets: [
          {
            label: 'Training Loss',
            data: currentModel.training_loss,
            borderColor: 'rgb(255, 99, 132)',
            backgroundColor: 'rgba(255, 99, 132, 0.5)'
          },
          {
            label: 'Training Accuracy',
            data: currentModel.training_accuracy,
            borderColor: 'rgb(0, 204, 102)',
            backgroundColor: 'rgba(0, 204, 102, 0.5)'
          }
        ]
      }

      /* Set validation loss data */
      const validation_data = {
        labels: Array.from(Array(100).keys()),
        datasets: [
          {
            label: 'Validation Loss',
            data: currentModel.validation_loss,
            borderColor: 'rgb(255, 99, 132)',
            backgroundColor: 'rgba(255, 99, 132, 0.5)'
          },
          {
            label: 'Validation Accuracy',
            data: currentModel.validation_accuracy,
            borderColor: 'rgb(0, 204, 102)',
            backgroundColor: 'rgba(0, 204, 102, 0.5)'
          }
        ]
      }

      setActiveTrainingData(training_data);
      setActiveValidationData(validation_data);
    }
  };

  return (
    <div>
      <div className="grid-header">
        <div>Inputs</div>
        <div>{activeModelName ? `${activeModelName} (${activeModelType})` : 'Model Name (Type)'}</div>
        <div>Outputs</div>
      </div>
      <Swiper
        onSlideChange={handleSlideChange}
        pagination={{
          clickable: true,
          renderBullet: (index, className) => `<span class="${className}">${index + 1}</span>`,
        }}
        navigation={true}
        modules={[Pagination, Navigation]}
        slidesPerView={3}
        slidesPerGroup={3}
        spaceBetween={10}
        className="mySwiper"
      >
        {models.length > 0 ? models.flatMap((model, idx) => [
          <SwiperSlide key={`params-${idx}`}>
            <div className="parameters-grid">
              {Object.entries(model.selected_stats).map(([key, value], index) => (
                <div key={index} className="parameters-item">
                  {value.replace(/_/g, " ")}
                </div>
              ))}
            </div>
          </SwiperSlide>,
          <SwiperSlide key={`accuracy-${idx}`}>
            <div className='model-vis'>
              <img src={`data:image/png;base64,${activeModelVis}`} alt="Model Visualization" />
            </div>
          </SwiperSlide>,
          <SwiperSlide key={`validation-${idx}`}>
            <div className="outputs">
              <div className='training-output'>

                <div className='training-text'>
                  Training Accuracy
                </div>
                
                <div className='training-accuracy'>
                  {(model.training_accuracy[99]*100).toFixed(2)}%
                </div>

              </div>

              <br/>

              <div className='validation-output'>

                <div className='validation-text'>
                  Validation Accuracy
                </div>
                
                <div className='validation-accuracy'>
                  {(model.validation_accuracy[99]*100).toFixed(2)}%
                </div>
              </div>
            </div>
          </SwiperSlide>
        ]) : <SwiperSlide>Loading models...</SwiperSlide>}
      </Swiper>

      <div className={`popup ${isOpen ? "open" : ""}`}>
        <button
          className="w-full bg-button-blue text-white p-4 text-center flex justify-center items-center group"
          onClick={() => setIsOpen(!isOpen)}
        >
          Stats and Parameters {isOpen ? "⯆" : "⯅"}
        </button>
        <div className="popup-content">
          <div className="stats-grid">
            <div>
              {activeTrainingData.datasets && <Line data={activeTrainingData} />}
            </div>
            <div>
              {activeValidationData.datasets && <Line data={activeValidationData} />}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default SavedModels;