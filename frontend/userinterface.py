# class that creates a simple display to show the "emotion" of the robot
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout

from frontend.voice_synthesis import say

class ContainerBox(BoxLayout):
    def speech_synthesis(self, *args):
        text = self.text_field.text
        say(text)

    def speech_recognition(self, *args):
        # TODO
        return True


class UserInterface(App):
    def build(self):
        return ContainerBox()