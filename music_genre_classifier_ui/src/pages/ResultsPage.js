import React from 'react';
import { useState, useEffect } from 'react';
  
function ResultsPage({ videoUrl }) {
    const [resultMessage, setResultMessage] = useState('');
    const [modelResults, setModelResults] = useState(null);

    const fetchModelResults = async (urlToTest) => {
        const baseUrl = 'http://127.0.0.1:5000/model-results';
        const response = await fetch(baseUrl + `?songUrl=${encodeURIComponent(urlToTest)}`);
        const data = await response.json();

        // Handle errors
        if (response.status !== 200) {
            alert(`Error while fetching model results, status code = ${response.status}`);
        } else {

            // Check if response data is empty before proceeding
            
            setModelResults(data);
        }
    }

    // On page render, run model using audio of given video URL then display results    
    useEffect(() => {
        setResultMessage(`Showing results for URL: ${videoUrl}`);
        
        // run model
        fetchModelResults(videoUrl);    

    }, [videoUrl])

    
    return (
        <> 
            <h1>Results Page</h1> 
            <p>{resultMessage}</p>
            <p>{modelResults}</p>    
        </>
    );
};
  
export default ResultsPage;