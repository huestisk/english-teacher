# class that creates a voice output from a written message
import pyttsx3

def say(text):
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[0].id)
    engine.say(text)
    engine.runAndWait()

# while True:
#     text_to_say = input("Enter text to say: ")
#     say(text=text_to_say)