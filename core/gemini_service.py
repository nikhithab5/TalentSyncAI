from google import genai
from django.conf import settings

# Create Gemini client
client = genai.Client(api_key=settings.GOOGLE_API_KEY)


def ask_gemini(prompt):
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
        )
        return response.text

    except Exception as e:
        print("Gemini Error:", e)
        return """
⚠️ Gemini AI is currently busy.

This usually happens when Google's servers are under high load.

Please refresh the page after a few seconds.
"""