import google.generativeai as genai
from django.conf import settings

# Configure Gemini with your API key
genai.configure(api_key=settings.GOOGLE_API_KEY)

# Load the Gemini model
model = genai.GenerativeModel("gemini-2.5-flash")


def ask_gemini(prompt):
    response = model.generate_content(prompt)
    return response.text