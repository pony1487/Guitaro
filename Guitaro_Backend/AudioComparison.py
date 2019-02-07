class AudioComparison:

    def __init__(self, lesson_note_list, lesson_timing_list, user_note_list, user_timing_list):
        self.lesson_note_list = lesson_note_list
        self.lesson_timing_list = lesson_timing_list

        self.user_note_list = user_note_list
        self.user_timing_list = user_timing_list

    def compare_note_lists(self):
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
                print("The {} note was meant to be a {}, You played a {}".format(i + 1, self.lesson_note_list[i],
                                                                                 self.user_note_list[i]))

        print("List indexes of wrong played notes")
        print(list_of_note_indexes)

        print("Notes that dont match original")
        print(set(self.user_note_list) - set(self.lesson_note_list))

    def compare_timing_lists(self):
        for i in range(0, len(self.lesson_timing_list)):
            if i > len(self.user_timing_list):
                break
            print(abs(self.lesson_timing_list[i] - self.user_timing_list[i]), end='')

        return ""
