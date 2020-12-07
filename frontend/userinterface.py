# class that creates a simple display to show the "emotion" of the robot
from kivy.app import App
from kivy.config import Config
from kivy.uix.floatlayout import FloatLayout

from frontend.voice_synthesis import say

Config.set('graphics', 'resizable', True) 


class ContainerBox(FloatLayout):
    def speech_synthesis(self, *args):
        text = self.text_field.text
        if text:
            say(text)

    def speech_recognition(self, *args):
        # TODO
        return True


class UserInterface(App):
    def build(self):
        return ContainerBox()