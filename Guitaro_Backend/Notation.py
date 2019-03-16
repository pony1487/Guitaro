import numpy as np
from fret_mappings import fret_mappings, strings, number_of_beats_dictionary


class Notation:

    def __init__(self, freqs_in_recording, timing_list, bpm):
        """
        On guitar the same note can be played in two or even three different places. This raises the issue of
        how to determine what frets and what strings were played.

        This class gets the fret of the first note played on each string. It uses this fret as a start point to
        determine which notes where played where by limiting notes surrounding it to be not greater than 3 frets
        away. This has the effect of creating "boxes" around where notes where played on the fret board.
        This limits the amount of possible combinations of notes played to a be more like how they are actually
        played on a real fretboard.

        Currently, it is limited to the first note it encounters to set the "box". To show alternative ways to play
        the same thing, loop through each number in start frets

        :param freqs_in_recording: An array of note frequencies
        """
        self.fret_mappings = fret_mappings
        self.strings = strings
        self.bpm = int(bpm)
        self.number_of_beats_dictionary = number_of_beats_dictionary
        self.timing_list = timing_list

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
        self.frets_to_be_played_list = list()

        # Get frets and strings
        self.__find_played_note_locations()
        self.__get_start_fret_of_each_string()
        self.__find_frets_and_strings_of_notes()

        # Get durations of notes
        self.duration_list = self.__get_note_durations_of_timing_list(self.timing_list)
        self.padded_duration_list = self.__pad_note_durations(self.duration_list)

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
            string = self.played_note_locations[i]

            for j in range(0, len(string)):
                if string[j] == 1:
                    self.start_frets.append(j)
                    break

    def __find_frets_and_strings_of_notes(self):

        # Catch if there is just silence submitted
        if self.start_frets:
            # Limit it to just the first "box"
            start_fret = self.start_frets[0]
            for freq in self.freqs_in_recording:

                for string, value in fret_mappings.items():
                    string_dict = fret_mappings.get(string)
                    if string_dict.get(freq):
                        fret_of_freq = string_dict.get(freq)
                        # Between one fret below and 3 frets above
                        if start_fret - 1 <= fret_of_freq <= start_fret + 3:
                            self.strings_to_be_played_list.append(string)
                            self.frets_to_be_played_list.append(fret_of_freq)

        else:
            print("Notation.py: start_frets is empty! Silence being submitted is probable cause")

    def __get_note_durations_of_timing_list(self, arr):
        """
        Gets the difference in time between each consecutive note in a note timing list and will find determine the
        duration name ie half, whole, quater etc

        NOTE: The duration is gotten by substracting the next note from the current note. This wont work for the last
        note as there is no note following the current note. I set every last note to be the same as the
        second last note as it doesnt really matter how long it lasts and this makes it easier to notate it.
        :param arr:
        :param bpm:
        :return:
        """
        # duration_name = ["whole", "half", "quarter", "eight", "sixteenth", "thirty_second"]
        duration_name = ["whole", "half", "quarter", "eight", "sixteenth"]

        note_durations = self.__get_note_duration_given_tempo(self.bpm)

        return_list = list()

        for i in range(0, len(arr) - 1):
            diff = arr[i + 1] - arr[i]
            duration, index = self.__find_nearest(note_durations, diff)
            duration = float(duration)
            duration_index = note_durations.index(duration)
            return_list.append(duration_name[duration_index])

        # we assume that the last note played is always the same duration as the one that came before it.
        # The last note generally is just let ring out. It doesnt really matter how long it rings out for.
        # For the notation to work, there needs to be a duration for the last note. I set every last note played
        # to be same as the second last
        if return_list:
            second_last_note_duration = return_list[-1]
            return_list.append(second_last_note_duration)

        return return_list

    def __get_note_duration_given_tempo(self, bpm):
        """
        Assume that their are only 6 possible values. More can be added for faster notes. ie 32nd note
        So to get the note name index is:
        0 = whole
        1 = half
        2 = quarter
        3 = eight
        4 = sixteen
        5 = 32nd note
        """
        whole_note = 4 * (60 / bpm)
        half_note = 2 * (60 / bpm)
        quarter_note = 60 / bpm  # 0.5
        eight_note = 0.5 * (60 / bpm)  # 0.25
        sixteenth_note = 0.25 * (60 / bpm)
        # thirty_second_note = 0.125 * (60 / bpm)

        duration_list = list()
        duration_list.append(whole_note)
        duration_list.append(half_note)
        duration_list.append(quarter_note)
        duration_list.append(eight_note)
        duration_list.append(sixteenth_note)
        # duration_list.append(thirty_second_note)

        return duration_list

    def __find_nearest(self, array, value):
        """
        Stackoverflow used for this. https://stackoverflow.com/questions/2566412/find-nearest-value-in-numpy-array
        :param array: contain the durations of the whole,half,quarter etc notes based on tempo give
        :param value: The difference between two consecutive notes. ie Note B - A gives A's length which is then check
        against the note durations calculated from the tempo
        :return:
        """
        array = np.asarray(array)
        index = (np.abs(array - value)).argmin()
        return array[index], index

    def __pad_note_durations(self, arr):

        total_beats = self.calculate_total_beats(arr)
        print("total_beats: " + str(total_beats))
        # If there is not the correct amount of notes to fill a bar pad it whatever durations add up to make a full bar
        if total_beats % 4 != 0:
            next_multiple_of_four = total_beats + (4 - total_beats % 4)
            print("next_multiple_of_four: " + str(next_multiple_of_four))

            diff = next_multiple_of_four - total_beats
            print("diff: " + str(diff))
            for key, val in self.number_of_beats_dictionary.items():
                if val <= diff:
                    diff = diff % val

                    arr.append(key)
            print("arr padded: " + str(arr))
            return arr
        else:
            print("arr not padded: " + str(arr))
            return arr

    def calculate_total_beats(self, arr):
        total_beats = 0
        for i in arr:
            total_beats += self.number_of_beats_dictionary.get(i)
        return total_beats

    def get_strings_to_be_played(self):
        return self.strings_to_be_played_list

    def get_frets_to_be_played(self):
        return self.frets_to_be_played_list

    def get_duration_list(self):
        return self.duration_list

    def get_padded_duration_list(self):
        return self.padded_duration_list
