from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI()

def client_agent(user_message: str) -> str:
    with open("prompts/client_agent.txt", "r") as f:
        system_prompt = f.read()

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message}
        ],
        temperature=0.3
    )

    return response.choices[0].message.content
