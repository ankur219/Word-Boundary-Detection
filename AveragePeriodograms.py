import os
import wave


import pylab

def wordBoundary(path):
    import copy
    f = open(path,'r')
    text = f.read()
    index = text.find('"word"')
    word_intervals = text[index-1:]
    word_intervals = word_intervals.replace('\n', ' ')
    word_intervals = word_intervals.split()[5:]
    words, boundaries = word_intervals[1::3], [float(i) for i in word_intervals[::3]]
    for word, boundary in zip(words, copy.deepcopy(boundaries)):
        if word == '"sp"':
            boundaries.remove(boundary)
    
    return boundaries

def graph_spectrogram(wav_file):
    sound_info, frame_rate = get_wav_info(wav_file)
    pylab.figure(num=None, figsize=(19, 12))
    pylab.subplot(111)
    pylab.title('spectrogram of %r' % wav_file)
    return pylab.specgram(sound_info, Fs=frame_rate)
    
    
    
    #pylab.plot(0.26)
    #pylab.savefig('spectrogram15.png')
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
    periodograms_sum = np.sum(periodograms[0], axis = 0)
    boundary_indices = []
    time = list(periodograms[2])
    for i in boundary:
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
    non_boundary_periodogram_average = (np.sum(periodograms_sum) - boundary_periodogram_sum)/(periodograms_sum.shape[0] - len(boundary))
    return (boundary_periodogram_average, non_boundary_periodogram_average)

