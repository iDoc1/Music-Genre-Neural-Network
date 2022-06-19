import React from 'react';
import { useState, useEffect } from 'react';
import BarChartResults from '../components/BarChartResults';


/**
 * Defines the page that displays teh bar chart results
 */
function ResultsPage({ videoUrl, videoTitle }) {
    const [resultMessage, setResultMessage] = useState('');
    const [modelResults, setModelResults] = useState([]);

    // Specifies the locations for which audio samples are passed through the model
    const sampleLocations = ['Start', 'Middle', 'End'];

    // Specifies colors for each bar chart
    const barChartColors = ['red', 'blue', 'green'];

    // Call server to run the audio at the given URL through the model and get the results
    const fetchModelResults = async (urlToTest) => {
        const baseUrl = 'http://127.0.0.1:5000/model-results';
        const response = await fetch(baseUrl + `?songUrl=${encodeURIComponent(urlToTest)}`);
        const data = await response.json();

        // Handle errors
        if (response.status !== 200) {
            alert(`Error while fetching model results, status code = ${response.status}`);
        } else {

            // Check if response data is empty before storing response data
            if (data.length > 0) {
                setModelResults(data);
            }
        }
    }

    // On page render, run model using audio of given video URL then display results    
    useEffect(() => {
        setResultMessage(`Showing results for: "${videoTitle}"`);
        fetchModelResults(videoUrl);    
    }, [videoTitle, videoUrl])

    
    return (
        <> 
            <h1>Model Results</h1> 
            <p>{resultMessage}</p>
            <div className='barChartContainer'>
                {modelResults.map((resultArr, i) => <BarChartResults
                    resultArr={resultArr}
                    sampleLocation={[sampleLocations[i]]}
                    barChartColor={barChartColors[i]}
                    key={i}/>)}  
            </div>
        </>
    );
};
  
export default ResultsPage;