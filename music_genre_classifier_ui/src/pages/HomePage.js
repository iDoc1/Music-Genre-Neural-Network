import React from 'react';
import { useState } from 'react';
import SearchBox from '../components/SearchBox';
import Thumbnail from '../components/Thumbnail';
import InfoText from '../components/InfoText';

/**
 * Defines the home page for the website that contains a search box
 */
function HomePage({ setVideoUrl, setVideoTitle }) {
    const [songObjArr, setSongObjArr] = useState([]);
    const [infoTextCount, setInfoTextCount] = useState(0);

    // Call server to get YouTube search data given the queryString submitted by user
    const fetchSearchData = async (queryString) => {        
        const baseUrl = '/youtube-search-results';
        const response = await fetch(baseUrl + `?songName=${encodeURIComponent(queryString)}`);
        const data = await response.json();

        // Handle errors
        if (response.status !== 200) {
            alert(`Error while fetching YouTube records, status code = ${response.status}`);
        } else {

            // Check if response data is empty before proceeding
            if (Object.keys(data).length > 0) {            
                setSongObjArr([]);  // Clear array first
                
                // Create an array of song objects using the JSON response data
                for (let i = 0; i < data['thumbnail_urls'].length; i++) {
                    let songObj = {};
                    songObj['videoUrl'] = data['video_urls'][i];
                    songObj['videoImgUrl'] = data['thumbnail_urls'][i];
                    songObj['videoTitle'] = data['video_titles'][i];
                    setSongObjArr(songObjArr => [...songObjArr, songObj]);
                }

                // Add informative text
                setInfoTextCount(1);
            }
        }       
    }

    return (
        <>
            <h1>Model Accuracy Tester</h1>
            <br/>
            <SearchBox fetchSearchData={fetchSearchData}/>
            <br/>
            <div className='thumbnailContainer'>                
                {songObjArr.map((songObj, i) => <Thumbnail
                    songInfo={songObj}
                    setVideoUrl={setVideoUrl}
                    
                    setVideoTitle={setVideoTitle}
                    key={i}/>)}                
            </div>
            <div className='infoTextContainer'>
                {[...Array(infoTextCount)].map((_, i) => <InfoText
                        key={i}/>)}
            </div>
        </>
    );
};
  
export default HomePage;