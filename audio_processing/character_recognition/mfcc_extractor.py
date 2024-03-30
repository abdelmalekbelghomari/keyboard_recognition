import librosa
import numpy as np
import pandas as pd

def extract_mfcc(segments, sample_rate, label, n_mfcc=13):
    mfcc_dataframes = []
    for data, char in zip(segments, label):
        char_label = "space" if char == ' ' else char
        mfccs = librosa.feature.mfcc(y=data.astype(np.float32), sr=sample_rate, n_mfcc=n_mfcc)
        mfccs_vector = np.mean(mfccs, axis=1)
        df = pd.DataFrame([np.append(char_label, mfccs_vector)])
        mfcc_dataframes.append(df)
    
    return mfcc_dataframes