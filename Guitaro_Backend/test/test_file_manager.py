import sys
import pytest

sys.path.insert(0, '../')

from FileManager import FileManager


class TestFileManager(object):

    def test_list_directories(self):
        directory = "topics"
        file_manager = FileManager(directory)

        dir_list = file_manager.list_directories()

        expected_output = {'directories': ['fingerIndependence', 'strumming', 'picking']}
        assert dir_list == expected_output

    def test_list_directories_bad_input(self):
        with pytest.raises(Exception):
            directory = "directory_that_doesnt_exist"
            file_manager = FileManager(directory)

            dir_list = file_manager.list_directories()

    def test_get_tempo_from_file_name(self):
        directory = "topics"
        lesson_name = "A_minor_pentatonic_ascending_quarter_notes-95.wav"

        file_manager = FileManager(directory)

        bpm = file_manager.get_tempo_from_file_name(lesson_name)

        assert bpm == '95'

    def test_get_tempo_from_file_name_bad_input(self):
        directory = "topics"
        lesson_name = "A_minor_pentatonic_ascending_quarter_notes95.wav"

        file_manager = FileManager(directory)

        bpm = file_manager.get_tempo_from_file_name(lesson_name)

        assert not bpm
