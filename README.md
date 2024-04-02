# Audio Forensic Recognition System :mag_right: :keyboard:

Welcome to the Audio Forensic Recognition System repository! Our project is at the cutting edge of security and forensic technology, designed to identify individuals by the unique sound of their keyboard typing patterns and to decipher the keystrokes for enhanced computer security and forensic analysis.

## Overview :page_with_curl:

In the realm of digital security, knowing who is using a computer and what they are typing can be invaluable. Our system employs advanced neural network models to analyze audio data, discern typing patterns, and associate them with specific users. Moreover, our technology can recognize and transcribe the keystrokes, which has a broad range of applications from securing sensitive data to aiding in forensic investigations.

## Features :sparkles:

- **Person Identification**: Utilizing the subtle but unique sound profiles produced by individuals when typing, our system can determine who is using a keyboard with a high degree of accuracy.
- **Keystroke Deciphering**: Our system goes beyond mere identification; it can transcribe the keys being pressed based on the audio input of the typing, which is crucial for forensic analysis and security.
- **Neural Network Models**: We have implemented several machine learning models, optimized with diverse datasets,.
## Technical Stack :computer:

Our Audio Forensic Recognition System leverages a sophisticated stack of technologies and libraries, including:

- **Python**: Our primary programming language, known for its readability and vast ecosystem.
- **LibROSA**: A powerful library for music and audio analysis, used for extracting MFCCs from audio files.
- **Scikit-learn**: Utilized for creating and training the MLPClassifier neural network models, and for data scaling.
- **NLTK**: Used for Levenshtein distance corrections, enhancing our model's output accuracy for letter recognition.
- **Joblib**: For efficient saving and loading of our trained models and scalers.

## Data Preparation and Preprocessing :floppy_disk:

Key to our system's accuracy is the meticulous preparation and preprocessing of audio data:

- **Audio Splitting**: We dissect continuous typing audio into discrete keystroke sounds, isolating unique typing patterns.
- **Feature Extraction**: Through MFCCs, we transform audio signals into a feature set that our neural networks can learn from.

## Model Training and Evaluation :bar_chart:

- **Training Process**: Our models are trained on a dataset of typing sounds, learning to associate specific patterns with individual letters or users.
- **Evaluation Metrics**: We evaluate the performance of our models, ensuring high accuracy and reliability.

## Future Directions :rocket:

- **Dataset Expansion**: To enhance the system's robustness and accuracy, we plan to continually expand our training dataset with more varied typing patterns.
- **Model Optimization**: Ongoing efforts to refine our neural network architecture and parameters for improved performance.
- **Application Development**: We aim to encapsulate our technology into user-friendly applications for real-world forensic and security use cases.


## Getting Started :rocket:

To get started with the Audio Forensic Recognition System, please follow the instructions below:

1. Clone the repository to your local machine.
2. Install the required dependencies listed in `requirements.txt`. (Not complete yet)
3. Its ready! You just have to run the `demo.php` file. 


We're excited to see how our Audio Forensic Recognition System can contribute to the safety and security of digital information. For any queries or support, please contact us through the Issues section of this repository.

## Overview of Functionality

This repository is designed to support two main functionalities: **Letter-by-Letter Recognition** and **Person Recognition** from audio files. Each functionality has a tailored workflow to best suit the model's needs.

### Letter-by-Letter Recognition

For models aimed at recognizing letters or characters from audio:

1. **Splitting Audio Files**: Key to preparing data for letter-by-letter recognition, the `split()` function divides a `.wav` file into segments corresponding to individual keystroke sounds. This step is crucial for isolating the sounds of interest.
   
2. **Extracting MFCCs & Training**: Extract Mel-frequency cepstral coefficients (MFCCs) from these segments for feature representation, then train the model using these features compiled in a `.csv` file.

3. **Evaluation**: Evaluate your trained model on new data by extracting MFCCs from unseen audio files and using the model to predict the letters.

### Person Recognition

For models designed to recognize individuals from their voice:

- **MFCC Extraction Without Splitting**: Directly extract MFCCs from the `.wav` files without the need for splitting, as the model learns from the overall keystroke characteristics rather than isolated sounds.

- **Training & Evaluation**: Similar to the letter-by-letter approach, train your model with these features and evaluate on new data.

### How to Use

#### To Identify a Letter

1. **Extract MFCCs from a Specific `.wav` File**:
    ```sh
    python3 audio_processing/character_recognition/evaluation_audio_processing.py --audio_file path/to/audio_file.wav --output_csv outpu_csv.csv
    ```

2. **Run the Trained Model to Make Predictions**:
    ```sh
    python3 evaluation/trained_model.py --model ../models/model.joblib --scaler ../scalers/scaler.joblib --input_csv ../output_csv.csv --predictions_output ../models_results/results.txt
    ```
3. **Train the model if needed**:
    ```sh
    python3 training/train.py --input_csv path/to/input_csv --predictions_output path/to/predictions_output.txt --model_name model --scaler_name scaler
    ```
#### To Identify a Person

1. **Extract MFCCs from a Specific `.wav` File**:
    ```sh
    python3 ../audio_processing/person_recognition/evaluation_mfcc_extractor.py --audio_file ../sentences_audios/haykel_sentences/1_haykel.wav --output_csv ../test2.csv
    ```

2. **Run the Trained Model to Make Predictions**:
    ```sh
    python3 ../evaluation/trained_model.py --model ../models/second_person_recognizer.joblib --scaler ../scalers/400_features_scaler.joblib --input_csv ../test2.csv --predictions_output ../models_results/person_results.txt
    ```
3. **Train the model if needed**:
    ```sh
    python3 training/train.py --input_csv path/to/input_csv --predictions_output path/to/predictions_output.txt --model_name model --scaler_name scaler
    ```
#### To use the demonstration

First, run `demo.py`, then launch `demo.php`. Choose the mode you desire, either person recognition or letter recognition. Next, type into the input for 10 seconds, and voilà, you'll have your result—even if it's incorrect.

These commands provide a streamlined process for using the provided scripts for both letter identification and person recognition. Each step is designed to prepare the data, extract the necessary features, and apply the trained models for prediction. Make sure to adjust the paths according to your project's directory structure.




Happy investigating! :detective:


