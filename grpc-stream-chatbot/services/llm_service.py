from groq import Groq
from dotenv import load_dotenv

import os
load_dotenv()

client=Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

def stream_groq_responses(history):
    stream=client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        
        stream=True,
        messages=history,
        temperature=0.7
    )

    for chunk in stream:
        if not chunk.choices:
            continue

        delta=chunk.choices[0].delta

        if delta and delta.content:
            yield delta.content