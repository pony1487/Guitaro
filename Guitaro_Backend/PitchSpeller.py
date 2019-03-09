class PitchSpeller:
    """
    This code is based on Brayn Duggans code for a DT228/2 Object Orientated Programming Example
    https://www.dit.ie/computing/people/academicstaff/staff/staffname161825en.html

    The frequencies cover from the lowest note to the highest on a guitar in standard tuning.
    """

    def __init__(self):
        # E2 to E6: 4 octaves
        # NOTE: Find a better way to do this
        self.frequencies = [82.41, 87.31, 92.50, 98.00, 103.83, 110.00, 116.54, 123.47, 130.81, 138.59, 146.83, 155.56,
                            164.81, 174.61, 185.00, 196.00, 207.65, 220.00, 233.08, 246.94, 261.63, 277.18, 293.66,
                            311.13,
                            329.63, 349.23, 369.99, 392.00, 415.30, 440.00, 466.16, 493.88, 523.25, 554.37, 587.33,
                            622.25,
                            659.25, 698.46, 739.99, 783.99, 830.61, 880.00, 932.33, 987.77, 1046.50, 1108.73, 1174.66,
                            1244.51, 1318.51]
        self.notes = ["E", "F", "F#", "G", "G#", "A", "Bb", "B", "C", "C#", "D", "Eb",
                      "E", "F", "F#", "G", "G#", "A", "Bb", "B", "C", "C#", "D", "Eb",
                      "E", "F", "F#", "G", "G#", "A", "Bb", "B", "C", "C#", "D", "Eb",
                      "E", "F", "F#", "G", "G#", "A", "Bb", "B", "C", "C#", "D", "Eb", "E"]

    def spell(self, frequency):
        """
        This method takes a frequency and finds the index of the value it is closed to in the frequencies list. This
        index is then used to get the corresponding char in the notes list.
        :param frequency:
        :return: the note of corresponding the frequency
        """
        freq_index = 0
        note_index = 0

        for freq in self.frequencies:
            if frequency >= (freq - 4.0) and frequency <= (freq + 4.0):
                note_index = freq_index
                print(str(frequency) + " ", end="")
            freq_index += 1

        return self.notes[note_index]

    def get_num_of_notes_between_notes(self, frequency_a, frequency_b):
        """
        This method takes to frequencies and determines how many frets/steps are between them if there is any.
        :param frequency_a:
        :param frequency_b:
        :return:
        """

        frequency_a_index = 0
        for i in self.frequencies:
            if frequency_a >= (i - 5.0) and frequency_a <= (i + 5.0):
                break
            frequency_a_index += 1

        frequency_b_index = 0
        for i in self.frequencies:
            if frequency_b >= (i - 5.0) and frequency_b <= (i + 5.0):
                break
            frequency_b_index += 1

        print("freq: " + str(frequency_a) + " closet to index: " + str(frequency_a_index))
        print("freq: " + str(frequency_b) + " closet to index: " + str(frequency_b_index))

        if frequency_a_index < frequency_b_index:
            output_str = "frequency_a is {} and is {} notes below frequency_b {}".format(self.notes[frequency_a_index],
                                                                                         frequency_b_index - frequency_a_index,
                                                                                         self.notes[frequency_b_index])
            print(output_str)

        if frequency_a_index > frequency_b_index:
            output_str = "frequency_a is {} and is {} notes above frequency_b {}".format(self.notes[frequency_a_index],
                                                                                         frequency_a_index - frequency_b_index,
                                                                                         self.notes[frequency_b_index])
            print(output_str)

        if frequency_a_index == frequency_b_index:
            output_str = "frequency_a is {} and is the same as frequency_b {}".format(self.notes[frequency_a_index],
                                                                                      self.notes[frequency_b_index])
            print(output_str)

