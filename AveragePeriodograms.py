import os
import wave
import numpy as np


import pylab

def wordBoundary(path):
    """This function is used to extract the word boundary timings from the Text Grid file
    that I received from the Forced Aligner"""
    import copy
    f = open(path,'r')
    text = f.read()
    index = text.find('"word"')
    word_intervals = text[index-1:]
    word_intervals = word_intervals.replace('\n', ' ')
    word_intervals = word_intervals.split()[5:]
    words, boundaries = word_intervals[1::3], [float(i) for i in word_intervals[::3]]
    for word, boundary in zip(words, copy.deepcopy(boundaries)):
        if word == '"sp"': #remove timings that indicate to silence
            boundaries.remove(boundary)
    
    return boundaries

def graph_spectrogram(wav_file):
    """This function is used to return the periodograms for each timing."""
    sound_info, frame_rate = get_wav_info(wav_file)
    pylab.figure(num=None, figsize=(19, 12))
    pylab.subplot(111)
    pylab.title('spectrogram of %r' % wav_file)
    return pylab.specgram(sound_info, Fs=frame_rate)
    
    
def get_wav_info(wav_file):
    wav = wave.open(wav_file, 'r')
    frames = wav.readframes(-1)
    sound_info = pylab.fromstring(frames, 'Int16')
    frame_rate = wav.getframerate()
    wav.close()
    return sound_info, frame_rate



def average(path_to_boundary_TextGrid, path_to_wav_file):
    boundary = wordBoundary(path_to_boundary_TextGrid)
    periodograms = graph_spectrogram(path_to_wav_file)
    periodograms_sum = np.sum(periodograms[0], axis = 0) #finding sum of periodograms along each column. Each column corresponds to a time
    boundary_indices = []
    time = list(periodograms[2])
    
    for i in boundary: #find indices in 'time' list whose values are the closest to boundary timings
        minimum = 999999999
        for j in periodograms[2]:
            if abs(i-j) <= minimum:
                minimum = abs(i-j)
                index = time.index(j)
        boundary_indices.append(index)
    
    boundary_periodogram_sum = 0
    
    for i in boundary_indices:
        boundary_periodogram_sum += periodograms_sum[int(i)]
    boundary_periodogram_average = boundary_periodogram_sum/len(boundary)    
    non_boundary_periodogram_average = (np.sum(periodograms_sum) - boundary_periodogram_sum)/(len(time) - len(boundary))
    
    x = 0
    for i in boundary_indices:
        x += (boundary_periodogram_average - periodograms_sum[int(i)])**2
        
    std_deviation_boundary = (x/len(boundary))**(0.5)
    
    x = 0
    for j in [i for i in range(len(time)) if i not in boundary_indices]:
        x += (non_boundary_periodogram_average - periodograms_sum[int(j)])**2
    
    std_deviation_nonboundary = (x/(len(time) - len(boundary)))**0.5
    
    
    return (boundary_periodogram_average, non_boundary_periodogram_average, std_deviation_boundary, std_deviation_nonboundary)
