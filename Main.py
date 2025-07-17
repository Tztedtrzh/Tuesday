import speech_recognition as sr
import pyttsx3
import webbrowser
import subprocess
import pyautogui
import os
from openai import OpenAI

client: OpenAI = OpenAI(api_key="") # Placeholder for your actual key

sleeping: bool = False

tts_engine = pyttsx3.init()
tts_engine.setProperty('rate', 170)

def speak(text: str) -> None:
    print("Monday:", text)
    tts_engine.say(text)
    tts_engine.runAndWait()

def listen() -> str:
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
    try:
        command: str = recognizer.recognize_google(audio)
        print("You:", command)
        return command
    except sr.UnknownValueError:
        speak("Sorry, I didn't catch that.")
        return ""
    except sr.RequestError:
        speak("Speech service is unavailable.")
        return ""

def ask_monday(question: str) -> str:
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": question}]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print("!!! OpenAI Error:", e)
        return "Sorry, I couldn't retrieve an answer from GPT."

def handle_command(command: str) -> None:
    global sleeping
    command = command.lower()

    if "wake up" in command:
        if sleeping:
            sleeping = False
            speak("I'm awake and listening again.")
        else:
            speak("I'm already awake.")
        return

    if sleeping:
        return

    if "go to sleep" in command:
        sleeping = True
        speak("Okay, I'm sleeping now.")
        return

    if "open youtube" in command:
        webbrowser.open("https://www.youtube.com")
        speak("Opening YouTube.")

    elif "open chrome" in command:
        chrome_path: str = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"
        if os.path.exists(chrome_path):
            subprocess.Popen([chrome_path]) # More robust than os.startfile for some cases
            speak("Opening Google Chrome.")
        else:
            speak("I couldn't find Chrome on your system.")

    elif "open steam" in command:
        steam_path: str = "C:\\Program Files (x86)\\Steam\\Steam.exe"
        if os.path.exists(steam_path):
            subprocess.Popen([steam_path])
            speak("Opening Steam.")
        else:
            speak("I couldn't find Steam on your system.")

    elif "open xbox" in command or "open xbox app" in command:
        try:
            subprocess.run(["explorer.exe", "shell:AppsFolder\\Microsoft.GamingApp_8wekyb3d8bbwe!App"], check=True)
            speak("Opening the Xbox app.")
        except subprocess.CalledProcessError:
            speak("I couldn't open the Xbox app.")
        except FileNotFoundError:
            speak("The necessary system command to open Xbox app was not found.")

    elif "type" in command:
        to_type: str = command.replace("type", "", 1).strip()
        if to_type:
            speak(f"Typing: {to_type}")
            pyautogui.write(to_type, interval=0.05)
        else:
            speak("What should I type?")

    elif "exit" in command or "quit" in command or "goodbye" in command:
        speak("Goodbye. I'll be here if you need me.")
        exit()

    else:
        reply: str = ask_monday(command)
        speak(reply)

speak("Hello, I'm Monday. How can I help?")
while True:
    user_command: str = listen()
    if user_command:
        handle_command(user_command)
