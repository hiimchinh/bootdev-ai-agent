import os
from dotenv import load_dotenv
import sys

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

from google import genai
from google.genai import types
client = genai.Client(api_key=api_key)


user_prompt = sys.argv[1]
argv = sys.argv 

is_verbose = '--verbose' in argv

if not user_prompt:
    print("Usage: python main.py <prompt>")
    sys.exit(1)
messages = [
    types.Content(role="user", parts=[types.Part(text=user_prompt)])
]
res = client.models.generate_content(model="gemini-2.0-flash-001", contents=messages)

if is_verbose:
    print(f"User prompt: {user_prompt}")
    print("Prompt tokens: " + str(res.usage_metadata.prompt_token_count))
    print("Response tokens: " + str(res.usage_metadata.candidates_token_count))