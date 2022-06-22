import React from 'react';
import { useNavigate } from 'react-router-dom';

/**
 * Returns a component that displays a YouTube video thumbnail image with 
 * a title and link to the video
 */
function Thumbnail({ songInfo, setVideoUrl, setVideoTitle }) {
    const navigate = useNavigate();

    // Sends request to run song through results, then shows results page
    const showModelResults = () => {
        setVideoUrl(songInfo.videoUrl);
        setVideoTitle(songInfo.videoTitle);
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
                <a 
                    className='videoLink' 
                    target='_blank'
                    rel='noreferrer'
                    href={songInfo.videoUrl}>
                    Video Link
                </a>
            </div>       
        </>
    );
};
  
export default Thumbnail;