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

During this step, however, I discovered that many of the audio files were not actually 30 seconds long. For the sake of maintaining the 3 second long samples, I decided to split each audio file into nine samples instead for a total of 9000 samples. Although I could have used a shorter sample length like 2.5 or 2.7 seconds, I opted to stay with 3 seconds because dealing with a whole number would keep the calculations simple and ensure that I didn't end up with non-integer values later on. This was my first lesson during this project on the importance of quality datasets.

My next step was to randomize the data and split it into training and test data. I opted for a 90/10 split of training to test since the dataset size is relatively small. I then processed the audio files and only kept every 50th data point. Since the sampling rate of the dataset os 22050 Hz, it's not necessary to keep every data point in order to classify the audio.

Lastly, I save the training and test datasets as Numpy arrays to be used as input for the classical models and traditional neural network models.

### Classical Models

### Traditional Model

### 1D Convolutional Neural Network Model

## Model Development - Phase 2

### Spectrograms

### 2D Convolutional Neural Network Model

## Final Results

### Test Set Accuracy

### Confusion Matrix

### F1 Score

## Next Steps

## Citations
https://nostarch.com/practical-deep-learning-python  
https://www.tensorflow.org/tutorials/keras/classification  
https://towardsdatascience.com/understanding-auc-roc-curve-68b2303cc9c5