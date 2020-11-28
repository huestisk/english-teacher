# class that creates a simple display to show the "emotion" of the robot
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout

from voice_synthesis import say


class SpeechSynthesisApp(App):
    def build(self):
        layout = BoxLayout()
        self.text_field = TextInput(hint_text='Enter Text Here')
        button = Button(text="Perform Speech Synthesis", on_press=self.perform)
        layout.add_widget(self.text_field)
        layout.add_widget(button)
        return layout

    def perform(self, action):
        text = self.text_field.text
        say(text)


SpeechSynthesisApp().run()