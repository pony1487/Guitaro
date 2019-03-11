import numpy as np
from fret_mappings import fret_mappings, strings


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
        self.fret_mappings = fret_mappings
        self.strings = strings

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

        self.strings_to_be_played_list = list()

        self.__find_played_note_locations()
        self.__get_start_fret_of_each_string()
        self.__find_frets_and_string_of_notes()

    def __find_played_note_locations(self):

        # Fill 2d array with locations of notes played
        for i in range(0, len(self.strings)):
            gtr_string = self.strings[i]

            for j in range(0, len(self.freqs_in_recording)):

                freq = self.freqs_in_recording[j]
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

        # Catch if there is just silence submitted
        if self.start_frets:
            # Limit it to just the first "box"
            start_fret = self.start_frets[0]
            for freq in self.freqs_in_recording:

                for string, value in fret_mappings.items():
                    string_dict = fret_mappings.get(string)
                    if string_dict.get(freq):
                        fret_of_freq = string_dict.get(freq)
                        if start_fret <= fret_of_freq <= start_fret + 3:
                            s = "{} {}".format(string, fret_of_freq)
                            self.strings_to_be_played_list.append(string)
                            # print(s)

        else:
            print("Notation.py: start_frets is empty!")

    def get_strings_to_be_played(self):
        return self.strings_to_be_played_list
