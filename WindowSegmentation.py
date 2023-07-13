import mne
import matplotlib.pyplot as plt
import numpy as np
from Parser import DetectSeizure
import torch

def SlidingWindow(data, window_size, shift_step):
    windows = []
    i = 0
    while i + window_size <= data.shape[1]:
        windows.append(data[:,i:window_size+i])
        i += shift_step
    return windows
    # Now windows is a list of 2D arrays, each of size (23, 1024)
  
def process_data(filename, data, window_size, shift_step, sampling_rate):
    windows = SlidingWindow(data, (window_size*sampling_rate), (shift_step*sampling_rate))
    my_data = []
    for i in range(len(windows)):
        # Calculate the time for the start of the window
        window_start_time = i * shift_step
        window_end_time = window_start_time + window_size
        my_data.append((windows[i],DetectSeizure(filename, window_start_time, window_end_time)))
    return my_data

filename = "chb01_03.edf"
window_size = 30 #seconds
shift_step = 10 #seconds
sampling_rate = 256 # hz 

raw = mne.io.read_raw_edf("..\..\downloads\chb01_03.edf")
data, times1 = raw[:]

my_data = process_data(filename, data, window_size, shift_step, sampling_rate)
train_loader = torch.utils.data.DataLoader(my_data, batch_size=64)
print((my_data[300]))

'''
len(process_data(filename, data, window_size, shift_step, sampling_rate)[0][0][0]) = length of data in each window (=window_size*sampling_rate)
len(process_data(filename, data, window_size, shift_step, sampling_rate)[0][0]) = length of channel for each window (=23)
len(process_data(filename, data, window_size, shift_step, sampling_rate)[0]) = length of data +lable tuple (=2)
len(process_data(filename, data, window_size, shift_step, sampling_rate)) = number of windows/labels
'''