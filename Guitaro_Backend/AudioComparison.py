class AudioComparison:

    def __init__(self, lesson_name, lesson_note_list, lesson_timing_list, user_note_list, user_timing_list):
        self.lesson_name = lesson_name
        self.lesson_note_list = lesson_note_list
        self.lesson_timing_list = lesson_timing_list

        self.user_note_list = user_note_list
        self.user_timing_list = user_timing_list

        self.comparison_dict = dict()
        self.__init_comparison_json(self.lesson_name)

    def __init_comparison_json(self, lesson_name):
        self.comparison_dict["lesson"] = lesson_name
        self.comparison_dict["user_note_list"] = self.user_note_list
        self.comparison_dict["user_timing_list"] = self.user_timing_list
        self.comparison_dict["lesson_note_list"] = self.lesson_note_list
        self.comparison_dict["lesson_timing_list"] = self.lesson_timing_list
        self.comparison_dict["wrong_note_indexes"] = []
        self.comparison_dict["notes_not_in_lesson"] = []
        self.comparison_dict["feedback"] = []
        self.comparison_dict["percentage_difference"] = []

        self.__compare_note_lists()
        self.__compare_timing_lists()

    def __compare_note_lists(self):
        list_of_note_indexes = []
        expected_len_of_list = len(self.lesson_note_list)
        counter = 0

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

    def __compare_timing_lists(self):
        """

        :return: A list containing the percentage difference of notes. Each index is a note
        """
        percent_list = []

        for i in range(0, len(self.lesson_timing_list)):
            if i > len(self.user_timing_list):
                break
            diff = self.__get_percentage_difference_of_timing(self.user_timing_list[i], self.lesson_timing_list[i])
            percent_list.append(diff)

        self.comparison_dict["percentage_difference"] = percent_list
        return percent_list

    def __get_percentage_difference_of_timing(self, user_note_time, lesson_note_time):
        """
        Takes a single note time from the users attempt and the lesson and finds the percentage increase or decrease
        Positive float note has been played to late
        Negative float note has been played to soon
        :param user_note_time:
        :param lesson_note_time:
        :return:
        """

        if user_note_time >= lesson_note_time:
            difference = user_note_time - lesson_note_time
            percent = difference / lesson_note_time * 100
            return percent
        else:
            difference = lesson_note_time - user_note_time
            percent = difference / lesson_note_time * 100
            return percent * -1

    def __get_note_duration_difference(self, user_note_time, lesson_note_time, tempo):
        """
        TO DO

        """

        quarter_note = 60 / tempo  # 0.5
        eight_note = 0.5 * (60 / tempo)  # 0.25
        sixteenth_note = 0.25 * (60 / tempo)
        thirty_second_note = 0.125 * (60 / tempo)

        # print(quarter_note)
        # print(eight_note)
        # Played too fast
        if user_note_time >= lesson_note_time:
            difference = user_note_time - lesson_note_time
            print("Too fast: ", difference)
            if eight_note <= difference <= quarter_note:
                print("quarter_note fast: ", difference)
            if quarter_note <= difference <= sixteenth_note:
                print("sixteenth fast: ", difference)
            if sixteenth_note <= difference <= thirty_second_note:
                print("32nd fast: ", difference)

        else:  # Played too slow
            difference = lesson_note_time - user_note_time
            print("Too Slow: ", difference)
            if quarter_note <= difference <= eight_note:
                print("quarter note off")

    def get_comparision_dict(self):
        return self.comparison_dict
