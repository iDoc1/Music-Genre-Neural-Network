import React from 'react';
import { useState, useEffect } from 'react';
  
function ResultsPage({ videoUrl }) {
    const [testVar, setTestVar] = useState("");

    // On page render, run model using audio of given video URL then display results    
    useEffect(() => {
        setTestVar("testVar");
        // run model
        // display results
    }, [])

    
    return (
        <> 
            <h1>Results Page</h1> 
            <p>Show results for: {videoUrl}</p>
            <p>{testVar}</p>     
        </>
    );
};
  
export default ResultsPage;