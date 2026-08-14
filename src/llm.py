import os
from groq import Groq


def generate_response(user_input,intent,context,history):
    prompt = f"""You are Luma, an intelligent university assistant with direct access to Google Calendar. You CAN and DO create calendar events automatically — you don't need to instruct the user to do it manually.The student said: {user_input}Intent detected: {intent}Context: {context}If an event was just created, confirm it was added to their Google Calendar.Respond in Spanish, be concise."""
    system_message = {"role": "system", "content": prompt}
    current_message = {"role": "user", "content": user_input}
    client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
    response = client.chat.completions.create(
    
    
        model="openai/gpt-oss-20b",
        messages=[system_message] + history + [current_message]
    )
    return response.choices[0].message.content

