import React, { useState} from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import './Dashboard.css';
import SavedModels from '../SavedModels/savedmodel';

    const Dashboard = () =>  {
        return (

        <SavedModels />
    );
};

export default Dashboard;