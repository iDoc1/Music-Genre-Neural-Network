import React from 'react';
  
function Thumbnail({ songInfo }) {
  return (
    <> 
        <div className='imgContainer'>
            <img 
            className='imgThumbnail'
            src={songInfo.videoImgUrl}
            alt='new'
            />
            <figcaption>{songInfo.videoTitle}</figcaption>
            <a className='videoLink' href={songInfo.videoUrl}>Video Link</a>
        </div>       
    </>
  );
};
  
export default Thumbnail;