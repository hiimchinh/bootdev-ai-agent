import os
import sys

from dotenv import load_dotenv
from google import genai
from google.genai import types

from functions.call_function import call_function
from functions.get_file_content import schema_get_file_content
from functions.get_files_info import schema_get_files_info
from functions.run_python import schema_run_python_file
from functions.write_file import schema_write_file
from helper import system_prompt

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
        schema_write_file,
    ]
)


def gen_content(messages: list[types.Content]) -> None:
    count = 0
    while count < 20:
        count += 1
        try:
            res = client.models.generate_content(
                model="gemini-2.0-flash-001",
                contents=messages,
                config=types.GenerateContentConfig(
                    system_instruction=system_prompt, tools=[available_functions]
                ),
            )

            if hasattr(res, "candidates") and res.candidates is not None:
                for candidate in res.candidates:
                    if hasattr(candidate, "content") and candidate.content is not None:
                        messages.append(candidate.content)

            if hasattr(res, "function_calls") and res.function_calls:
                func_responses = []
                for function_call_part in res.function_calls:
                    function_call_result = call_function(function_call_part, is_verbose)
                    # Defensive: check function_call_result.parts is not None and has expected structure
                    parts = getattr(function_call_result, "parts", None)
                    if (
                        not parts
                        or not isinstance(parts, list)
                        or len(parts) == 0
                        or not hasattr(parts[0], "function_response")
                    ):
                        raise Exception(
                            "Fatal exception. Function call result parts not found or invalid"
                        )
                    function_response = getattr(parts[0], "function_response", None)
                    func_responses.append(parts[0])
                    func_call_response = (
                        getattr(function_response, "response", None)
                        if function_response
                        else None
                    )
                    if func_call_response is None:
                        raise Exception(
                            "Fatal exception. Function call response not found"
                        )

                    if is_verbose:
                        print(f"-> {func_call_response}")
                messages.append(types.Content(role="user", parts=func_responses))
            else:
                if hasattr(res, "text"):
                    print(f"Final response: {res.text}")
                    break

            if is_verbose:
                print(f"User prompt: {user_prompt}")
                usage_metadata = getattr(res, "usage_metadata", None)
                if usage_metadata:
                    prompt_token_count = getattr(
                        usage_metadata, "prompt_token_count", None
                    )
                    candidates_token_count = getattr(
                        usage_metadata, "candidates_token_count", None
                    )
                    print("Prompt tokens: " + str(prompt_token_count))
                    print("Response tokens: " + str(candidates_token_count))
        except Exception as e:
            print(f"Exception generate function caught: {e}")


gen_content(messages)
