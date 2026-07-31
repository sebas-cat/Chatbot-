import os
from groq import Groq


def generate_response(user_input,intent,context):
    prompt = f"""You are a university assistant that helps students organize their academic activities.\nThe student said: {user_input}\nIntent detected: {intent}\nContext: {context}\nRespond in Spanish, be concise and helpful."""
    client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
    response = client.chat.completions.create(
        
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}]
        )
    return response.choices[0].message.content