# Music Genre Classifier

## Background
The purpose of this project was to give myself hands-on experience developing and training a neural network. I
began my journey into neural network by working my way through the textbook "Practical Deep Learning" by Ron
Kneusel (which I believe is an excellent introduction to the world of deep learning). In order to solidify my
skills, I used the knowledge gained from this textbook to start my own deep learning project.

For this project I decided to use the GTZAN dataset to train a model that can classify songs by their genre. This
dataset is very popular and easily accessible, but it does have limitations, which I'll describe later on. The 
dataset consists of 10 genres with 100 songs each. Each song is roughly 30 seconds long.

In addition to building and training the model, I also decided to build a website that will allow a user to choose
a YouTube video to test the model with. The website provides a quick and easy way to test the accuracy of the 
model in a real-world setting.

You'll notice that there are three main project directories, as described below:  
* model_development: contains all the scripts I used to prepare the data, build, and train the model.
* music_genre_classifier_ui: contains the code used to build the React UI
* music_genre_classifier_server: contains the code used to build the Flask server

The rest of this README describes the process I used to process the data and build a functional neural network model using the Keras and Tensorflow libraries.

## Model Development - Phase 1

### Data Preparation
First, I wrote a script to build a file list of each audio file location and it's associated label (music genre). Since each audio sample is supposed to be 30 seconds long, and there are 1000 audio files, I decided to split each
audio file into ten 3 second samples for a total of 10000 samples. 

During this step, however, I discovered that many of the audio files were not actually 30 seconds long. For the sake of maintaining the 3 second long samples, I decided to split each audio file into nine samples instead for a total of 9000 samples. Although I could have used a shorter sample length like 2.5 or 2.7 seconds, I opted to stay with 3 seconds because dealing with a whole number would keep the calculations simple and ensure that I didn't end up with non-integer values later on (for example, dividing the sampling rate 22050 by 3 is a whole number, but dividing by 2.7 is not). This was my first lesson during this project on the importance of quality datasets.

My next step was to randomize the data and split it into training and test data. I opted for a 90/10 split of training to test since the dataset size is relatively small. I then processed the audio files and only kept every 50th data point. Since the sampling rate of the dataset os 22050 Hz, it's not necessary to keep every data point in order to classify the audio.

Lastly, I save the training and test datasets as Numpy arrays to be used as input for the classical models and traditional neural network models.

### Classical Models
I used the scikit-learn library to attempt to create a genre classifier using the following models:
* Nearest Centroid
* K-Nearest Neighbors
* Naive Bayes
* Random Forest
* SVM

The results were horrible. They test data accuracies are summarized in the "classical_models_results.txt" file. The Random Forest with 500 tress achieved about 26% accuracy. The rest achieve 10-20% accuracy, just barely better than randomly guessing one of the 10 possible genres. The meant that I needed to try a different approach.

### Traditional Model
The next approach I took was to utilize Tensorflow to build a traditional, forward feed neural network. The network I build consisted on 3 hidden layers and a softmax output layer with dropout applied after each hidden layer. The model is defined in the "traditional_neural_network.py" file.

This model achieved about 24% accuracy on the test data - worse than the Random Forest approach. Again, this signaled that I needed to try another approach.

### 1D Convolutional Neural Network Model
Next, I created a set of 1-dimensional convolutional neural network models ranging from 1 to 9 convolutional layers. For each model, I varied the size of the kernel from 3 to 11 in increments of 2. The results are described in the "cnn_1d_models_results.txt" file. This model performed significantly better, achieving an accuracy of nearly 58% on the test data. The winning model was the deep1 model with 7 convolutional layers and a kernel size of 7. Even with this much of an improvement in accuracy, further improvement was still possible.

## Model Development - Phase 2

### About Spectrogram
As summarized by Towards Data Science (cited at bottom), "audio signal is a complex signal composed of multiple ‘single-frequency sound waves’ which travel together as a disturbance(pressure-change) in the medium". When a sound is recorded, we capture the resulting amplitude of those individual waves, which is what makes up the data in an audio file in combination with the sampling rate of the audio. Fourier Transform is a mathematical technique with can take a wave signal and decompose it into its constituent waves as a function of time. Essentially, Fourier Transforms break down a complex wave into the individual, simple waves that compose the complex wave. In addition, we can also use this technique to get the frequency of each component wave.

This is where spectrograms come into play. At each moment in time in the audio wave, we can use Fourier Transforms to break the complex wave into its components, and then find the frequency of each of these components. We can then plot this on a 3-dimensional graph, where the x-axis is time, the y-axis is the frequency, and the color represents the density (number of occurences) of each frequency. The produces an image, such as the following:
![spectrogram](/readme_images/spectrogram_example.png)

Having an image that represents each audio sample enables us to use a 2-dimensional convolutional neural network, which, hopefully, performs even better than the 1-dimensional model.

### Spectrogram Data Preparation
Using a command-line program called Sox, I took each 3-second audio sample and produced a spectrogram image from that audio. I then reduced the resolution of each image to 100x160 pixels to reduce the amount of data needed, which would speed up the training. Based on an exercise I performed in the textbook I mentioned earlier, 100x160 pixels seemed like an adequate size to produce an accurate model.

The last step was to convert each image into a numpy array. I combined all the resulting image arrays into one large 9000x100x160x3 dimensional array. The 3 comes from the fact that a color image file is composed of 3 separate RGB images. After randomizing the order of the images, I split the data set into 8100 and 900 samples for a 90/10 training to test data split.

### 2D Convolutional Neural Network Model

## Final Results

### Test Set Accuracy

### Confusion Matrix

### F1 Score

## Next Steps

## Citations
https://nostarch.com/practical-deep-learning-python  
https://www.tensorflow.org/tutorials/keras/classification  
https://towardsdatascience.com/understanding-audio-data-fourier-transform-fft-spectrogram-and-speech-recognition-a4072d228520