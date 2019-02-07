import aubio
import itertools

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
        :returns A list of notes
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

        pitch_list_minus_duplicates = self.remove_consecutive_duplicates(pitches)
        return pitch_list_minus_duplicates

    def remove_consecutive_duplicates(self, freq_list):
        """
        This method reduces repeating characters to more accurately represent the notes being played.
        The frequencies in freq_list first converted to the appropriate notes using PitchSpeller.
        The Aubio library method that returns the frequencies that fill the freq_list is constantly checking the frequency
        until the audio is over. This leads to for example multiple A notes being put in the list for the duration of a
        single A note. For example, the notes played could be A B C D and the freq_list after being pitch spelt would be
        something like A A A A A A A A A B B B B B B B B C C C C C C C D D D D D D D. Which is note wrong, but messy to
        look at an gives the impression that the notes were played multiple times as opposed to once each.


        :param freq_list:
        :return:
        """
        pitch_speller = PitchSpeller()
        pitch_spelled_list = []

        for freq in freq_list:
            if freq != 0:
                pitch_spelled_list.append(pitch_speller.spell(freq))

        pitch_list_minus_duplicates = [k for k, g in itertools.groupby(pitch_spelled_list)]

        return pitch_list_minus_duplicates

    def analyse_timing(self):
        pass

    def get_timing_list(self):
        return self.timing_list

    def get_note_list(self):
        return self.note_list

    def test_print_contents(self):
        """
        DELETE WHEN DONE TESTING
        DELETE WHEN DONE TESTING
        :return:
        """
        print("In AudioAnalysis Class")
        print(self.filepath.read())
