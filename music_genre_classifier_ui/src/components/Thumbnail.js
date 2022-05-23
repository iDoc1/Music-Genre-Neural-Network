import React from 'react';
  
function Thumbnail() {
  return (
    <> 
        <div className='imgContainer'>
            <img 
            src='https://img.youtube.com/vi/a1BS7XnEZqc/0.jpg'
            alt='new'
            />
            <figcaption>Song name here</figcaption>
        </div>       
    </>
  );
};
  
export default Thumbnail;