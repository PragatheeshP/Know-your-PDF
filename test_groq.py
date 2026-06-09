from groq import Groq

client = Groq(api_key="GROQ_API_KEY")

response = client.chat.completions.create(
    model="deepseek-r1-distill-llama-70b",
    messages=[
        {
            "role": "user",
            "content": "Say Hello"
        }
    ]
)

print(response.choices[0].message.content)