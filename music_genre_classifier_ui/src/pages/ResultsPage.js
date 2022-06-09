import React from 'react';
import { useState, useEffect } from 'react';
  
function ResultsPage({ videoUrl }) {
    const [resultMessage, setResultMessage] = useState('');
    const [testVar, setTestVar] = useState('');

    // On page render, run model using audio of given video URL then display results    
    useEffect(() => {
        setTestVar("testVar");
        setResultMessage(`Showing results for URL: ${videoUrl}`);
        // run model
        // display results
    }, [videoUrl])

    
    return (
        <> 
            <h1>Results Page</h1> 
            <p>{resultMessage}</p>
            <p>{testVar}</p>     
        </>
    );
};
  
export default ResultsPage;