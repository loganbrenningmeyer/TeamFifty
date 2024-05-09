import React, { useEffect, useState } from "react";
import axios from "axios";

const Leaderboard = () => {
  const [modelList, setModelList] = useState([]);

  useEffect(() => {
    const fetchModels = async () => {
      const response = await axios.get("http://localhost:3000/getAllModels");
      setModelList(response.data.sort(
        (a, b) => b.validation_accuracy[(b.validation_accuracy).length-1] - a.validation_accuracy[(a.validation_accuracy).length-1]
      ));
    };
    fetchModels();
  }, []);

  return (
    <div class="bg-contain bg-bg-grey">
    <div class="flex flex-col bg-bg-grey min-h-screen">
      <table class="w-full text-sm text-left text-gray-500 dark:text-gray-400">
        <thead class="text-xs text-gray-700 uppercase bg-gray-50 dark:bg-gray-700 dark:text-gray-400">
          <tr>
            <th scope="col" class="p-4">Rank</th>
            <th scope="col" class="px-6 py-3">Model name</th>
            <th scope="col" class="px-6 py-3">Model Type</th>
            <th scope="col" class="px-6 py-3">Accuracy</th>
            <th scope="col" class="px-6 py-3">View Model</th>
          </tr>
        </thead>
        <tbody>
          {modelList.map((element, index) => (
            <tr class="odd:bg-white odd:dark:bg-gray-900 even:bg-gray-50 even:dark:bg-gray-800 border-b dark:border-gray-700">
              <td class="w-4 p-4">{index + 1}</td>
              <td class="px-6 py-4 font-medium text-gray-900 whitespace-nowrap dark:text-white">
                {element.model_name}
              </td>
              <td class="px-6 py-4">{element.model_type}</td>
              <td class="px-6 py-4">{element.validation_accuracy[element.validation_accuracy.length - 1]}</td>
              <td class="px-6 py-4">
                <a href="#" class="font-medium text-blue-600 dark:text-blue-500 hover:underline">View</a>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
    </div>
  );
};

export default Leaderboard;
