class AudioAnalysis:
    """
    Use this class like this:

    with open('my_file.txt', 'r') as f:
        a = AudioAnalysis(f)

    OR

    f = open("path/to/file")
    a = AudioAnalysis(f)

    """

    def __init__(self, file):
        self.file = file
        self.timing_list = []
        self.note_list = []

    def analyse_notes(self):
        pass

    def analyse_timing(self):
        pass

    def get_timing_list(self):
        return self.timing_list

    def get_note_list(self):
        return self.note_list

    def test_print_contents(self):
        """
        DELETE WHEN DONE TESTING
        DELETE WHEN DONE TESTING
        :return:
        """
        print("In AudioAnalysis Class")
        print(self.file.read())
