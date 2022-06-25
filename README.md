# Music Genre Classifier

## Background
The purpose of this project was to give myself hands-on experience developing and training a neural network. I
began my journey into neural networks by working my way through the textbook "Practical Deep Learning" by Ron
Kneusel (which I believe is an excellent introduction to the world of deep learning). In order to solidify my
skills, I used the knowledge gained from this textbook to start my own deep learning project.

For this project I decided to use the GTZAN dataset to train a model that can classify songs by their genre. This
dataset is very popular and easily accessible, but it does have limitations, which I'll describe later on. The 
dataset consists of 10 genres with 100 songs each. Each song is roughly 30 seconds long.

In addition to building and training the model, I also built a web application that will allow a user to choose
a YouTube video to test the model with. The website provides a quick and easy way to test the accuracy of the 
model in a real-world setting.

You'll notice that there are three main project directories, as described below:  
* model_development: contains all the scripts I used to prepare the data, build, and train the model.
* music_genre_classifier_ui: contains the code used to build the React UI
* music_genre_classifier_server: contains the code used to build the Flask server

The rest of this README describes the process I used to process the data and build a convolutional neural network model using the Keras and Tensorflow libraries.

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

The results were horrible. The test data accuracies are summarized in the "classical_models_results.txt" file. The Random Forest with 500 tress achieved about 26% accuracy. The rest achieve 10-20% accuracy, just barely better than randomly guessing one of the 10 possible genres. The meant that I needed to try a different approach.

### Traditional Model
The next approach I took was to utilize Tensorflow to build a traditional, forward feed neural network. The network I build consisted on 3 hidden layers and a softmax output layer with dropout applied after each hidden layer. The model is defined in the "traditional_neural_network.py" file.

This model achieved about 24% accuracy on the test data - worse than the Random Forest approach. Again, this signaled that I needed to try another approach.

### 1D Convolutional Neural Network Model
Next, I created a set of 1-dimensional convolutional neural network models ranging from 1 to 9 convolutional layers. For each model, I varied the size of the kernel from 3 to 11 in increments of 2. The results are described in the "cnn_1d_models_results.txt" file. This model performed significantly better, achieving an accuracy of nearly 58% on the test data. The winning model was the deep1 model with 7 convolutional layers and a kernel size of 7. Even with this much of an improvement in accuracy, further improvement was still possible.

## Model Development - Phase 2

### About Spectrograms
As summarized by Towards Data Science (cited at bottom), "audio signal is a complex signal composed of multiple ‘single-frequency sound waves’ which travel together as a disturbance(pressure-change) in the medium". When a sound is recorded, we capture the resulting amplitude of those individual waves, which is what makes up the data in an audio file in combination with the sampling rate of the audio. Fourier Transform is a mathematical technique with can take a wave signal and decompose it into its constituent waves as a function of time. Essentially, Fourier Transforms break down a complex wave into the individual, simple waves that compose the complex wave. In addition, we can also use this technique to get the frequency of each component wave.

This is where spectrograms come into play. At each moment in time in the audio wave, we can use Fourier Transforms to break the complex wave into its components, and then find the frequency of each of these components. We can then plot this on a 3-dimensional graph, where the x-axis is time, the y-axis is the frequency, and the color represents the density (number of occurences) of each frequency. The produces an image, such as the following:
![spectrogram](/readme_images/spectrogram_example.png)

Having an image that represents each audio sample enables us to use a 2-dimensional convolutional neural network, which, hopefully, performs even better than the 1-dimensional model.

### Spectrogram Data Preparation
Using a command-line program called Sox, I took each 3-second audio sample and produced a spectrogram image from that audio. I then reduced the resolution of each image to 100x160 pixels to reduce the amount of data needed, which would speed up the training. Based on an exercise I performed in the textbook I mentioned earlier, 100x160 pixels seemed like an adequate size to produce an accurate model.

The last step was to convert each image into a numpy array. I combined all the resulting image arrays into one large 9000x100x160x3 dimensional array. The 3 comes from the fact that a color image file is composed of 3 separate RGB images. After randomizing the order of the images, I split the dataset into 8100 and 900 samples for a 90/10 training to test data split.

### 2D Convolutional Neural Network Model
To find the optimal model architecture, I followed a process similar to that of the traditional neural network training where I tested different depth neural networks with different kernel sizes. The results for each step in the process I documented in the "cnn_2d_models_results.txt" file. I used 90% of the data for training, 5% for validation, and 5% held back for testing only.

First, I constructed three deep networks named deep0, deep1, and deep2 with 3, 4, and 5 convolutional layers respectively. I varied the kernel size from 3x3 to 7x7 for each. The highest accuracy network was the deep0 model with a 3x3 kernel that achieved about 77% accuracy on the test dataset. This is a significant improvement over the traditional model, but I felt I could do better.

The next step I took was to go back to the data preparation stage and see if including augmented data samples would improve accuracy since the network could be trained with more data. For each 3 second audio file, I created 3 additional files that had pitch shift, time shift, noise, and time stretch/compression applied randomly. I then created the spectrogram images and retrained the deep0 model using this new dataset. The results were significantly worse, achieving about 70% accuracy. So, augmented data was not a good approach for this dataset.

Next, I took the deep0 model and started playing with the hyperparameters. I decreased the learning rate, increased the epochs, changed the weight initialization to HE normal, and tried using batch normalization. The highest performing model was the deep0 model with a learning rate of 0.0005, 24 epochs, and an HE normal intialization. This model achieved 80.6% accuracy on the test data.

In a last-ditch effort to improve the accuracy further, I tried recreating the spectrogram dataset using high-contrast images. The idea was that high-contrast images might filter out areas of the image that are less impactful to the genre. Unfortunately, this didn't work and decreased the accuracy to about 72%.

The last change I made to produce the final model was to decrease the epochs from 20 to 24. The reason for this is that, at around 20 epochs, I noticed the validation accuracy begin to drop off while the training set accuracy kept increasing. This is a sure sign of overtraining. Once decreasing the epochs to 20, I was able to achieve a slight improvement with an accuracy of 80.8%.

## Final Results

### Test Set Accuracy
As mentioned previously, the highest performing model achieved 80.8% accuracy on the test dataset. This model used the deep0 architecture with a learning rate of 0.005, 20 epochs, and HE normal weight initialization.IardYtre1!

### Confusion Matrix
The classes for the confusion matrix are listed here:  
   {0: "blues",
    1: "classical",
    2: "country",
    3: "disco",
    4: "hiphop",
    5: "jazz",
    6: "metal",
    7: "pop",
    8: "reggae",
    9: "rock"}

The matrix for the test dataset is depicted below:  
![confusion_matrix](/readme_images/confusion_matrix.png)  

If you follow the diagonal, a few things pop out. First, the metal genre (index 6) has the highest accuracy in the test dataset. Second, the rock genre has the lowest accuracy and is most commonly confused with the country music genre. This tells that, in general, the model should be pretty good at accurately classifying metal music, but pretty bad at classifying rock music.

### Precision, Recall, and F1 Score
Below is a classification report for each genre:  

              precision    recall  f1-score

           0       0.86      0.79      0.83
           1       0.93      1.00      0.96
           2       0.59      0.82      0.68
           3       0.79      0.74      0.77
           4       0.79      0.79      0.79
           5       1.00      0.87      0.93
           6       0.98      0.85      0.91
           7       0.81      0.78      0.79
           8       0.80      0.85      0.83
           9       0.64      0.59      0.61 

The precision is calculated as: # of true positives / (# of true positives + # of false positives). This tells us how good the model is at correctly classifying each genre. The model may still miss quite a few positives, but a high precision means that the model is not missing very many positives. We can see that jazz music (index 5) has a perfect precision for the test dataset while country and rock music have lower precisions. This tells us that other genres are likely to be falsely classified as country and rock genres.

The recall is calculates as: # of true positives / (# of true positives + # of false negatives). In this scenario, a false negative would be a sample that is wrongly classified as a different genre. This metric tells us how well the model can find all of the positive classifications for each genre, even if some of those postives are wrongly identified. We can see that rock music has the lowest recall. This means that the model is not very good at finding all of the positive cases for rock genres in the test dataset.

The F1 score combines the previous two metrics into a single metric by calculating the average of the precision and recall. A high F1 score indicates that both precision and recall are high. Thus, we can see that classical music has the highest F1 score and rock has the lowest. This means that the model is good at classifying classical music in the test dataset and bad at classifying rock music.

## Next Steps
Initially, I had hoped to achieve a higher accuracy on the test dataset. After a bit of research I found that an accuracy of 81% is not at all unusual for the GTZAN dataset using a convolutional neural network. For example, the paper at the following link, https://www.diva-portal.org/smash/get/diva2:1354738/FULLTEXT01.pdf, only achieved a 56% accuracy. The data scientists at this link, https://publikationen.bibliothek.kit.edu/1000118785/71295164, achieved an 84% accuracy using a residual neural network, which is a type of convolutional neural network.

This tells me that the dataset itself is insufficient and that more data is needed to achieve an accuracy in inexcess of 90%. In addition, the GTZAN dataset is not very diverse, has variations in quality, and it is questionable about whether all of the songs are accurately labeled with their correct genres. In order to achieve a better performing model a larger, higher quality dataset is necessary. In addition, trying a different deep learning architecture, such as a residual neural network, might also prove useful.

If you made it this far, thanks for reading! If not, be sure to check out the website link at the top of the README to test the neural network on real world data. 

## Sources
https://nostarch.com/practical-deep-learning-python  
https://www.tensorflow.org/tutorials/keras/classification  
https://towardsdatascience.com/understanding-audio-data-fourier-transform-fft-spectrogram-and-speech-recognition-a4072d228520
https://towardsdatascience.com/the-f1-score-bec2bbc38aa6  
