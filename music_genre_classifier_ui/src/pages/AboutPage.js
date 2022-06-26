import React from 'react';

/**
 * Defines the page that shared info about this project
 */
function AboutPage() {
  return (
    <>
        <h1>About this Project</h1>
        <br/>

        <h3>How to Use This Website</h3>
        <p className='aboutPageParagraph'>
            The purpose of this website is to provide a way to visualize how well the neural network
            model classifies music genres in real-worl scenarios. To use the tool, simply go to the
            Model Accuracy Tester page, enter the name of a song you would like to test, click on the
            YouTube thumbnail image that pops up, then view the results for audio samples taken from
            the start, middle, and end of the selected audio.
        </p>
        <br/>

        <h3>Source Code</h3>
        <p className='aboutPageParagraph'>
            To view the source code and in-depth documentation on how this website and the associated
            neural network was developed, follow the below link to the project GitHub repository:        
        </p>
        <a  
            href='https://github.com/iDoc1/Music-Genre-Neural-Network' 
            target='_blank'
            rel='noreferrer'
            >Link to GitHub Repo
            
        </a>
        <br/>
        <br/>

        <h3>Details on Model Accuracy</h3>
        <p className='aboutPageParagraph'>
            If you read through the README at the above GitHub link you will learn that the model achieved
            about 81% accuracy on the test data. However, if you actually test the tool yourself you will
            find that the classification of genres is often wildly inaccurate. This indicates multiple
            issues. First, there is not enough test data. The GTZAN dataset used to train the model
            is not very diverse, high quality, large, or even that accurate in how the dataset has the genres 
            labeled. The GTZAN dataset is one of the most accessible music genre training sets available, but is
            obviously lacking. In order to make the model more accurate, a larger, more diverse, and more accurate 
            dataset is needed. In addition, trying a different approach, such as a Recurrent Neural Network might 
            also prove useful. Future iterations of this project may involve using a different dataset and/or 
            utilizing a different type of neural network.
        </p>
        <br/>

        <h3>About the Developer</h3>
        <p className='aboutPageParagraph'>
            My name is Ian Docherty and I'm an aspiring software engineer. I used this project to teach 
            myself the fundamentals of machine learning using traditional and convolutional neural networks. 
            Instead of simply building and training a neural network, I wanted to try and build something 
            that would actually use the resulting model. That's where the idea for this website came from.
            Now, I have a framework which I can use to evaluate the accuracy of a model. I encourage you 
            to check out the GitHub link if you're interested in learning more about how the model was
            developed.
        </p>
        <br/>
    </>
  );
};
  
export default AboutPage;