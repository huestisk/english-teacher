# class that creates a voice output from a written message
import pyttsx3

class Text2Speech:

    def __init__(self, **kwargs):
        self.engine = pyttsx3.init()
        self.voices = self.engine.getProperty('voices')
        try:
            self.engine.setProperty('voice', 'english')
        except KeyError:
            self.engine.setProperty('voice', self.voices[0].id) # mac
            
    def say(self, text):
        self.engine.say(text)
        self.engine.runAndWait()

""" find a good voice """
if __name__ == '__main__':
    speaker = Text2Speech()
    for voice in speaker.voices:
        print(voice, voice.id)
        speaker.engine.setProperty('voice', voice.id)
        speaker.say("Hello World!")
        speaker.engine.stop()