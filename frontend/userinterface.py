# class that creates a simple display to show the "emotion" of the robot
from kivy.app import App
from kivy.config import Config
from kivy.core.window import Window
from kivy.uix.floatlayout import FloatLayout

from frontend.voice_synthesis import speechGen

Config.set('graphics', 'resizable', True) 

class ContainerBox(FloatLayout):

    def __init__(self, **kwargs):
        super(ContainerBox, self).__init__(**kwargs)
        Window.bind(on_key_down=self._on_keyboard_down)
        self.speaker = speechGen()

    def _on_keyboard_down(self, instance, keyboard, keycode, text, modifiers):
        if self.text_field.focus and keycode == 40:  # 40 - Enter key pressed
            self.keyboard_input()

    def keyboard_input(self):
        # TODO: 
        #   pass text to backend
        #   remove speech generation
        #   improve speech bubble
        text = self.text_field.text
        if text:
            self.speaker.say(text)
            self.text_field.text = ""
            self.speech_bubble.text = text
            self.change_to_sad()

    def listen(self, *args):
        # TODO: add speech recognition
        pass

    def change_to_sad(self):
        self.robot.source = 'frontend/images/sad_robot.jpg'

    def change_to_happy(self):
        self.robot.source = 'frontend/images/robot_png.jpg'


class UserInterface(App):
    def build(self):
        return ContainerBox()