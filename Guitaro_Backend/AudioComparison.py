class AudioComparison:

    def __init__(self, lesson_name, lesson_note_list, lesson_timing_list, user_note_list, user_timing_list, bpm,
                 user_string_list, user_fret_list, user_duration_list,total_beats):
        self.lesson_name = lesson_name
        self.lesson_note_list = lesson_note_list
        self.lesson_timing_list = lesson_timing_list

        self.user_note_list = user_note_list
        self.user_timing_list = user_timing_list
        self.bpm = int(bpm)

        self.user_string_list = user_string_list
        self.user_fret_list = user_fret_list
        self.user_duration_list = user_duration_list

        self.total_beats = total_beats

        self.comparison_dict = dict()
        self.__init_comparison_json(self.lesson_name)

    def __init_comparison_json(self, lesson_name):
        self.comparison_dict["lesson"] = lesson_name
        self.comparison_dict["lesson_tempo"] = self.bpm
        self.comparison_dict["user_note_list"] = self.user_note_list
        self.comparison_dict["user_timing_list"] = self.user_timing_list
        self.comparison_dict["lesson_note_list"] = self.lesson_note_list
        self.comparison_dict["lesson_timing_list"] = self.lesson_timing_list

        self.comparison_dict["wrong_note_indexes"] = []
        self.comparison_dict["notes_not_in_lesson"] = []
        self.comparison_dict["feedback"] = []
        self.comparison_dict["percentage_difference"] = []

        self.comparison_dict["user_string_list"] = self.user_string_list
        self.comparison_dict["user_fret_list"] = self.user_fret_list
        self.comparison_dict["user_duration_list"] = self.user_duration_list

        self.comparison_dict["total_beats"] = self.total_beats

        self.__compare_note_lists()
        self.__compare_timing_lists()

    def __compare_note_lists(self):
        list_of_note_indexes = []
        expected_len_of_list = len(self.lesson_note_list)
        counter = 0

        # check if the list is empty. Its empty if the there is just background noise submitted
        if self.user_note_list and self.lesson_note_list:
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
            print("AudioComparision.py: user_note_list is empty. len of submited user list: " + str(
                len(self.user_note_list)))

    def __compare_timing_lists(self):
        """

        :return: A list containing the percentage difference of notes. Each index is a note
        """
        percent_list = []

        # Only compare timing if there were actual notes played by user.
        if self.user_timing_list and self.lesson_timing_list:
            for i in range(0, len(self.lesson_timing_list)):
                if i > len(self.user_timing_list) - 1:
                    break
                diff = self.__get_percentage_difference_of_timing(self.user_timing_list[i], self.lesson_timing_list[i])
                percent_list.append(diff)

            self.comparison_dict["percentage_difference"] = percent_list
            return percent_list
        else:
            print("AudioComparison.py: user_note_list is empty!")

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

    def get_comparision_dict(self):
        return self.comparison_dict
