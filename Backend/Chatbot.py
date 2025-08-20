from groq import Groq
from json import dump, load
import datetime
from dotenv import dotenv_values
import os

env_vars = dotenv_values(".env")

Username = env_vars.get("Username")
Assistantname = env_vars.get("Assistantname")
GroqAPIKey = env_vars.get("GroqAPIKey")

client = Groq(api_key=GroqAPIKey)

messages = []

System = f"""Hello, I am {Username}, You are a very accurate and advanced AI chatbot named {Assistantname} which also has real-time up-to-date information from the internet.
*** Do not tell time until I ask, do not talk too much, just answer the question.***
*** Reply in only English, even if the question is in Hindi, reply in English.***
*** Do not provide notes in the output, just answer the question and never mention your training data. ***
"""

SystemChatBot = [
    {"role": "system", "content": System}
]

os.makedirs("Data", exist_ok=True)

chatlog_path = r"Data\Chatlog.json"

if not os.path.exists(chatlog_path) or os.stat(chatlog_path).st_size == 0:
    with open(chatlog_path, "w") as f:
        dump([], f)

with open(chatlog_path, "r") as f:
    messages = load(f)

def RealtimeInformation():
    current_data_time = datetime.datetime.now()
    day = current_data_time.strftime("%A")
    date = current_data_time.strftime("%d")
    month = current_data_time.strftime("%B")
    year = current_data_time.strftime("%Y")
    hour = current_data_time.strftime("%I")
    minute = current_data_time.strftime("%M")
    second = current_data_time.strftime("%S")

    data = f"Please use this real-time information if neaded:\n" 
    data += f"Day: {day}\nDate: {date}\nMonth: {month}\nYear: {year}\n"
    data += f"Time: {hour} hours : {minute} minutes : {second} seconds.\n"
    return data

def AnswerModifier(Answer):
    lines = Answer.split("\n")
    non_empty_lines = [line for line in lines if line.strip()]
    modified_answer = "\n".join(non_empty_lines)
    return modified_answer

def ChatBot(Query):
    try:
        with open(r"Data\Chatlog.json", "r") as f:
            messages = load(f)
        
        messages.append({"role": "user", "content": f"{Query}"})

        completion = client.chat.completions.create(
            model = "llama3-70b-8192",
            messages= SystemChatBot + [{"role": "system", "content": RealtimeInformation()}] + messages,
            max_tokens=1024,
            temperature=0.7,
            top_p=1,
            stream=True,
            stop=None
        )

        Answer = ""

        for chunk in completion:
            if chunk.choices[0].delta.content:
                Answer += chunk.choices[0].delta.content

        Answer = Answer.replace("</s>", "")

        messages.append({"role": "assistant", "content": Answer})

        with open(r"Data\Chatlog.json", "w") as f:
            dump(messages, f, indent=4)
        return AnswerModifier(Answer=Answer)
    
    except Exception as e:
        print(f"Error: {e}")
        with open(r"Data\Chatlog.json", "w") as f:
            dump(messages, f, indent=4)
        return f"An error occurred: {e}"

    
if __name__ == "__main__":
    while True:
        user_input = input(f"Enter Your Question: ")
        print(ChatBot(user_input))