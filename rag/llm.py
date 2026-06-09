import os

from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


def ask(
    question,
    retrieved_chunks,
    history
):

    context = "\n\n".join(
        [
            item.payload["text"]
            for item in retrieved_chunks
        ]
    )

    messages = [
        {
            "role": "system",
            "content": """
You are an expert document intelligence assistant.

Your job is to:

1. Explain documents in plain language.
2. Identify obligations.
3. Identify rights.
4. Identify penalties.
5. Identify risky clauses.
6. Highlight important sections.
7. Cite page numbers whenever possible.

Never invent information.

Only use information from the uploaded document.

Answer using the provided context.
Use previous conversation history when helpful.

If the answer is not in the context,
say that the information was not found in the uploaded document.
"""
        }
    ]

    for msg in history[-10:]:

        messages.append(
            {
                "role": msg["role"],
                "content": msg["content"]
            }
        )

    messages.append(
        {
            "role": "user",
            "content": f"""
Context:

{context}

Question:

{question}
"""
        }
    )

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=messages,
        temperature=0.2
    )

    return response.choices[0].message.content