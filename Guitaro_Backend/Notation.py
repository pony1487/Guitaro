import numpy as np


class Notation:

    def __init__(self, freqs_in_recording):
        """
        On guitar the same note can be played in two or even three different places. This raises the issue of
        how to determine what frets and what strings were played.
        
        This class gets the fret of the first note played on each string. It uses this fret as a start point to
        determine which notes where played where by limiting notes surrounding it to be not greater than 3 frets
        away. This has the effect of creating "boxes" around where notes where played on the fret board.
        This limits the amount of possible combinations of notes played to a be more like how they are actually
        played on a real fretboard.

        :param freqs_in_recording: An array of note frequencies
        """
        self.strings = [
            [82.41, 87.31, 92.50, 98.00, 103.83, 110.00, 116.54, 123.47, 130.81, 138.59, 146.83, 155.56, 164.81],
            [110.00, 116.54, 123.47, 130.81, 138.59, 146.83, 155.56, 164.81, 174.61, 185.00, 196.00, 207.65, 220.00],
            [146.83, 155.56, 164.81, 174.61, 185.00, 196.00, 207.65, 220.00, 233.08, 246.94, 261.63, 277.18, 293.66],
            [196.00, 207.65, 220.00, 233.08, 246.94, 261.63, 277.18, 293.66, 311.13, 329.63, 349.23, 369.99, 392.00],
            [246.94, 261.63, 277.18, 293.66, 311.13, 329.63, 349.23, 369.99, 392.00, 415.30, 440.00, 466.16, 493.88],
            [329.63, 349.23, 369.99, 392.00, 415.30, 440.00, 466.16, 493.88, 523.25, 554.37, 587.33, 622.25, 659.25]]

        self.fret_frequencies_to_string_number_mapping = {
            "0": "6",
            "1": "5",
            "2": "4",
            "3": "3",
            "4": "2",
            "5": "1"
        }

        self.freqs_in_recording = freqs_in_recording
        self.start_frets = list()

        # init a two d list with Zeros that represents 6 strings and 12 frets per string
        # (13 across to account for the open string)
        self.played_note_locations = [[0 for i in range(13)] for j in range(6)]

        self.__find_played_note_locations()
        self.__get_start_fret_of_each_string()
        self.__find_frets_and_string_of_notes()

    def __find_played_note_locations(self):
        # Fill 2d array with locations of notes played
        for i in range(0, len(self.strings)):
            gtr_string = self.strings[i]

            for j in range(0, len(self.freqs_in_recording)):

                freq = self.freqs_in_recording[j]

                freq = find_nearest(gtr_string, freq)
                # print(freq)

                if freq in gtr_string:
                    fret = gtr_string.index(freq)
                    s = "freq: {} fret: {}".format(freq, fret)
                    # print("i: " + str(i) + " j: " + str(j))
                    self.played_note_locations[i][fret] = 1

    def __get_start_fret_of_each_string(self):
        # Get the first fret played on each string
        for i in range(0, len(self.played_note_locations)):
            for j in range(0, len(self.played_note_locations)):
                if self.played_note_locations[i][j] == 1:
                    self.start_frets.append(j)
                    break

    def __find_frets_and_string_of_notes(self):
        # For each first fret played, find notes that are no more than 3 frets away
        for start_fret in self.start_frets:
            print("-----------------------------")
            for i in range(0, len(self.strings)):
                gtr_string = self.strings[i]

                string_num = self.fret_frequencies_to_string_number_mapping.get(str(i))
                print("\nString number: " + string_num)

                for j in range(0, len(self.freqs_in_recording)):
                    freq = self.freqs_in_recording[j]

                    nearest = find_nearest(gtr_string, freq)

                    if not (nearest - freq) > 5.00:
                        # print(freq)
                        fret_of_note = gtr_string.index(nearest)

                        if fret_of_note >= start_fret and fret_of_note <= start_fret + 3:
                            s = "freq: {} fret: {}: start_fret: {}".format(nearest, fret_of_note, start_fret)
                            print(s)


def find_nearest(array, value):
    """
    Finds the nearest value closest to the value argument in a array
    :param array:
    :param value:
    :return:
    """
    array = np.asarray(array)
    index = (np.abs(array - value)).argmin()
    return array[index]
