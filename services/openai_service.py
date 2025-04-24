import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def ask_openai(history, user_input, model="gpt-4o-mini"):
    try:
        response = client.chat.completions.create(
            model=model,
            messages=history + [{"role": "user", "content": user_input}],
            max_tokens=300
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"[ERROR] {str(e)}"
