"""
class that captures and evaluates the quizzes that are saved in json format
"""
import json
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent


class JSONParser:

    def __init__(self, path_to_json=os.path.join(BASE_DIR, 'quizzes', 'quizz1.json')):
        self.data = JSONParser.load(path_to_json)

    def reload_data(self, filename):
        path_to_json=os.path.join(BASE_DIR, filename)
        self.data = JSONParser.load(path_to_json)

    def get_question(self, question_id):
        return self.data['questions'][question_id]['question']

    def get_answers(self, question_id):
        return self.data['questions'][question_id]['answers']

    def get_answer(self, question_id, answer_id):
        return self.get_answers(question_id)[answer_id]

    def get_correct_answer(self, question_id):
        # because we start numbering from one in json
        correct_index = self.data['questions'][question_id]['correctIndex'] - 1
        return self.get_answer(question_id, correct_index)

    def get_correct_answer_id(self, question_id):
        # because we start numbering from one in json
        correct_index = self.data['questions'][question_id]['correctIndex'] - 1
        return correct_index

    def get_number_of_questions(self):
        return len(self.data['questions'])

    @staticmethod
    def load(path_to_json):
        with open(path_to_json) as f:
            data = json.load(f)
        return data

    @classmethod
    def from_config(cls):
        return cls()


class UserEvaluator:

    def __init__(self, parser: JSONParser = None):
        if parser is None:
            self.parser = JSONParser.from_config()
        else:
            self.parser = parser

        self.user_answers = {}

    def check_user_answer(self, question_id, user_answer_id):  # we get from user answer_id enumerated from 0
        self.user_answers[question_id] = user_answer_id
        if self.parser.get_correct_answer_id(question_id) == user_answer_id:
            return True
        else:
            return False

    def calculate_score(self):
        number_correct = 0
        for question in self.user_answers.keys():
            if self.check_user_answer(question, self.user_answers[question]):
                number_correct += 1

        # return number_correct/len(self.user_answers)
        return number_correct


if __name__ == "__main__":
    parser = JSONParser(os.path.join('quizzes', 'quizz1.json'))
