import sys
import pytest

sys.path.insert(0, '../')

from PitchSpeller import PitchSpeller


class TestPitchSpeller(object):

    def test_spell(self):
        pitch_speller = PitchSpeller()
        note = pitch_speller.spell(220.00)
        assert note == 'A'

    def test_negative_input(self):
        with pytest.raises(Exception):
            pitch_speller = PitchSpeller()
            note = pitch_speller.spell(-1)

    def test_char_as_input(self):
        with pytest.raises(Exception):
            pitch_speller = PitchSpeller()
            note = pitch_speller.spell('A')

    def test_input_larger_than_max_frequency(self):
        with pytest.raises(Exception):
            pitch_speller = PitchSpeller()
            note = pitch_speller.spell(20000.00)
