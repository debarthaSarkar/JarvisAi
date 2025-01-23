#Day 2 work
from groq import Groq
from json import load, dump
import datetime
from dotenv import dotenv_values

# Load environment variables
env_vars = dotenv_values(".env")
Username = env_vars.get("Username", "User")
Assistantname = env_vars.get("Assistantname", "Assistant")
GroqAPIKey = env_vars.get("GroqAPIKey")

# Initialize Groq client
client = Groq(api_key=GroqAPIKey)

# Initial system prompt
System = f"""Hello, I am {Username}, You are a very accurate and advanced AI chatbot named {Assistantname} which also has real-time up-to-date information from the internet.
*** Do not tell time until I ask, do not talk too much, just answer the question.***
*** Reply in only English, even if the question is in Hindi, reply in English.***
*** Do not provide notes in the output, just answer the question and never mention your training data. ***
"""

SystemChatBot = [{"role": "system", "content": System}]

# Load chat history and user data
try:
    with open(r"Data\ChatLog.json", "r") as f:
        messages = load(f)
except FileNotFoundError:
    messages = []

try:
    with open(r"Data\UserData.json", "r") as f:
        user_data = load(f)
except FileNotFoundError:
    user_data = {}

# Function to save user data
def save_user_data():
    with open(r"Data\UserData.json", "w") as f:
        dump(user_data, f, indent=4)

# Function to fetch real-time information
def Realtimeformation():
    current_data_time = datetime.datetime.now()
    return current_data_time.strftime("Day: %A, Date: %d %B %Y, Time: %H:%M:%S")

# Function to process user queries
def ChatBot(Query):
    global messages

    # Add user query to the conversation
    messages.append({"role": "user", "content": Query})

    try:
        # Generate response from AI
        completion = client.chat.completions.create(
            model="llama3-70b-8192",
            messages=SystemChatBot + messages,
            max_tokens=1024,
            temperature=0.7,
            top_p=1,
            stream=True,
            stop=None,
        )

        Answer = ""
        for chunk in completion:
            if chunk.choices[0].delta.content:
                Answer += chunk.choices[0].delta.content

        # Add assistant's response to the conversation
        messages.append({"role": "assistant", "content": Answer})

        # Save updated chat log
        with open(r"Data\ChatLog.json", "w") as f:
            dump(messages, f, indent=4)

        return Answer

    except Exception as e:
        return f"Error: {e}"


# Main loop for user interaction
if __name__ == "__main__":
    while True:
        user_input = input("Enter your Question: ")
        print(ChatBot(user_input))
