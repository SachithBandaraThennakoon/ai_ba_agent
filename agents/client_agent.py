from openai import OpenAI
from dotenv import load_dotenv
from vector_db.company_knowledge import query_company_knowledge


load_dotenv()
client = OpenAI()

def client_agent(session_memory, user_input: str):
    # Detect confirmation
    if user_input.strip().upper() == "CONFIRM":
        session_memory.confirm()

        system_prompt = """
You are a Client Engagement Agent.

The client has CONFIRMED understanding.
Generate a FINAL structured business summary.

Output format (MANDATORY):
1. Business Problem Statement
2. Business Goals
3. Clarification Questions
"""
        company_context = ""

    else:
        # 🔍 Detect company-related questions
        company_keywords = [
            "company", "your company", "company name",
            "who are you", "about you", "services", "what do you do"
        ]

        if any(keyword in user_input.lower() for keyword in company_keywords):
            company_context = query_company_knowledge(
                "company name, overview, services"
            )
        else:
            company_context = ""

        system_prompt = f"""
You are a Client Engagement Agent in a Data, AI, and BI company.

Mode: DISCOVERY CHAT

Rules:
- Be friendly and professional
- Answer company-related questions using PROVIDED COMPANY CONTEXT
- Ask business-focused questions
- Avoid technical jargon
- Gradually understand the problem
- When confident, ask the client to type CONFIRM

COMPANY CONTEXT (use ONLY if relevant):
{company_context}
"""

    messages = [
        {"role": "system", "content": system_prompt},
        *session_memory.get(),
        {"role": "user", "content": user_input}
    ]

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        temperature=0.3
    )

    reply = response.choices[0].message.content

    session_memory.add("user", user_input)
    session_memory.add("assistant", reply)

    return reply, session_memory.is_confirmed()
