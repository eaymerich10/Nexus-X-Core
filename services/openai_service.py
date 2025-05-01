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
    model="gpt-4o-mini",
    mode="default",
    max_tokens=100,
    extra_context=None,
    extra_interests=None
):
    try:
        system_prompt = get_personality_prompt(mode, lang)

        # Añadir detalles extra si existen
        if extra_context:
            system_prompt += f"\nNota adicional sobre el usuario: {extra_context}"
        if extra_interests:
            system_prompt += f"\nIntereses conocidos: {extra_interests}"

        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "system", "content": system_prompt}] + history + [{"role": "user", "content": user_input}],
            max_tokens=max_tokens
        )
        content = response.choices[0].message.content.strip()

        # Mostrar tokens usados
        usage = getattr(response, "usage", None)
        if usage:
            prompt_tokens = usage.prompt_tokens
            completion_tokens = usage.completion_tokens
            total_tokens = usage.total_tokens
            print(f"🧠 Tokens usados → Prompt: {prompt_tokens}, Respuesta: {completion_tokens}, Total: {total_tokens}")

        return content

    except Exception as e:
        return f"[ERROR] {str(e)}"
