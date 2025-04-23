import os
import openai
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def ask_openai(history, message):
    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=history + [{"role": "user", "content": message}],
    )
    return response.choices[0].message.content.strip()
