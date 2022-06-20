import React from 'react';
import { Oval } from 'react-loader-spinner';


function LoadingSpinner({isLoading}) {
    
    if (isLoading) {
        return (
            <>
                <div className='spinner'>
                <Oval 
                    height="100"
                    width="100"
                    color='#0d6efd'
                    ariaLabel='processing audio data'
                />
                </div>
            </>
        );
    }
}

export default LoadingSpinner;
