import os
from dotenv import load_dotenv
import sys
from google import genai
from google.genai import types
from helper import system_prompt
from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_file_content
from functions.run_python import schema_run_python_file
from functions.write_file import schema_write_file

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")


client = genai.Client(api_key=api_key)


user_prompt = sys.argv[1]
argv = sys.argv

is_verbose = "--verbose" in argv

if not user_prompt:
    print("Usage: python main.py <prompt>")
    sys.exit(1)
messages = [types.Content(role="user", parts=[types.Part(text=user_prompt)])]
available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_run_python_file,
        schema_write_file
    ]
)


res = client.models.generate_content(
    model="gemini-2.0-flash-001",
    contents=messages,
    config=types.GenerateContentConfig(system_instruction=system_prompt, tools=[available_functions]),
)
if res.function_calls:
    for function_call_part in res.function_calls:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})") 
else:
    print(res.text)

if is_verbose:
    print(f"User prompt: {user_prompt}")
    print("Prompt tokens: " + str(res.usage_metadata.prompt_token_count))
    print("Response tokens: " + str(res.usage_metadata.candidates_token_count))
