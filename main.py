import argparse
import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

from functions.get_file_info import schema_get_files_info


load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""


available_functions = types.Tool(
    function_declarations=[schema_get_files_info]
)

client = genai.Client(api_key=api_key)

parser = argparse.ArgumentParser(
    prog="ai-agent-python",
    description="Python Agent using the Google Gemini API"
)
parser.add_argument('prompt')
parser.add_argument('--verbose', action='store_true')
args = parser.parse_args()

def main():
    print("Starting model run:")
    messages = [
        types.Content(role="user", parts=[types.Part(text=args.prompt)]),
    ]
    try:
        prompt_result = client.models.generate_content(
            model="gemini-2.0-flash-001",
            contents=messages,
            config=types.GenerateContentConfig(
                tools=[available_functions],
                system_instruction=system_prompt
            )
        )
        if args.verbose:
            print(f"User prompt: {args.prompt}")
            print(f"Prompt tokens: {prompt_result.usage_metadata.prompt_token_count}")
            print(f"Response tokens: {prompt_result.usage_metadata.candidates_token_count}")

        if prompt_result.function_calls:
            for function_call_part in prompt_result.function_calls:
                print(f"Calling function: {function_call_part.name}({function_call_part.args})")
        else:
            print(prompt_result.text)
    except Exception as e:
        print(f"Issues with prompt: {e}")
        exit(1)


if __name__ == "__main__":
    main()
