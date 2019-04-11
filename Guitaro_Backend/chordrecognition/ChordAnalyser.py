"""
Algorithm based on the paper 'Automatic Chord Recognition from
Audio Using Enhanced Pitch Class Profile' by Kyogu Lee
This script computes 12 dimensional chromagram for chord detection
@author ORCHISAMA
https://github.com/orchidas/Chord-Recognition
https://ccrma.stanford.edu/~orchi/
"""

from __future__ import division
import numpy as np
import os
import matplotlib.pyplot as plt
from scipy.io.wavfile import read
import json
from chordrecognition.chromagram import compute_chroma


class ChordAnalyser:
    """
    match_templates.py from https://github.com/orchidas/Chord-Recognition has been modified into a class for use in
    Guitaro.
    """

    def __init__(self, filepath):
        self.chroma_list = []
        self.filepath = filepath

        """read from JSON file to get chord templates"""
        with open('chordrecognition/chord_templates.json', 'r') as fp:
            self.templates_json = json.load(fp)

        self.chords = ['N', 'G', 'G#', 'A', 'A#', 'B', 'C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'Gm', 'G#m', 'Am', 'A#m',
                       'Bm', 'Cm', 'C#m', 'Dm', 'D#m', 'Em', 'Fm', 'F#m']
        self.templates = []

        for chord in self.chords:
            if chord is 'N':
                continue
            self.templates.append(self.templates_json[chord])

        """read audio"""
        (self.fs, self.s) = read(self.filepath)

    def compute_chromagram(self):
        """
        @author ORCHISAMA. Modified to return the chromagram as a list
        :return: chromagram as a list
        """
        x = self.s[::4]
        x = x[:, 1]
        fs = int(self.fs / 4)

        # framing audio, window length = 8192, hop size = 1024 and computing PCP
        nfft = 8192
        hop_size = 1024
        nFrames = int(np.round(len(x) / (nfft - hop_size)))
        # zero padding to make signal length long enough to have nFrames
        x = np.append(x, np.zeros(nfft))
        xFrame = np.empty((nfft, nFrames))
        start = 0
        chroma = np.empty((12, nFrames))
        id_chord = np.zeros(nFrames, dtype='int32')
        timestamp = np.zeros(nFrames)
        max_cor = np.zeros(nFrames)

        for n in range(nFrames):
            xFrame[:, n] = x[start:start + nfft]
            start = start + nfft - hop_size
            timestamp[n] = n * (nfft - hop_size) / fs
            chroma[:, n] = compute_chroma(xFrame[:, n], fs)
            plt.figure(1)
            plt.plot(chroma[:, n])

            """Correlate 12D chroma vector with each of 24 major and minor chords"""
            cor_vec = np.zeros(24)
            for ni in range(24):
                cor_vec[ni] = np.correlate(chroma[:, n], np.array(self.templates[ni]))
            max_cor[n] = np.max(cor_vec)
            id_chord[n] = np.argmax(cor_vec) + 1

        # if max_cor[n] < threshold, then no chord is played
        # might need to change threshold value
        id_chord[np.where(max_cor < 0.8 * np.max(max_cor))] = 0

        for n in range(nFrames):
            if self.chords[id_chord[n]] != "N":
                print("Chord: " + str(self.chords[id_chord[n]]))

        # @author Ronan Connolly
        self.chroma_list = chroma.tolist()
        return self.chroma_list

    def get_notes_of_chord(self, chroma_list):
        """
        @author Ronan Connolly
        :param chroma_list:
        :return:
        """
        notes = {0: "G", 1: "G#",
                 2: "A", 3: "A#",
                 4: "B", 5: "C",
                 6: "C#", 7: "D",
                 8: "D#", 9: "E",
                 10: "F", 11: "F#"}

        g_to_a_sharp_list = list()
        b_to_d_sharp_list = list()
        d_sharp_to_f_sharp = list()

        for i in range(0, len(chroma_list)):
            if i < 4:
                g_to_a_sharp_list.append(max(chroma_list[i]))
            if i >= 4 and i < 8:
                b_to_d_sharp_list.append(max(chroma_list[i]))
            if i >= 8 and i < 12:
                d_sharp_to_f_sharp.append(max(chroma_list[i]))

        note_1 = max(g_to_a_sharp_list)
        note_2 = max(b_to_d_sharp_list)
        note_3 = max(d_sharp_to_f_sharp)

        list_of_note_maxes = g_to_a_sharp_list + b_to_d_sharp_list + d_sharp_to_f_sharp

        list_of_notes = list()
        list_of_notes.append(notes.get(list_of_note_maxes.index(note_1)))
        list_of_notes.append(notes.get(list_of_note_maxes.index(note_2)))
        list_of_notes.append(notes.get(list_of_note_maxes.index(note_3)))
        return list_of_notes

    def plot_figures(self, timestamp, id_chord):
        """
        @author ORCHISAMA
        :param timestamp:
        :param id_chord:
        :return:
        """
        # Plotting all figures
        plt.figure(1)
        notes = ['G', 'G#', 'A', 'A#', 'B', 'C', 'C#', 'D', 'D#', 'E', 'F', 'F#']
        plt.xticks(np.arange(12), notes)
        plt.title('Pitch Class Profile')
        plt.xlabel('Note')
        plt.grid(True)

        plt.figure(2)
        plt.yticks(np.arange(25), self.chords)
        plt.plot(timestamp, id_chord)
        plt.xlabel('Time in seconds')
        plt.ylabel('Chords')
        plt.title('Identified chords')
        plt.grid(True)
        plt.show()
