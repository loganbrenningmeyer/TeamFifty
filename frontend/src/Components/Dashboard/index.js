import React, {useState} from 'react'
import { DashboardContainer, DashboardBg, } from './DashboardElements';
import { Provider } from 'react-redux'

const Dashboard = () => {
    const [hover, setHover] = useState(false)

    const onHover = () => {
        setHover(!hover)
    }



    return (
        <DashboardContainer id="home">
            <DashboardBg>
            </DashboardBg>
        </DashboardContainer>
        );
};



export default Dashboard