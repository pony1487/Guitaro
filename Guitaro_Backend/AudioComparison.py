import numpy as np


class AudioComparison:

    def __init__(self, lesson_name, lesson_note_list, lesson_timing_list, user_note_list, user_timing_list, bpm,
                 lesson_string_list, user_string_list,lesson_fret_list,user_fret_list):
        self.lesson_name = lesson_name
        self.lesson_note_list = lesson_note_list
        self.lesson_timing_list = lesson_timing_list

        self.user_note_list = user_note_list
        self.user_timing_list = user_timing_list
        self.bpm = int(bpm)

        self.lesson_string_list = lesson_string_list
        self.user_string_list = user_string_list

        self.lesson_fret_list = lesson_fret_list
        self.user_fret_list = user_fret_list

        self.comparison_dict = dict()
        self.__init_comparison_json(self.lesson_name)

    def __init_comparison_json(self, lesson_name):
        self.comparison_dict["lesson"] = lesson_name
        self.comparison_dict["lesson_tempo"] = self.bpm
        self.comparison_dict["user_note_list"] = self.user_note_list
        self.comparison_dict["user_timing_list"] = self.user_timing_list
        self.comparison_dict["lesson_note_list"] = self.lesson_note_list
        self.comparison_dict["lesson_timing_list"] = self.lesson_timing_list
        self.comparison_dict["lesson_string_list"] =  self.lesson_string_list
        self.comparison_dict["user_string_list"] =  self.user_string_list

        self.comparison_dict["lesson_fret_list"] = self.lesson_fret_list
        self.comparison_dict["user_fret_list"] = self.user_fret_list

        self.comparison_dict["wrong_note_indexes"] = []
        self.comparison_dict["notes_not_in_lesson"] = []
        self.comparison_dict["feedback"] = []
        self.comparison_dict["percentage_difference"] = []
        self.comparison_dict["lesson_note_durations"] = self.__get_note_durations_of_timing_list(self.lesson_timing_list)
        self.comparison_dict["user_note_durations"] = self.__get_note_durations_of_timing_list(self.user_timing_list)

        """
        # TODO Move this check to the actual functions so it can return some data to the client. This check will return nothing
        if self.user_note_list and self.user_timing_list:
            self.__compare_note_lists()
            self.__compare_timing_lists()
        else:
            print("user_note_list or user_timing_list is empty!")
        """
        self.__compare_note_lists()
        self.__compare_timing_lists()

    def __compare_note_lists(self):
        list_of_note_indexes = []
        expected_len_of_list = len(self.lesson_note_list)
        counter = 0

        # check if the list is empty. Its empty if the there is just background noise submitted
        if self.user_note_list:
            # Determine the index of the incorrect note
            while counter < expected_len_of_list:
                if counter == len(self.user_note_list):
                    print("You didnt play the correct number of notes!")
                    break
                if self.lesson_note_list[counter] != self.user_note_list[counter]:
                    list_of_note_indexes.append(counter)
                counter += 1

            # Display the position of the note that the user played wrong
            for i in range(0, len(self.lesson_note_list)):
                if i in list_of_note_indexes:
                    # i + 1 so user doesn't have to start counting at 0
                    feedback_str = "The {} note was meant to be a {}, You played a {}".format(i + 1,
                                                                                              self.lesson_note_list[i],
                                                                                              self.user_note_list[i])
                    self.comparison_dict["feedback"].append(feedback_str)

            self.comparison_dict["wrong_note_indexes"] = list_of_note_indexes

            notes_not_in_lesson = list(set(self.user_note_list) - set(self.lesson_note_list))
            self.comparison_dict["notes_not_in_lesson"] = notes_not_in_lesson
        else:
            print("AudioComparision.py: user_note_list is empty. len of submited user list: " + str(len(self.user_note_list)))

    def __compare_timing_lists(self):
        """

        :return: A list containing the percentage difference of notes. Each index is a note
        """
        percent_list = []

        if self.user_timing_list:
            for i in range(0, len(self.lesson_timing_list)):
                if i > len(self.user_timing_list) - 1:
                    break
                diff = self.__get_percentage_difference_of_timing(self.user_timing_list[i], self.lesson_timing_list[i])
                percent_list.append(diff)

            self.comparison_dict["percentage_difference"] = percent_list
            return percent_list
        else:
            print("user_timing_list is empty!")

    def __get_percentage_difference_of_timing(self, user_note_time, lesson_note_time):
        """
        Takes a single note time from the users attempt and the lesson and finds the percentage increase or decrease
        Positive float note has been played to late
        Negative float note has been played to soon
        :param user_note_time:
        :param lesson_note_time:
        :return:
        """

        if lesson_note_time != 0:
            if user_note_time >= lesson_note_time:
                difference = user_note_time - lesson_note_time
                percent = difference / lesson_note_time * 100
                return percent
            else:
                difference = lesson_note_time - user_note_time
                percent = difference / lesson_note_time * 100
                return percent * -1

    def __get_note_durations_of_timing_list(self, arr):
        """
        Gets the difference in time between each consecutive note in a note timing list and will find determine the
        duration name ie half, whole, quater etc
        :param arr:
        :param bpm:
        :return:
        """
        duration_name = ["whole", "half", "quarter", "eight", "sixteen"]

        note_durations = self.__get_note_duration_given_tempo(self.bpm)

        return_list = list()

        for i in range(0, len(arr) - 1):
            diff = arr[i + 1] - arr[i]
            duration, index = self.__find_nearest(note_durations, diff)
            duration = float(duration)
            duration_index = note_durations.index(duration)
            return_list.append(duration_name[duration_index])

        return return_list

    def __get_note_duration_given_tempo(self, bpm):
        """
        Assume that their are only 5 possible values. More can be added for faster notes. ie 32nd note
        So to get the note name index is:
        0 = whole
        1 = half
        2 = quarter
        3 = eight
        4 = sixteen
        """
        whole_note = 4 * (60 / bpm)
        half_note = 2 * (60 / bpm)
        quarter_note = 60 / bpm  # 0.5
        eight_note = 0.5 * (60 / bpm)  # 0.25
        sixteenth_note = 0.25 * (60 / bpm)

        duration_list = list()
        duration_list.append(whole_note)
        duration_list.append(half_note)
        duration_list.append(quarter_note)
        duration_list.append(eight_note)
        duration_list.append(sixteenth_note)

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

    def get_comparision_dict(self):
        return self.comparison_dict
