const Leaderboard = () => {


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
            <tr class="odd:bg-white odd:dark:bg-gray-900 even:bg-gray-50 even:dark:bg-gray-800 border-b dark:border-gray-700">
                <td class="w-4 p-4">
                    <div class="flex items-center">
                        <th>1</th>
                        <label for="checkbox-all-search" class="sr-only">checkbox</label>
                    </div>
                </td>
                <th scope="row" class="px-6 py-4 font-medium text-gray-900 whitespace-nowrap dark:text-white">
                    Christians Model
                </th>
                <td class="px-6 py-4">
                    ANN
                </td>
                <td class="px-6 py-4">
                    78.6%
                </td>
                <td class="px-6 py-4">
                    4/14/2024
                </td>
                <td class="px-6 py-4">
                    <a href="#" class="font-medium text-blue-600 dark:text-blue-500 hover:underline">View</a>
                </td>
            </tr>
            <tr class="odd:bg-white odd:dark:bg-gray-900 even:bg-gray-50 even:dark:bg-gray-800 border-b dark:border-gray-700">
            <td class="w-4 p-4">
                    <div class="flex items-center">
                        <th>2</th>
                        <label for="checkbox-all-search" class="sr-only">checkbox</label>
                    </div>
                </td>
                <th scope="row" class="px-6 py-4 font-medium text-gray-900 whitespace-nowrap dark:text-white">
                    Logans Model
                </th>
                <td class="px-6 py-4">
                    SVM
                </td>
                <td class="px-6 py-4">
                    74.4%
                </td>
                <td class="px-6 py-4">
                    4/14/2024
                </td>
                <td class="px-6 py-4">
                    <a href="#" class="font-medium text-blue-600 dark:text-blue-500 hover:underline">View</a>
                </td>
            </tr>
            <tr class="odd:bg-white odd:dark:bg-gray-900 even:bg-gray-50 even:dark:bg-gray-800 border-b dark:border-gray-700">
            <td class="w-4 p-4">
                    <div class="flex items-center">
                        <th>3</th>
                        <label for="checkbox-all-search" class="sr-only">checkbox</label>
                    </div>
                </td>
                <th scope="row" class="px-6 py-4 font-medium text-gray-900 whitespace-nowrap dark:text-white">
                    Joshs Model
                </th>
                <td class="px-6 py-4">
                    GBR
                </td>
                <td class="px-6 py-4">
                    73.9%
                </td>
                <td class="px-6 py-4">
                    4/14/2024
                </td>
                <td class="px-6 py-4">
                    <a href="#" class="font-medium text-blue-600 dark:text-blue-500 hover:underline">View</a>
                </td>
            </tr>
            <tr class="odd:bg-white odd:dark:bg-gray-900 even:bg-gray-50 even:dark:bg-gray-800 border-b dark:border-gray-700">
            <td class="w-4 p-4">
                    <div class="flex items-center">
                        <th>4</th>
                        <label for="checkbox-all-search" class="sr-only">checkbox</label>
                    </div>
                </td>
                <th scope="row" class="px-6 py-4 font-medium text-gray-900 whitespace-nowrap dark:text-white">
                    Connors Model
                </th>
                <td class="px-6 py-4">
                    SVM
                </td>
                <td class="px-6 py-4">
                    56%
                </td>
                <td class="px-6 py-4">
                    4/15/2024
                </td>
                <td class="px-6 py-4">
                    <a href="#" class="font-medium text-blue-600 dark:text-blue-500 hover:underline">View</a>
                </td>
            </tr>

        </tbody>
    </table>
</div>

);

};

export default Leaderboard;