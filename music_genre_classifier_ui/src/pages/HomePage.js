import React from 'react';
import SearchBox from '../components/SearchBox';
import Thumbnail from '../components/Thumbnail';
  
function HomePage() {
    const songInfo = {
        videoUrl: 'https://www.youtube.com/watch?v=Ee_uujKuJMI',
        videoImgUrl: 'https://img.youtube.com/vi/a1BS7XnEZqc/0.jpg',
        videoTitle: 'American Idiot'
    };

  // Call Flask server to get YouTube search data
    const getSearchData = async (queryString) => {
        const response = await fetch(`http://127.0.0.1:8050/getYouTubeResults?songName=${encodeURIComponent(queryString)}`);
        const data = await response.json();
        // TODO: Set Data here and pass to thumbnails
    }

  return (
    <>
        <h1>Model Accuracy Tester</h1>
        <br/>
        <SearchBox onClickSubmit={getSearchData}/>
        <br/>
        <div className='thumbnailContainer'>
          <Thumbnail 
            songInfo={songInfo} />

        </div>
    </>
  );
};
  
export default HomePage;