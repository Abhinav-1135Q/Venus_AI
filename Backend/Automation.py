from AppOpener import close, open as appopen
from webbrowser import open as webopen
from pywhatkit import search, playonyt
from dotenv import dotenv_values
from bs4 import BeautifulSoup
from rich import print 
from groq import Groq
import webbrowser
import subprocess
import requests
import keyboard
import asyncio
import os

env_vars = dotenv_values(".env")
GroqAPIKey = env_vars.get("GroqAPIKey")

classes = ["zCubwf", "hgKElc", "LTKOO SY7ric", "ZOLcW", "gsrt vk_bk FzvWSb YwPhnf", "pclqee", "tw-Data-text tw-text-small tw-ta", "IZ6rdc", "05uR6d LTKOO", "vlzY6d", "webanswers-webanswers_table_webanswers-table", "dDoNo ikb4Bb gsrt", "sXLa0e","LWkfKe", "VQF4g", "qv3Wpe", "kno-rdesc", "SPZz6b"]
useragent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896/75 Safari/537.36"

client = Groq(api_key=GroqAPIKey)

porfessional_response = [
    "Your satisfaction is my top priority; feel free to reach out if there's anything else I can help you with.",
    " I'm at your service for any additional questions or support you may need-don't hesitate to ask."
]

message = []

SystemChatBot = [{"role": "system", "content": f"Hello, I am {os.environ['Username']}, your personal assistant. I am here to assist you with any task you need help with. I can search the web, open applications, and perform various tasks to make your life easier. If you have any questions or need assistance, just let me know!"}]

def GoogleSearch(Topic):
    search(Topic)
    return True

def Content(Topic):
    def OpenNotepad(File):
        default_tex_editor = 'notepad.exe'
        subprocess.Popen([default_tex_editor, File])
    def ContentWriterAI(prompt):
        message.append({"role": "user", "content": f"{prompt}"})
        completion = client.chat.completions.create(
            model = "mixtral-8x7b-32768",
            messages = SystemChatBot + message,
            max_tokens = 2048,
            temperature=0.7,
            top_p = 1,
            stream = True,
            stop = None
        )
        Answer = ""

        for chunk in completion:
            if chunk.choices[0].delta.content:
                Answer += chunk.choices[0].delta.content
        Answer = Answer.replace("</s>","")
        message.append({"role": "assistant", "content": Answer})
        return Answer
    Topic: str = Topic.replace("Content: ", "")
    ContentByAI = ContentWriterAI(Topic)

    with open(rf"Data\{Topic.lower().replace(' ', '')}.txt","w", encoding = "utf-8") as file:
        file.write(ContentByAI)
        file.close()

    OpenNotepad(rf"Data\{Topic.lower().replace(' ', '')}.txt")
    return True

def YouTubeSearch(Topic):
    Url4Search = f"http://www.youtube.com/results?search_query={Topic}"
    webbrowser.open(Url4Search)
    return True

def PlayYoutube(query):
    playonyt(query)
    return True

def OpenApp(app, sess=requests.session()):
    try:
        appopen(app, match_closest = True, output=True, throw_error=True)
        return True
    except:
        def extract_links(html):
            if html is None:
                return []
            soup = BeautifulSoup(html, 'html.parser')
            links = soup.find_all('a', {'jsname': 'UWckNb'})
            return [link.get('href') for link in links]
        def search_google(query):
            url = f"https://www.google.com/search?q={query}"
            headers = {"User-Agent": useragent}
            response = sess.get(url, headers=headers)
            if response.status_code == 200:
                return response.text
            else:
                print("Failed to retrieve search results.")
            return None
        html = search_google(app)

        if html:
            link = extract_links(html)[0]
            webopen(link)
        return True

def CloseApp(app):
    if "Chrome" in app:
        pass
    else:
        try:
            close(app, match_closest=True, output=True, throw_error=True)
            return True
        except:
            return False
        
def System(command):
    def mute():
        keyboard.pass_and_release("volume mute")
    def unmute():
        keyboard.pass_and_release("volume unmute")
    def volume_up():
        keyboard.pass_and_release("volume up")
    def volume_down():
        keyboard.pass_and_release("volume down")

    if command == "mute":
        mute()
    elif command == "unmute":
        unmute()
    elif command == "volume up":
        volume_up()
    elif command == "volume down":
        volume_down()
    return True

async def TranslateAndExecute(commands: list[str]):
    funcs = []
    for command in commands:
        if command.startswith("open "):
            if "open it" in command:
                pass
            elif "open file" == command:
                pass
            else:
                fun = asyncio.to_thread(OpenApp, command.removeprefix("open "))
                funcs.append(fun)
        elif command.startswith("general "):
            pass
        elif command.startswith("realtime "):
            pass
        elif command.startswith("close "):
            fun = asyncio