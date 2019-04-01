import sys
import pytest

sys.path.insert(0, '../')

from Notation import Notation


class TestNotation(object):

    def test_strings_to_be_played(self):
        freqs_in_recording = [110.0, 130.81, 146.83, 164.81, 196.0, 220.0]

        timing_list = [2.4904987812042236, 3.736825466156006, 4.915533065795898,
                       4.999251842498779, 6.24546480178833, 6.309228897094727,
                       7.552244663238525, 8.79773235321045, 8.856847763061523]
        bpm = 95
        notation = Notation(freqs_in_recording, timing_list, bpm)

        expected_strings = ["E", "E", "A", "A", "D", "D"]
        strings_to_be_played = notation.get_strings_to_be_played()

        assert expected_strings == strings_to_be_played

    def test_strings_to_be_played_bad_input(self):
        freqs_in_recording = [-1, -1]

        timing_list = [-1, -1]
        bpm = 95
        notation = Notation(freqs_in_recording, timing_list, bpm)

        strings_to_be_played = notation.get_strings_to_be_played()

        assert len(strings_to_be_played) == 0

    def test_note_durations(self):
        freqs_in_recording = [110.0, 130.81, 146.83, 164.81, 196.0, 220.0]

        timing_list = [2.488072633743286, 3.783242702484131,
                       4.996575832366943, 6.3053059577941895,
                       7.550408363342285, 8.852245330810547]
        bpm = 95
        notation = Notation(freqs_in_recording, timing_list, bpm)
        padded_duration_list = notation.get_padded_duration_list()

        expected_output = ['half', 'half', 'half', 'half', 'half', 'half']
        assert padded_duration_list == expected_output

    def test_padding_durations(self):
        """
        Six Quarter Notes so it should be padded
        :return:
        """
        freq_list = [110.0, 130.81, 146.83, 164.81, 196.0, 220.0]
        timing_list = [2.511587381362915,
                       3.0793650150299072,
                       3.7543764114379883,
                       4.387029647827148,
                       5.066054344177246,
                       5.673401355743408]

        bpm = 95
        notation = Notation(freq_list, timing_list, bpm)
        padded_duration_list = notation.get_padded_duration_list()

        # 6 quarter notes is six beats. The next bar would be 8 beats so add two beats(half)
        expected_output = ['quarter', 'quarter', 'quarter', 'quarter', 'quarter', 'quarter', 'half']
        assert padded_duration_list == expected_output
