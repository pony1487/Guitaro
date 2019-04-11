from FileManager import FileManager
import json


class PracticeGenerator:
    def __init__(self, topic):
        self.topic_path = "topic/{}".format(topic)
        self.file_manager = FileManager(self.topic_path)

    def get_random_lesson_names(self):
        files_str = self.file_manager.list_files_in_directory()
        files_dict = json.loads(files_str)
        # Get the number of files in a topic and use it to get random file names
        print(len(files_dict.get("files")))

    def get_topic_path(self):
        print(self.topic_path)
