from http import server
import subprocess
import wolframalpha
import pyttsx3
import json
import pyaudio
import random
import operator
import speech_recognition as sr
import datetime
import wikipedia
import webbrowser
import os
from dotenv import load_dotenv
import winshell
import pyjokes
import feedparser
import smtplib
import ctypes
import time
import requests
import shutil
from twilio.rest import Client
from clint.textui import progress
from ecapture import ecapture as ec
from bs4 import BeautifulSoup
import win32com.client as wincl
from urllib.request import urlopen

load_dotenv()

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)


# Sub functions

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def wishMe():
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour < 12:
        speak("Good Morning Sir!")

    elif hour >= 12 and hour < 18:
        speak("Good Afternoon Sir!")

    else:
        speak("Good Evening Sir!")

    assname = "Jarvis"
    version = "1 point o"
    speak("I am your Assistant")
    speak(assname)
    speak("Version")
    speak(version)


def takeCommand():
    r = sr.Recognizer()

    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language = 'en-us')
        print(f"User said: {query}\n")

    except Exception as e:
        print(e)
        print("Unable to recognize your voice")
        return "None"

    return query

def username():
    speak("What should i call you sir?")
    uname = takeCommand()
    speak("Welcome ")
    speak(uname)
    columns = shutil.get_terminal_size(fallback=(80, 20)).columns

    print("####################".center(columns))
    print("Welcome Mr.", uname.center(columns))
    print("####################".center(columns))

    speak("How can i help you, Sir")

def sendEmail(to, content):
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()

        email = os.getenv('EMAIL')
        password = os.getenv('EMAIL_PASSWORD')
        
        if not email or not password:
             print("Email or password is missing.")
             return

        server.login(email, password)
        server.sendmail(email, to, content)
        server.close()

    except Exception as e:
        print(e)
        speak("I am not able to send this email")

# Main function
if __name__ == '__main__':
    clear = lambda: os.system('cls' if os.name == 'nt' else 'clear')

    # This function will clean any command before execution of the file
    clear()
    wishMe()
    username()

    assname = "Jarvis"
    version = "1 point o"

    while True:
        query = takeCommand().lower()

        # all the commands said by the user will be stored here in 'query' and will be converted to lower case for easily recognition of the command given
        if 'wikipedia' in query:
            speak('Searching Wikipedia...')
            query = query.replace("wikipedia", "")
            results = wikipedia.summary(query, sentences = 3)
            speak("According to Wikipedia")
            print(results)
            speak(results)

        elif 'open youtube' in query:
            speak("Opening Youtube...\n")
            webbrowser.open("youtube.com")

        elif 'open google' in query:
            speak("Opening Google...\n")
            webbrowser.open("google.com")

        elif 'open stackoverflow' in query:
            speak("Opening Stackoverflow, Happy coding!")
            webbrowser.open("stackoverflow.com")

        elif 'time' in query:
            strTime = datetime.datetime.now().strftime("% H:% M:% S")
            speak(f"Sir, the time is {strTime}")


        elif 'send email' in query:
            try:
                speak("What should i say?")
                content = takeCommand()
                speak("To whom should i send it to?")
                to = input()
                sendEmail(to, content)
                speak("Email has been sent!")

            except Exception as e:
                print(e)
                speak("I am not able to send this email")

        elif 'how are you' in query:
            speak("I am fine, Thank you")
            speak("How are you, Sir")

        elif 'fine' in query or 'good' in query:
            speak("It's good to know that")

        elif "what's your name?" in query or "What is your name" in query:
            speak("My creator named me")
            speak(assname)
            print("My creator named me", assname)

        elif 'exit' in query:
            speak("Thanks for giving me your time")
            exit()

        elif "who made you" in query or "who created you" in query:
            speak("I was made by Lukhanyo Radebe")

        elif 'joke' in query:
             speak(pyjokes.get_joke())


        elif "calculate" in query:

            app_id = os.getenv("WOLFRAMALPHA_API_KEY")
            client = wolframalpha.Client(app_id)
            indx = query.lower().split().index('calculate')
            query = query.split()[indx + 1:]
            res = client.query(' '.join(query))
            answer = next(res.results).text
            print("The answer is " + answer)
            speak("The answer is" + answer)

        elif 'search' in query:
            query = query.replace("search", "")
            webbrowser.open(query)

        elif "what is the purpose of your existence" in query:
            speak("My purpose is to help individuals with mobility or vision impairments may find it challenging to use traditional interfaces and hopefully khanyo adds more functionality to my core so i can be more helpfull")

        elif 'news' in query:
            try: 
                news_api = os.getenv("NEWS_API_KEY")
                jsonObj = urlopen(news_api)
                data = json.load(jsonObj)
                i = 1

                speak('here are some top news from the times of south africa')
                print('''================= TIMES OF SOUTH AFRICA =================''' + '\n')

                for item in data['articles']:

                    print(str(i) + '. ' + item['title'] + '\n')
                    print(item['description'] + '\n')
                    speak(str(i) + '. ' + item['title'] + '\n')
                    i += 1

            except Exception as e:
                 print(str(e))

        elif 'lock window' in query:
            speak("locking the device")
            ctypes.windll.user32.LockWorkStation()

        elif 'shutdown system' in query:
            speak("Hold on a sec, your system is on its way to shut down")
            subprocess.call('shutdown /p /f')

        elif 'empty recycle bin' in query:
            winshell.recycle_bin().empty(confirm = False, show_progress = True, sound = True)
            speak("Recycle bin has been recycled")

        elif "don't listen" in query or "stop listening" in query:
            while True:
                try:
                    speak("How long should I stop listening, Please provide an integer value.")
                    a = int(takeCommand())  
                    time.sleep(a)  
                    print(a)
                    break  

                except ValueError:
                    speak("That was not a valid integer. Please try again.")


        elif "where is" in query:
            query = query.replace("where is", "")
            location = query
            speak("locating...")
            speak(location)
            webbrowser.open("https://www.google.nl/maps/place/" + location)

        elif "camera" in query or "take a photo" in query:
            try:
                ec.capture(0, "Jarvis Camera", "img.jpg")
            except Exception as e:
                print("Camera error:", e)
                speak("Unable to access the camera.")

        elif "restart" in query:
            subprocess.call(["shutdown", "/r"])

        elif "hibernate" in query or "sleep" in query:
            speak("Hibernating")
            subprocess.call("Shutdown /h")
