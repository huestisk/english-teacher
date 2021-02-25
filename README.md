# CIR Project : An English Teaching Robot

## Evaluation instructions
@professors: This is a copy of our Github repository with additional files. In the folder called deliverables, you will find our report and presentation as pdfs. 
In case you would like to test the system without installing the requirements, we have included an executable file for windows. All of the code for the system and the statistical evaluation of the experiment can be found here. The main file for the code is called english_teacher.py, although most of the logic is in the file frontend/userinterface.py
The questionnaire is appended to the report and the participants answers (as well as the questions) can be found in the csv file in the folder experiment. 

Please feel free to contact us with any questions.

## Setting up  
Installing PyAudio for Debian Linux - necessary for microphone input
```shell
$ sudo apt-get install python-pyaudio python3-pyaudio
```

Creating exe file from project
```shell
pyinstaller --onefile --hidden-import=pyttsx3.drivers  --hidden-import=pyttsx3.drivers.espeak --add-data 'config.yaml:.' --add-data 'quizzes:quizzes' --add-data 'frontend/userinterface.kv:frontend' --add-data 'frontend/images/*:frontend/images'  english_teacher.py
```

with additional hook (pyttsx3):
```shell
pyinstaller --onefile --add-data 'config.yaml:.' --add-data 'quizzes:quizzes' --add-data 'frontend/userinterface.kv:frontend' --add-data 'frontend/images/*:frontend/images' --add-data 'frontend/speech.json:frontend' --additional-hooks-dir=.  english_teacher.py 
```

Windows:
```shell
pyinstaller --onefile --hidden-import _rapidfuzz_cpp --add-data "config.yaml;." --add-data "quizzes;quizzes" --add-data "frontend/userinterface.kv;frontend" --add-data "frontend/images/*;frontend/images" --add-data "frontend/speech.json;frontend" --additional-hooks-dir=.  english_teacher.py 
```
The easier way is to use:
```shell
pyinstaller english_teacher.spec
```
All the pyinstaller parameters are included in the spec file, and it should be portable.

### URL of the exes :  
Group 1 (voice only) : <https://we.tl/t-IEFS8ozMhV>  
Group 2 (control group) : <https://we.tl/t-8lodJB2roX>  
Group 3 (mixed group) : <https://we.tl/t-zTYJm0PCpx>
