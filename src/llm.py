import os
from groq import Groq


def generate_response(user_input,intent,context,history):
    prompt = f"""You are a university assistant that helps students organize their academic activities.\nThe student said: {user_input}\nIntent detected: {intent}\nContext: {context}\nRespond in Spanish, be concise and helpful."""
    system_message = {"role": "system", "content": prompt}
    current_message = {"role": "user", "content": user_input}
    client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
    response = client.chat.completions.create(
    
    
        model="llama-3.1-8b-instant",
        messages=[system_message] + history + [current_message]
    )
    return response.choices[0].message.content

