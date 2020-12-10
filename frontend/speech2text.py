# class that captures the voice input of a user

import os
from pathlib import Path
import speech_recognition as sr
import yaml

BASE_DIR = Path(__file__).resolve().parent.parent.parent


class SpeechRecognizer:

    def __init__(self, recognizer, microphone):
        """Class for handling Speech2Text tasks"""

        # check that recognizer and microphone arguments are appropriate type
        if not isinstance(recognizer, sr.Recognizer):
            raise TypeError("`recognizer` must be `Recognizer` instance")

        if not isinstance(microphone, sr.Microphone):
            raise TypeError("`microphone` must be `Microphone` instance")

        self.recognizer = recognizer
        self.microphone = microphone

    def recognize_speech_from_mic(self):
        """Transcribe speech from recorded from `microphone`.

        Returns a dictionary with three keys:
        "success": a boolean indicating whether or not the API request was
                   successful
        "error":   `None` if no error occured, otherwise a string containing
                   an error message if the API could not be reached or
                   speech was unrecognizable
        "transcription": `None` if speech could not be transcribed,
                   otherwise a string containing the transcribed text
        """

        # adjust the recognizer sensitivity to ambient noise and record audio
        # from the microphone
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source)
            audio = self.recognizer.listen(source)

        # set up the response object
        response = {
            "success": True,
            "error": None,
            "transcription": None
        }

        # try recognizing the speech in the recording
        # if a RequestError or UnknownValueError exception is caught,
        #     update the response object accordingly
        try:
            response["transcription"] = self.recognizer.recognize_google(audio)
        except sr.RequestError:
            # API was unreachable or unresponsive
            response["success"] = False
            response["error"] = "API unavailable"
        except sr.UnknownValueError:
            # speech was unintelligible
            response["error"] = "Unable to recognize speech"

        return response

    @classmethod
    def from_config(cls):
        r = sr.Recognizer()
        mic = sr.Microphone()

        with open(os.path.join(BASE_DIR, 'config.yaml')) as f:
            data = yaml.load(f, Loader=yaml.FullLoader)

        mic = sr.Microphone(device_index=data['Speech2Text']['default_mic_number'])
        return cls(recognizer=r, microphone=mic)


# USAGE
if __name__ == "__main__":
    speech_recognizer = SpeechRecognizer.from_config()
    print(speech_recognizer.recognize_speech_from_mic())