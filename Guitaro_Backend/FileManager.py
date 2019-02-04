from os import listdir
from os.path import isfile, join
import json


class FileManager:
    def __init__(self, directory):
        self.root = "audio/"
        self.directory = self.root + directory

    def list_directories(self):
        """

        :return: string representation of the json containing directories
        """
        directory_dict = dict()
        directory_dict["directories"] = []

        directory_list = listdir(self.directory)

        for dir in directory_list:
            directory_dict["directories"].append(dir)

        return json.dumps(directory_dict)

    def list_files_in_directory(self):
        """
        Creates a dictionary to store file names from a directory.
        :return: string representation of the json containing filenames(lessons)
        """
        lesson_file_dict = dict()
        lesson_file_dict["files"] = []

        directory_list = listdir(self.directory)
        for dir in directory_list:
            if isfile(join(self.directory, dir)):
                lesson_file_dict["files"].append(dir)

        return json.dumps(lesson_file_dict)
