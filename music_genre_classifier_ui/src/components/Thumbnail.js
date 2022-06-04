import React from 'react';
import { useNavigate } from 'react-router-dom';
 
function Thumbnail({ songInfo, setVideoUrl }) {
    const navigate = useNavigate();

    // Sends request to run song through results, then shows results page
    const showModelResults = () => {
        setVideoUrl(songInfo.videoUrl);
        navigate('/results');
    }

    return (
        <> 
            <div className='imgContainer'>
                <img 
                className='imgThumbnail'
                src={songInfo.videoImgUrl}
                alt='new'
                onClick={showModelResults}
                />
                <figcaption>{songInfo.videoTitle}</figcaption>
                <a className='videoLink' href={songInfo.videoUrl}>Video Link</a>
            </div>       
        </>
    );
};
  
export default Thumbnail;