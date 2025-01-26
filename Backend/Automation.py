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

classes = ["zCubwf","hgKElc","LTKOO sY7ric","Z0lcW","gsrt vk_bk FzvWSb YwPhnf", "pclqee", "tw-Data-text tw-text-small tw-ta",
           "IZ6rdc","O5uR6d LTKOO","vlzY6d","webanswers-webanswers_table__webanswers-table","dDono ikb4Bb gsrt", "sXLaOe",
           "LWkfKe","VQF4g","qv3Wpe","kno-rdesc","SPZz6b"]

useragent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36'

client = Groq(api_key=GroqAPIKey)

professional_responses = [
    "Your satisfaction is my top priority: feel free to reach out if there's anything else I can help you with.",
    "I'm at your service for any additional questions or support or support you may need-don't hesitate to ask.",
]

messages = []

SystemChatBot = [{"role":"system","content":f"Hello, I am {os.environ['Username']}, You're a content writer. You have to write content like letter"}]

def GoogleSearch(Topic):
    search(Topic)
    return True

# def Content(Topic):

    def OpenNotepad(File):
        default_text_editor = 'notepad.exe'
        subprocess.Popen([default_text_editor,File])

    def ContentWriterAI(prompt):
        messages.append({"role":"user", "content":f"{prompt}"})

        completion = client.chat.completions.create(
            model="mistral-8x7b-32768",
            messages=SystemChatBot + messages,
            max_tokens=2048,
            temperature=0.7,
            top_p=1,
            stream=True,
            stop=None
        )

        Answer = ""

        for chunk in completion:
            if chunk.choice[0].delta.content:
                Answer += chunk.choice[0].delta.content
        
        Answer = Answer.replace("</s>","")
        messages.append({"role":"assistant","content":Answer})
        return Answer
    
    Topic: str = Topic.replace("Content","")
    ContentByAI = ContentWriterAI(Topic)

    with open(rf"Data\{Topic.lower().replace('','')}.txt","w",encoding="utf-8") as file:
        file.write(ContentByAI)
        file.close()

    OpenNotepad(rf"Data\{Topic.lower().replace('','')}.txt")
    return True

# def Content(Topic):
    def OpenNotepad(File):
        """Open the file in Notepad."""
        try:
            subprocess.Popen(["notepad.exe", File])
        except Exception as e:
            print(f"Error opening Notepad: {e}")

    def ContentWriterAI(prompt):
        """Generate content using Groq API."""
        try:
            messages.append({"role": "user", "content": prompt})

            completion = client.chat.completions.create(
                model="llama3-70b-8192",
                messages=SystemChatBot + messages,
                max_tokens=2048,
                temperature=0.7,
                top_p=1,
                stream=False
            )

            # Extract response content
            Answer = completion["choices"][0]["message"]["content"]
            messages.append({"role": "assistant", "content": Answer})
            return Answer
        except Exception as e:
            print(f"Error generating content: {e}")
            return None

    # Clean topic and set file path
    sanitized_topic = Topic.strip().replace(" ", "_").lower()
    file_path = f"Data/{sanitized_topic}.txt"

    # Ensure Data directory exists
    if not os.path.exists("Data"):
        os.makedirs("Data")

    # Generate content
    ContentByAI = ContentWriterAI(Topic)
    if not ContentByAI:
        print("Failed to generate content.")
        return False

    # Write content to file
    try:
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(ContentByAI)
        print(f"Content written to {file_path}.")
    except Exception as e:
        print(f"Error writing to file: {e}")
        return False

    # Open file in Notepad
    OpenNotepad(file_path)
    return True

def Content(Topic):
    try:
        # Append the user's message to the conversation history
        messages = [{"role": "system", "content": f"Hello, I am {os.environ['Username']}, You're a content writer. You have to write content like letter"}]
        messages.append({"role": "user", "content": Topic})

        # Make the API request to generate content using the Ollama3 model
        completion = client.chat.completions.create(
            model="mistral-8x7b-32768",  # Ensure this is the correct model identifier
            messages=messages,
            max_tokens=2048,
            temperature=0.7,
            top_p=1,
            stream=False  # Non-streaming response
        )

        # Extract the content from the response
        Answer = completion['choices'][0]['message']['content']

        # Clean up the topic name to use as a file name
        file_name = Topic.lower().replace(' ', '_') + ".txt"

        # Define the file path where the content will be saved
        file_path = os.path.join(os.getcwd(), "Data", file_name)

        # Create the 'Data' folder if it doesn't exist
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        # Write the generated content to the file
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(Answer)

        # Open the file in Notepad
        subprocess.Popen(['notepad.exe', file_path])

        return True

    except Exception as e:
        print(f"Error generating content: {e}")
        return False


def YoutubeSearch(Topic):
    Url4Search = f"https://www.youtube.com/results?search_query={Topic}"
    webbrowser.open(Url4Search)
    return True

def PlayYoutube(query):
    playonyt(query)
    return True

# def OpenApp(app, sess=requests.session()):

    try:
        appopen(app, match_closest=True, output=True, throw_error=True)
        return True
    except:
        def extract_links(html):
            if html is None:
                return []
            soup = BeautifulSoup(html, 'html.parser')
            links = soup.find_all('a',{'jsname':'UWckNb'})
            return [link.get('href') for link in links]
        
        def search_google(query):
            url = f"https://www.google.com/search?q={query}"
            headers={"User_Agents": useragent}
            response = sess.get(url, headers=headers)

            if response.status_code== 200:
                return response.text
            else:
                print("Failed to retrieve search results.")
            return None
        html = search_google(app)
        if html:
            link = extract_links(html)[0]
            webopen(link)

        return True

def OpenApp(app, sess=requests.session()):
    try:
        # Attempt to open the app using AppOpener
        appopen(app, match_closest=True, output=True, throw_error=True)
        return True
    except Exception as e:
        # Handle errors if AppOpener fails
        print(f"AppOpener failed: {e}. Attempting web search...")

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
            links = extract_links(html)
            if links:
                webopen(links[0])
                return True
            else:
                print("No links found in Google search results.")
        return False

def CloseApp(app):

    if "chrome" in app:
        pass
    else:
        try:
            close(app,match_closest=True, output=True, throw_error=True)
            return True
        except:
            return False
def System(command):
    def mute():
        keyboard.press_and_release("volume mute")
    def unmute():
        keyboard.press_and_release("volume mute")
    def volume_up():
        keyboard.press_and_release("volume up")
    def volume_down():
        keyboard.press_and_release("volume down")

    if command == "mute":
        mute()
    elif command == "unmute":
        unmute()
    elif command == "volume up":
        volume_up()
    elif command == "mute":
        volume_down()
    return True

async def TranslateAndExecute(commands: list[str]):
    funcs =[]
    for command in commands:
        if command.startswith("open "):
            if "open it" in command:
                pass
            if "open file" in command:
                pass
            else:
                fun = asyncio.to_thread(OpenApp, command.removeprefix("open"))
                funcs.append(fun)
        elif command.startswith("general"):
            pass
        elif command.startswith("realtime"):
            pass
        elif command.startswith("close"):
            fun = asyncio.to_thread(CloseApp, command.removeprefix("close"))
            funcs.append(fun)
        elif command.startswith("play"):
            fun = asyncio.to_thread(PlayYoutube, command.removeprefix("play"))
            funcs.append(fun)
        elif command.startswith("content"):
            fun = asyncio.to_thread(Content, command.removeprefix("content"))
            funcs.append(fun)
        elif command.startswith("google search"):
            fun = asyncio.to_thread(GoogleSearch, command.removeprefix("google search"))
            funcs.append(fun)
        elif command.startswith("youtube search"):
            fun = asyncio.to_thread(YoutubeSearch, command.removeprefix("youtube search"))
            funcs.append(fun)
        elif command.startswith("system"):
            fun = asyncio.to_thread(System,command.removeprefix("system"))
            funcs.append(fun)
        else:
            print(f"No function Found. for{command}")
    results = await asyncio.gather(*funcs)

    for result in results:
        if isinstance(result, str):
            yield result
        else:
            yield result

async def Automation(commands: list[str]):

    async for result in TranslateAndExecute(commands):
        pass
    return True

if __name__ == "__main__":
    asyncio.run(Automation(["open Whatsapp","content song for me"]))