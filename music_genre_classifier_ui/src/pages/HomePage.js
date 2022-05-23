import React from 'react';
import SearchBox from '../components/SearchBox';
import Thumbnail from '../components/Thumbnail';
  
function HomePage() {
  return (
    <>
        <h1>Model Accuracy Tester</h1>
        <br/>
        <SearchBox/>
        <br/>
        <div className='thumbnailContainer'>
          <Thumbnail/>
          <Thumbnail/>
          <Thumbnail/>
        </div>
    </>
  );
};
  
export default HomePage;