from openai import OpenAI
from config.personality import get_personality_prompt
import os
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def ask_openai(
    history,
    user_input,
    lang="es",
    model="gpt-4o",
    mode="default",
    max_tokens=100,
    extra_context=None,
    extra_interests=None
):
    try:
        system_prompt = get_personality_prompt(mode, lang)

        if extra_context:
            system_prompt += f"\nNota adicional sobre el usuario: {extra_context}"
        if extra_interests:
            system_prompt += f"\nIntereses conocidos: {extra_interests}"

        print(f"[USER] {user_input}")
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "system", "content": system_prompt}] + history + [{"role": "user", "content": user_input}],
            max_tokens=max_tokens
        )
        return response.choices[0].message.content.strip()

    except Exception as e:
        return f"[ERROR] {str(e)}"
