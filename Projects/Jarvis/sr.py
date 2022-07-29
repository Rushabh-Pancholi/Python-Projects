import pyttsx3
import os
import speech_recognition as sr
import wikipedia
import random
import time
import pyaudio

# pyttsx3
e = pyttsx3.init()
e.setProperty('rate',160)
e.setProperty('volume',1)
voices=e.getProperty('voices')
e.setProperty('voice',voices[1].id)


def say(word):
    e.say(word)
    e.runAndWait()

# speech recognition
r=sr.Recognizer()
mic=sr.Microphone.list_microphone_names()
def mic():
    with sr.Microphone(device_index=1, sample_rate=20000, chunk_size=2048) as Mic:
        r.adjust_for_ambient_noise(Mic)

        audio = r.listen(Mic)

        try:
            text = r.recognize_bing(audio)
            return text
        except sr.UnknownValueError:

            say("Sorry i didn't get it")
        except sr.RequestError as e:
            say('device is not connected to internet')



a=1
Quit=False
while not Quit:
    say('what can i do for you?')
    a=mic()
    g = ["i'm fine,what's about you","Great,aren't you?"]
    try:
        if ('nothing' in a):
                Quit=True


        elif('how are you' in a):
            say(random.choice(g))
        elif ('hello' in a):
            os.startfile(r"C:\Users\HP PC\AppData\Local\Google\Chrome\Application\chrome.exe")
        elif ('find' in a):
            say("what do you want to know?")
            a=mic()
            text = wikipedia.summary(a)
            print(text)
        #else:
    except TypeError:
        print('try again')




