import aubio
import itertools

from numpy import hstack, zeros

from PitchSpeller import PitchSpeller


class AudioAnalysis:

    def __init__(self, filepath):
        self.filepath = filepath
        self.timing_list = []
        self.note_list = []

    def analyse_notes(self):
        """
        Taken from https://github.com/aubio/aubio/tree/master/python/demos and slightly modified
        This uses the pitch method in aubio. It reads the audio file and gives a list of frequencies and the proability
        that it is that note.
        :returns A list of notes and the frequecies of those notes
        """
        downsample = 1
        samplerate = 44100 // downsample

        win_s = 4096 // downsample  # fft size
        hop_s = 512 // downsample  # hop size

        # TAKES A STR ARG FOR THE FILE PATH, NOT THE FILE ITSELF
        s = aubio.source(self.filepath, samplerate, hop_s)
        samplerate = s.samplerate

        tolerance = 0.8

        # uses the yin algorithm to determine pitch
        pitch_o = aubio.pitch("yin", win_s, hop_s, samplerate)
        pitch_o.set_unit("Hz")
        pitch_o.set_tolerance(tolerance)

        pitches = []
        confidences = []

        # total number of frames read
        total_frames = 0
        while True:
            samples, read = s()
            pitch = pitch_o(samples)[0]
            pitch = int(round(pitch))
            confidence = pitch_o.get_confidence()
            # set the threshold high to ignore frequencies such as random string noise before audio start playing
            if confidence < 0.99: pitch = 0.

            pitches += [pitch]
            confidences += [confidence]
            total_frames += read
            if read < hop_s: break

        pitch_list_minus_duplicates,freq_list_minus_duplicates = self.remove_consecutive_duplicates(pitches)
        return pitch_list_minus_duplicates, freq_list_minus_duplicates

    def remove_consecutive_duplicates(self, freq_list):
        """
        This method reduces repeating characters to more accurately represent the notes being played.
        The frequencies in freq_list first converted to the appropriate notes using PitchSpeller.
        The Aubio library method that returns the frequencies that fill the freq_list is constantly checking the frequency
        until the audio is over. This leads to for example multiple A notes being put in the list for the duration of a
        single A note. For example, the notes played could be A B C D and the freq_list after being pitch spelt would be
        something like A A A A A A A A A B B B B B B B B C C C C C C C D D D D D D D. Which is not wrong, but messy to
        look at an gives the impression that the notes were played multiple times as opposed to once each.

        The frequency_list is to be used for Notation. This also has the same issue of duplicates as well as being not
        being an exact frequency in the possible guitar frequencies. For example, the list can have 110,109,111 for an A
        note which is 110hz. The find_nearest function is used in PitchSpeller to find the what this numbers are closest
        to and then duplicates are removed. For example:
        Notes that have been pitch spelled:
        ['A', 'C', 'D', 'E', 'G']

        This is the list that of freqs that was used to generate the above list.
        [111, 110, 133, 132, 131, 148, 147, 166, 165, 197, 196, 197, 196]

        After finding the nearest value in the guitar frequency list would become

        [110.0, 110.0, 130.81, 130.81, 130.81, 146.83, 146.83, 164.81, 164.81, 196.0, 196.0, 196.0, 196.0]

        and then when de-duplicated

        [110.0, 130.81, 146.83, 164.81, 196.0]

        :param freq_list:
        :return: list containing the notes(pitches) and a list containing the frequencies
        """
        pitch_speller = PitchSpeller()
        pitch_spelled_list = []
        freq_list_minus_zeros = []

        # remove zeros that are added if the confidence from the above analyse_notes() < 0.99
        for freq in freq_list:
            if freq != 0:
                pitch_spelled_list.append(pitch_speller.spell(freq))
                freq_list_minus_zeros.append(freq)

        pitch_list_minus_duplicates = [k for k, g in itertools.groupby(pitch_spelled_list)]

        freq_list_minus_duplicates = pitch_speller.find_nearest_and_dedup_freq_list(freq_list_minus_zeros)
        return pitch_list_minus_duplicates,freq_list_minus_duplicates

    def analyse_timing(self):
        """
        Taken directly from here:
        https://github.com/aubio/aubio/blob/master/python/demos/demo_onset_plot.py

        However the threshold is set different to compensate for the different signal level of the microphone compared
        to the direct signal
        :return: A list of seconds when onset occurs
        """

        win_s = 512  # fft size
        hop_s = win_s // 2  # hop size

        filename = self.filepath

        samplerate = 0

        s = aubio.source(filename, samplerate, hop_s)
        samplerate = s.samplerate
        o = aubio.onset("default", win_s, hop_s, samplerate)

        # One threshold does not seem to work for all cases
        o.set_threshold(0.45)

        # list of when peaks happen at time t(seconds)
        onset_time_list = []
        # list of onsets, in samples
        onsets = []

        # storage for plotted data
        desc = []
        tdesc = []
        allsamples_max = zeros(0, )
        downsample = 2  # to plot n samples / hop_s

        # total number of frames read
        total_frames = 0
        while True:
            samples, read = s()

            if o(samples):
                # print("%f" % (o.get_last_s()))
                onset_time_list.append(o.get_last_s())
                onsets.append(o.get_last())
            # keep some data to plot it later
            new_maxes = (abs(samples.reshape(hop_s // downsample, downsample))).max(axis=0)
            allsamples_max = hstack([allsamples_max, new_maxes])
            desc.append(o.get_descriptor())
            tdesc.append(o.get_thresholded_descriptor())
            total_frames += read
            if read < hop_s: break

        return onset_time_list

    def get_timing_list(self):
        return self.timing_list

    def get_note_list(self):
        return self.note_list
