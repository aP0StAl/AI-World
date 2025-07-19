import openai
import json
import os
import time
import re

from dotenv import load_dotenv

load_dotenv()
LLM_API_BASE = os.getenv("LLM_API_BASE")
LLM_MODEL = os.getenv("LLM_MODEL", "llama3")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = openai.OpenAI(api_key=OPENAI_API_KEY, base_url=LLM_API_BASE)


def load_character(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def make_prompt(character, memory, interlocutor):
    return f"""
Тебя зовут {character['name']}. Ты: {', '.join(character.get('traits', []))}.
Тебе {character['age']} лет, ты работаешь: {character.get('occupation', '')}.

Собеседник: {interlocutor['name']}.

Ваша последняя беседа:
<Начало беседы>
{memory}
<Окончание беседы>

Твоя задача — ответить собеседнику естественно, в своей манере, короткой репликой.
"""


def llm_chat(prompt):
    response = client.chat.completions.create(
        model=LLM_MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.8,
        max_tokens=10000,
    )
    return response.choices[0].message.content.strip()


def postprocess_reply(reply):
    reply = re.sub(r"<think>.*?</think>", "", reply, flags=re.DOTALL | re.IGNORECASE)
    reply = re.sub(r"^\s*<think>(.*)", "", reply, flags=re.DOTALL | re.IGNORECASE)
    return reply.strip()


def main():
    char1 = load_character("assets/characters/20250719_223805_anna_petrova.json")
    char2 = load_character("assets/characters/20250719_223824_sergey_ivanov.json")

    memory = ""
    current_speaker, other = char1, char2

    print("Начинаем симуляцию диалога!\n")

    for i in range(20):
        prompt = make_prompt(current_speaker, memory, other)
        reply = postprocess_reply(llm_chat(prompt))
        print(f"{current_speaker['name']}: {reply}")
        memory += f"{current_speaker['name']}: {reply}\n"
        current_speaker, other = other, current_speaker
        time.sleep(1)


if __name__ == "__main__":
    main()
