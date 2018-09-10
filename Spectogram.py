
import os
import wave


import pylab

def wordBoundary(path_to_file):
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
    pylab.specgram(sound_info, Fs=frame_rate)
    pylab.scatter(wordBoundary(path_to_file), [5000 for i in range(len((wordBoundary(path_to_file))))], color = 'r')
    
    
    #pylab.plot(0.26)
    #pylab.savefig('spectrogram15.png')
def get_wav_info(wav_file):
    wav = wave.open(wav_file, 'r')
    frames = wav.readframes(-1)
    sound_info = pylab.fromstring(frames, 'Int16')
    frame_rate = wav.getframerate()
    wav.close()
    return sound_info, frame_rate

if __name__ == '__main__':
    path_to_file = 'path_to_wordBoundaries_file'
    wav_file = 'path_to_wav_file'
    wordBoundary(path_to_file)
    graph_spectrogram(wav_file)
