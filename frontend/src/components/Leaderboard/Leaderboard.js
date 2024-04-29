import React, { useEffect, useState } from 'react';
import { Navigation } from "swiper/modules";
import axios from 'axios';
import { elements } from 'chart.js';



const Leaderboard = () => {
    const [modelList,setModelList] = useState([])
    useEffect (() => {
        const getLeaderboardInfo =  async () => {
            const response = await axios.get('http://localhost:3000/getAllModels');
            
            setModelList(response.data)
            console.log(modelList)
        }
        getLeaderboardInfo();
    },[]); 
    
    const sorted = modelList.sort((a,b) => b.validation_accuracy[99] - a.validation_accuracy[99]);
return (
<div class="relative overflow-x-auto shadow-md sm:rounded-lg">
    <table class="w-full text-sm text-left rtl:text-right text-gray-500 dark:text-gray-400">
        <thead class="text-xs text-gray-700 uppercase bg-gray-50 dark:bg-gray-700 dark:text-gray-400">
            <tr>
            <th scope="col" class="p-4">
                    <div class="flex items-center">
                        <th >Rank</th>
                        <label for="checkbox-all-search" class="sr-only">checkbox</label>
                    </div>
                </th>
                <th scope="col" class="px-6 py-3">
                    Model name
                </th>
                <th scope="col" class="px-6 py-3">
                    Model Type
                </th>
                <th scope="col" class="px-6 py-3">
                    Accuracy
                </th>
                <th scope="col" class="px-6 py-3">
                    Date
                </th>
                <th scope="col" class="px-6 py-3">
                    View Model
                </th>
            </tr>
        </thead>
        <tbody>
            {
            sorted.map((element,index) => {
                return (
                    <tr class="odd:bg-white odd:dark:bg-gray-900 even:bg-gray-50 even:dark:bg-gray-800 border-b dark:border-gray-700">
                <td class="w-4 p-4">
                    <div class="flex items-center">
                        <th>{index+1}</th>
                        <label for="checkbox-all-search" class="sr-only">checkbox</label>
                    </div>
                </td>
                <th scope="row" class="px-6 py-4 font-medium text-gray-900 whitespace-nowrap dark:text-white">
                    {element.model_name}
                </th>
                <td class="px-6 py-4">
                {element.model_type}
                </td>
                <td class="px-6 py-4">
                {element.validation_accuracy[99]}
                </td>
                <td class="px-6 py-4">
                    4/14/2024
                </td>
                <td class="px-6 py-4">
                    <a href="#" class="font-medium text-blue-600 dark:text-blue-500 hover:underline">View</a>
                </td>
            </tr>
                )
            })
            
            }
        </tbody>
    </table>
</div>

);

};

export default Leaderboard;