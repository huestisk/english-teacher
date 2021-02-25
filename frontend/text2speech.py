# class that creates a voice output from a written message
import pyttsx3
import time
import sys
class Text2Speech:

    def __init__(self, **kwargs):
        self.engine = pyttsx3.init()
        self.voices = self.engine.getProperty('voices')
        try:
            if sys.platform == 'win32':
                en_us_id = "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_ZIRA_11.0"
                self.engine.setProperty('voice', en_us_id)
            elif sys.platform == 'linux':
                self.engine.setProperty('voice', 'english-us')
        except KeyError:
            self.engine.setProperty('voice', self.voices[0].id)  

    def say(self, text):
        if text:
            self.engine.say(text)
        try:
            self.engine.runAndWait()
        except RuntimeError:
            print("RuntimeError")
            time.sleep(0.5)
            self.say(text)


""" find a good voice """
if __name__ == '__main__':
    speaker = Text2Speech()
    for voice in speaker.voices:
        print(voice, voice.id)
        speaker.engine.setProperty('voice', voice.id)
        speaker.say("Hello World!")
        speaker.engine.stop()
