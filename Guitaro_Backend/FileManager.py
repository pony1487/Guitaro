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

        :return: string representation of the json containing directories
        """
        directory_dict = dict()
        directory_dict["directories"] = []

        directory_list = listdir(self.sub_dir)

        for directory in directory_list:
            directory_dict["directories"].append(directory)

        return json.dumps(directory_dict)

    def list_files_in_directory(self):
        """
        Creates a dictionary to store file names from a directory.
        :return: string representation of the json containing filenames(lessons)
        """
        lesson_file_dict = dict()
        lesson_file_dict["files"] = []

        directory_list = listdir(self.sub_dir)
        for directory in directory_list:
            if isfile(join(self.sub_dir, directory)):
                lesson_file_dict["files"].append(directory)

        return json.dumps(lesson_file_dict)

    def get_lesson_path(self, lesson_name):
        return self.sub_dir + lesson_name

    def get_base_path(self):
        return str(self.sub_dir)
