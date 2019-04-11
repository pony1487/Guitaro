import sys
import pytest

sys.path.insert(0, '../')

from AudioAnalysis import AudioAnalysis


class TestAudioAnalysis(object):

    def test_analyse_notes(self):
        filepath = "/home/ronan/connollyro@gmail.com/Year4/Semester2/FinalYearProject/FinalYearProject/Guitaro_Backend_Repo/efs/audio/topics/picking/A_minor_pentatonic_ascending_quarter_notes-95.wav"

        audio_analysis = AudioAnalysis(filepath)

        notes, freqs = audio_analysis.analyse_notes()

        expected_notes = ['A', 'C', 'D', 'E', 'G', 'A']
        expected_freqs = [110.0, 130.81, 146.83, 164.81, 196.0, 220.0]

        assert expected_notes == notes and expected_freqs == freqs
