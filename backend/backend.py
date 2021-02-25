"""
this class (backend manager):
 - talks to the frontend,
 - interacts with quiz retrieval + evaluation
 - manages the robots emotional states
 - tracks the interaction
"""
from backend.user_evaluator import UserEvaluator
from rapidfuzz import process


class BackendManager:

    def __init__(self, user_evaluator: UserEvaluator = None):
        if user_evaluator is None:
            self.user_evaluator = UserEvaluator()
        else:
            self.user_evaluator = user_evaluator

    def parse_string(string):
        pass


class StringMatcher:

    def __init__(self):
        pass

    @staticmethod
    def find_most_similar_answer(user_answer, answers):
        best_match = process.extractOne(user_answer, answers)
        return best_match


if __name__ == "__main__":
    backend_manager = BackendManager()
    print(backend_manager.user_evaluator.check_user_answer(1, 2))
