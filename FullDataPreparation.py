from WindowSegmentation import SlidingWindow
from Parser import DetectSeizure
import mne
import torch
import numpy as np
import pickle
import os
import gzip
from joblib import dump, load
import pandas as pd
import numpy as np
from scipy import signal
from scipy.fft import fftshift
import matplotlib
import matplotlib.pyplot as plt
from scipy.fft import fft, fftfreq
import gzip
import pickle

res = os.listdir('..\..\downloads')
counter = 0

window_size = 30 #seconds
shift_step = 10 #seconds
sampling_rate = 256 # hz 
my_data = []

for recording in (res):
    print(recording)
    raw = mne.io.read_raw_edf('..\..\downloads\\'+str(recording))
    data, times = raw[:]
    filename = str(recording)
    counter +=1 
    # my_data = process_data(filename, data, window_size, shift_step, sampling_rate)
    windows = SlidingWindow(data, (window_size*sampling_rate), (shift_step*sampling_rate)) 
    for i in range(len(windows)):
        window_start_time = i * shift_step
        window_end_time = window_start_time + window_size
        my_data.append((windows[i],DetectSeizure(filename, window_start_time, window_end_time)))
    if counter == 30:
        break


N = len(my_data[0][0][0])
T = 1.0 / 256
x = np.linspace(0.0, N*T, N, endpoint=False)  
new_data = []
for window in my_data:
    data, label = window
    window_features = []
    for channel in data:
        features = []
        y1 = channel
        yf1 = fft(y1)
        xf1 = fftfreq(N, T)[:N//2]
        features.append((abs(channel).sum()))
        features.append(np.var(channel))
        features.append(np.median((abs((channel)))))
        features.append(np.mean((2.0/N * np.abs(yf1[0:N//2]))[(np.where(xf1 == 0))[0][0]:((np.where(xf1 == 4))[0][0])]))
        features.append(np.mean((2.0/N * np.abs(yf1[0:N//2]))[(np.where(xf1 == 4))[0][0]:((np.where(xf1 == 8))[0][0])]))
        features.append(np.mean((2.0/N * np.abs(yf1[0:N//2]))[(np.where(xf1 == 8))[0][0]:((np.where(xf1 == 12))[0][0])]))
        features.append(np.mean((2.0/N * np.abs(yf1[0:N//2]))[(np.where(xf1 == 12))[0][0]:((np.where(xf1 == 30))[0][0])]))
        features.append(np.mean((2.0/N * np.abs(yf1[0:N//2]))[(np.where(xf1 == 30))[0][0]:((np.where(xf1 == 55))[0][0])]))
        features.append(np.mean((2.0/N * np.abs(yf1[0:N//2]))[(np.where(xf1 == 55))[0][0]:((np.where(xf1 == 61))[0][0])]))
        window_features.append(features)
    new_data.append((np.array(window_features), label))


with gzip.open('MyDataFeatureFull2.pkl', 'wb') as f:
    pickle.dump(new_data, f)
print("done")


