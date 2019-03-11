from os import listdir, path
from os.path import isfile, join
import json


class FileManager:
    def __init__(self, directory):
        self.base_path = path.dirname(__file__)
        self.audio_path = path.abspath(path.join(self.base_path, "..", "efs/audio"))
        self.sub_dir = path.join(self.audio_path, directory)

    def list_directories(self):
        """

        :return: dict containing directory names. This is jsonified to be sent back to client
        """
        directory_dict = dict()
        directory_dict["directories"] = []

        directory_list = listdir(self.sub_dir)

        for directory in directory_list:
            directory_dict["directories"].append(directory)

        return directory_dict

    def list_files_in_directory(self):
        """
        Creates a dictionary to store file names from a directory.
        :return: dict containing directory names. This is jsonified to be sent back to client
        """
        lesson_file_dict = dict()
        lesson_file_dict["files"] = []

        directory_list = listdir(self.sub_dir)
        for directory in directory_list:
            if isfile(join(self.sub_dir, directory)):
                lesson_file_dict["files"].append(directory)

        return lesson_file_dict

    def get_lesson_path(self, lesson_name):
        return self.sub_dir + lesson_name

    def get_base_path(self):
        return str(self.sub_dir)

    def get_tempo_from_file_name(self, lesson_name):
        if "-" in lesson_name:
            # Remove the .wav
            lesson_name_without_ext = lesson_name[:-4]
            # The bpm is always after the dash -
            bpm = lesson_name_without_ext.split('-')[1]
            return bpm
        else:
            error_str = "Error: Not valid filename. Filename should be <name-tempo.wav> format. Recieved: \'{}\'".format(
                lesson_name)
            print(error_str)
