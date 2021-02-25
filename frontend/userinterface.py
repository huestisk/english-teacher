# import kivy modules
from kivy.app import App
from kivy.config import Config
from kivy.core.window import Window
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.bubble import Bubble
from kivy.properties import StringProperty, NumericProperty, ObjectProperty, BooleanProperty
from kivy.clock import Clock

# import other modules
import os
import time
import threading
from frontend.text2speech import Text2Speech
from frontend.speech2text import SpeechRecognizer
from backend.backend import StringMatcher
from backend.user_evaluator import UserEvaluator, JSONParser

Config.set('graphics', 'resizable', True)
Config.set('kivy', 'exit_on_escape',  1)

DEBUG = False
SHOW_QUESTION = False

class SpeechBubble(Bubble):
    """ Speech Bubble Class """
    pass


class ContainerBox(FloatLayout):
    """ Layout Class """

    # change_to_sad = BooleanProperty(False)
    # change_to_happy = BooleanProperty(False)

    def __init__(self, **kwargs):
        super(ContainerBox, self).__init__(**kwargs)
        Window.bind(on_key_down=self._on_keyboard_down)
        self.speechBubb = SpeechBubble()
        self.speaking_thread = threading.Thread()
        self.thread_count = 0
        self.next_thread = 0
        self.robot_is_sad = False

    def _on_keyboard_down(self, instance, keyboard, keycode, text, modifiers):
        if self.text_field.focus and keycode == 40:  # Enter key pressed
            self.keyboard_input()
        elif not self.text_field.focus and keycode == 32:  # Space bar pressed
            self.voice_input()

    def speak(self, text, thread_num, happy=True):
        if self.thread_count > 0:
            self.speaking_thread.join()
            time.sleep(0.2)

        if thread_num != self.next_thread:
            time.sleep(1)  # pause and retry
            self.speak(text, thread_num, happy)
        
        elif thread_num < self.next_thread:
            return # kill the thread

        elif self.speaking_thread:
            self.speaking_thread = threading.Thread(target=self.speaker.say, args=[text])
            self.speaking_thread.start()

            if happy:
                self.robot_is_sad = False
            else:
                self.robot_is_sad = True

            self.speechBubb.sb.text = text
            threading.Thread(target=self.show_bubble).start()

            self.next_thread += 1

    def speak_without_bubble(self, text, thread_num):
        if self.thread_count > 0:
            self.speaking_thread.join()
            time.sleep(0.2)

        if thread_num != self.next_thread:
            time.sleep(1)  # pause and retry
            self.speak_without_bubble(text, thread_num)
        
        elif thread_num < self.next_thread:
            return # kill the thread

        elif self.speaking_thread:
            question_title = text.split("\n")[0]
            self.speaking_thread = threading.Thread(target=self.speaker.say, args=[text])
            self.speaking_thread.start()

            if question_title != "I'm listening.":
                self.speechBubb.sb.text = question_title
                threading.Thread(target=self.show_bubble).start()

            self.next_thread += 1

    def show_answers(self, answers, thread_num):
        if self.next_thread > 0:
            self.speaking_thread.join()
            time.sleep(0.5)

        if (thread_num != self.next_thread) or (self.speaking_thread and self.speaking_thread.isAlive()):
            time.sleep(1)  # pause and retry
            self.show_answers(answers, thread_num)

        elif thread_num < self.next_thread:
            return # kill the thread

        elif self.speaking_thread:
            fulltext = ""
            for idx, answer in enumerate(answers):
                if idx == 0:
                    fulltext += str(idx + 1) + ". " + answer
                else:
                    fulltext += "\n" + str(idx + 1) + ". " + answer
            
            self.speechBubb.sb.text = fulltext
            threading.Thread(target=self.show_bubble).start()
            self.next_thread += 1


    def show_bubble(self, *l):
        try:
            self.add_widget(self.speechBubb)
        except:
            self.rm_bubble()
            self.show_bubble()

    def rm_bubble(self, *l):
        try:
            self.remove_widget(self.speechBubb)
        except:
            pass

    def keyboard_input(self):
        pass

    def voice_input(self, *args):
        pass

    def next_question(self, button=False):
        pass

    def prev_question(self, button=False):
        pass

    def change_to_sad(self):
        # BUG: black square because call needs to be on main thread by is currently on side thread
        self.robot.source = 'frontend/images/sad_robot.jpg'

    def change_to_happy(self):
        self.robot.source = 'frontend/images/robot.png'


class LogicClass(ContainerBox):
    """ Logic Class """

    # definition of properties necessary for evaluation events
    input_text = StringProperty('')  # for voice and keyboard input
    question_id = NumericProperty(-1)  # because it is upgraded by one at the start()

    # for 3 different apps
    text_button = ObjectProperty()
    text_field = ObjectProperty()
    voice_button = ObjectProperty()

    def __init__(self, type_of_app, **kwargs):
        # Inherit
        super(LogicClass, self).__init__(**kwargs)
        self.type_of_app = type_of_app

        # Front-end
        self.speaker = Text2Speech()
        self.speech_recognizer = SpeechRecognizer.from_config()

        self.speech_parser = JSONParser()

        if DEBUG:
            self.speech_parser.reload_data('frontend/speech1.json')
        else:
            self.speech_parser.reload_data('frontend/speech.json')

        # Back-end
        self.user_evaluator = UserEvaluator()
        self.string_matcher = StringMatcher()
        self.parser = self.user_evaluator.parser

        if DEBUG:
            self.user_evaluator.parser.reload_data('quizzes/quizz_debug.json')

        # Parameters
        self.number_of_questions = self.parser.get_number_of_questions()
        # scheduling questions
        self.ask_next_question = True

        # label with number of questions
        self.label.text = f"Question {1}/{self.user_evaluator.parser.get_number_of_questions()}"

        # disable score button till user not reached final question
        self.score_button.disabled = True

        # based on type_of_app we disable some widgets
        if self.type_of_app == 1:
            self.text_button.height, self.text_button.size_hint_y, self.text_button.opacity, self.text_button.disabled = 0, None, 0, True
            self.text_field.height, self.text_field.size_hint_y, self.text_field.opacity, self.text_field.disabled = 0, None, 0, True
        elif self.type_of_app == 2:
            self.voice_button.height, self.voice_button.size_hint_y, self.voice_button.opacity, self.voice_button.disabled = 0, None, 0, True

        # Other
        self.user_answer_id = -1

    def on_start(self):
        # intro based on type_of_app
        if self.type_of_app == 1:
            self.intro = self.speech_parser.data['intro_voice']
        elif self.type_of_app == 2:
            self.intro = self.speech_parser.data['intro_keyboard']
        elif self.type_of_app == 3:
            self.intro = self.speech_parser.data['intro_mixed']

        for sentence in self.intro:
            self.speak(sentence, self.thread_count)
            self.thread_count += 1

        self.schedule_next_question()

    def keyboard_input(self):
        """Evaluate the keyboard input"""
        self.input_text = self.text_field.text  # to verify the answer
        self.text_field.text = ''

    def voice_input(self, *args):
        """Evaluate the voice input"""
        self.prompt_voice_input()
        response = self.speech_recognizer.recognize_speech_from_mic()
        while response['error'] is not None or response['transcription'] is None:
            if response['error'] == "API unavailable":
                pass  # TODO: probably close program and give message
            else:
                self.prompt_voice_input(louder=True)

            response = self.speech_recognizer.recognize_speech_from_mic()

        self.input_text = response['transcription']

    def next_question(self, button=False):
        """Move to next question"""
        if button: # BUG: leaves some dead threads
            self.thread_count += 1
            self.next_thread = self.thread_count

        if self.number_of_questions - 1 == self.question_id:
            self.question_id = 0
        else:
            self.question_id += 1

        if self.question_id > 0:
            transition = self.speech_parser.data['transition'][0]
            threading.Thread(target=self.speak, args=[transition, self.thread_count]).start()
            self.thread_count += 1

        self.update_label()
        self.ask_question()

    def prev_question(self, button=False):
        """Move to previous question"""
        if button: # BUG: leaves some dead threads
            self.thread_count += 1
            self.next_thread = self.thread_count

        if self.question_id != 0:
            self.question_id -= 1

        self.update_label()
        self.ask_question()

    def ask_question(self):
        """Starts ask question sequence"""
        self.update_emotion()

        question = "Question " + str(self.question_id + 1) + ":\n" + self.parser.get_question(self.question_id)
        answers = self.parser.get_answers(self.question_id)

        # Read question
        if SHOW_QUESTION:
            threading.Thread(target=self.speak, args=[question, self.thread_count]).start()
            self.thread_count += 1
        else:
            threading.Thread(target=self.speak_without_bubble, args=[question, self.thread_count]).start()
            self.thread_count += 1
            
        # Show the answers
        threading.Thread(target=self.show_answers, args=[answers, self.thread_count]).start()
        self.thread_count += 1


    def on_correct_response(self, user_answer_id):
        correct_response = self.speech_parser.data['correct_response'][user_answer_id]
        threading.Thread(target=self.speak, args=[correct_response, self.thread_count]).start()
        self.thread_count += 1

    def on_incorrect_response(self, user_answer_id):
        wrong_response = self.speech_parser.data['wrong_response'][user_answer_id]
        correct_response = self.user_evaluator.parser.get_correct_answer(self.question_id)
        fulltext = wrong_response + "\n\"" + correct_response + "\""
        threading.Thread(target=self.speak, args=[fulltext, self.thread_count, False]).start()
        self.thread_count += 1

    def prompt_voice_input(self, louder=False):
        # TODO: add some signal that UI is waiting for speech - probably another window for this
        if louder:
            text = 'Could you speak louder, please?'
        else:
            text = "I'm listening."
            
        threading.Thread(target=self.speak_without_bubble, args=[text, self.thread_count]).start()    
        self.thread_count += 1

    def on_input_text(self, instance, value):
        """Calculates the most similar answer and updates user evaluator"""
        answers = self.parser.get_answers(self.question_id)

        most_matching = self.string_matcher.find_most_similar_answer(value, answers)
        user_answer = most_matching[0]
        user_answer_id = answers.index(user_answer)

        self.user_answer_id = user_answer_id
        self.schedule_evaluation()

    def evaluate(self, dt):
        if self.user_evaluator.check_user_answer(self.question_id, self.user_answer_id):
            self.on_correct_response(self.user_answer_id)
        else:
            self.on_incorrect_response(self.user_answer_id)

        if self.number_of_questions - 1 == self.question_id:
            self.score_button.disabled = False
            self.canvas.ask_update()
        else:
            self.ask_next_question = True
            self.schedule_next_question()

    def schedule_evaluation(self):
        Clock.schedule_once(self.evaluate, 1)

    def schedule_next_question(self):
        Clock.schedule_once(self.go_to_next_question, 2)

    def go_to_next_question(self, dt):
        if self.ask_next_question:
            self.ask_next_question = False
            self.next_question()

    def update_label(self):
        self.label.text = f"Question {self.question_id + 1}/{self.user_evaluator.parser.get_number_of_questions()}"

    def show_score(self):
        score = self.user_evaluator.calculate_score()
        number_of_questions = self.user_evaluator.parser.get_number_of_questions()
        result = f"Your score is {score} out of {number_of_questions}"

        if score > number_of_questions / 2:
            result = "Congrats!\n" + result
            threading.Thread(target=self.speak, args=[result, self.thread_count]).start()
        else:
            result = "It could be better!\n" + result
            threading.Thread(target=self.speak, args=[result, self.thread_count, False]).start()
            
        self.thread_count += 1

        speech, self.text_field.text = self.speech_parser.data["questionnaire"]

        if self.type_of_app == 1:
            self.text_field.height, self.text_field.size_hint_y, self.text_field.opacity, self.text_field.disabled = 0.1, 0.1, 1, False       
            speech += "\n\nYou are in Group 1."
        elif self.type_of_app == 2:
            speech += "\n\nYou are in Group 2."
        elif self.type_of_app == 3:
            speech += "\n\nYou are in Group 3."

        time.sleep(0.5)
        threading.Thread(target=self.speak, args=[speech, self.thread_count, False]).start()
        self.thread_count += 1

        self.update_emotion()

    def update_emotion(self):
        # TODO: needs to update iteratively
        if self.robot_is_sad:
            self.change_to_sad()
        else:
            self.change_to_happy()


class UserInterface(App):
    """ App Class """

    def __init__(self, type_of_app=1, **kwargs):
        super(UserInterface, self).__init__(**kwargs)
        self.type_of_app = type_of_app

    def build(self):
        self.logic_class = LogicClass(self.type_of_app)
        return self.logic_class

    def on_start(self, **kwargs):
        threading.Thread(target=self.logic_class.on_start).start()
