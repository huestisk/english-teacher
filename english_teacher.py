# main program
from frontend.userinterface import UserInterface
from frontend.text2speech import Text2Speech
from frontend.speech2text import SpeechRecognizer

class FrontendManager:
    
    def __init__(self, **kwargs):
        self.ui = UserInterface()
        self.speaker = Text2Speech()
        # self.listener = SpeechRecognizer.from_config()
        # TODO: fix error "OSError: No Default Input Device Available"
        self.ui.run()

    def speak(self, text):
        self.speaker.say(text)  
        
    def listen(self):
        # TODO
        pass

    def frown(self):
        # TODO
        pass

""" Run Application """
if __name__ == '__main__':
    mgmt = FrontendManager()
    # mgmt.speak("Hi, I'm Robby!")