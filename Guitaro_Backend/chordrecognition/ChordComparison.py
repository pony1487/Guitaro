class ChordComparison:
    def __init__(self, lesson_name, user_note_list, lesson_note_list):
        self.lesson_name = lesson_name
        self.user_note_list = user_note_list
        self.lesson_note_list = lesson_note_list
        self.comparison_dict = dict()
        self.__init_comparison_json(self.lesson_name)

    def __init_comparison_json(self, lesson_name):
        self.comparison_dict["lesson"] = lesson_name
        self.comparison_dict["user_note_list"] = self.user_note_list
        self.comparison_dict["lesson_note_list"] = self.lesson_note_list
        self.comparison_dict["wrong_notes"] = []
        self.comparison_dict["feedback"] = []

        self.__compare_note_lists()

    def __compare_note_lists(self):
        notes_not_in_lesson = list(set(self.user_note_list) - set(self.lesson_note_list))
        self.comparison_dict["notes_not_in_lesson"] = notes_not_in_lesson

    def get_comparision_dict(self):
        return self.comparison_dict
