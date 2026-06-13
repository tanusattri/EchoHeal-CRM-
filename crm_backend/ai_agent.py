import os
import httpx

from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

print("GROQ_API_KEY =", GROQ_API_KEY)


async def ask_groq(system_prompt: str, user_prompt: str):

    async with httpx.AsyncClient() as client:

        response = await client.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {GROQ_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "llama-3.1-8b-instant",
                "messages": [
                    {
                        "role": "system",
                        "content": system_prompt
                    },
                    {
                        "role": "user",
                        "content": user_prompt
                    }
                ],
                "temperature": 0.3
            },
            timeout=30
        )

        if response.status_code != 200:
            raise Exception(
                f"Groq Error: {response.text}"
            )

        data = response.json()

        return data["choices"][0]["message"]["content"]