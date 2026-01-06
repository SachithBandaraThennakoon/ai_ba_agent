from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI()

def final_proposal_agent(ba_output: str, architect_output: str) -> str:
    with open("prompts/final_proposal.txt", "r") as f:
        system_prompt = f.read()

    combined_input = f"""
BUSINESS ANALYST OUTPUT:
{ba_output}

SOLUTION ARCHITECT OUTPUT:
{architect_output}
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": combined_input}
        ],
        temperature=0.2
    )

    return response.choices[0].message.content
