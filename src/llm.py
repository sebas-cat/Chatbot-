import os
from unittest import result
import google.generativeai as genai
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

def generate_response(user_input,intent,context):
    model = genai.GenerativeModel("gemini-1.5-flash")
    prompt = f"""You are a university assistant that helps students organize their academic activities.\nThe student said: {user_input}\nIntent detected: {intent}\nContext: {context}\nRespond in Spanish, be concise and helpful."""
    result = model.generate_content(prompt)
    return result.text