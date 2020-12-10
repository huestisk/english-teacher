# main program
from frontend.userinterface import UserInterface
from frontend.voice_synthesis import speechGen

class frontendManager:
    def __init__(self, **kwargs):
        self.ui = UserInterface()
        self.speaker = speechGen()

    def speak(self, text):
        self.speaker.say(text)  
        
    def listen(self):
        # TODO
        pass

    def frown(self):
        # TODO
        pass


if __name__ == '__main__':
    mgmt = frontendManager()
    mgmt.speak("Hi, I'm Robby!")
    mgmt.ui.run()