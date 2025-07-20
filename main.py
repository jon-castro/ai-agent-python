import argparse
import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

from functions.dispatcher import call_function
from functions.get_file_info import schema_get_files_info
from functions.get_file_content import schema_get_file_content
from functions.write_file import schema_write_file
from functions.run_python import schema_run_python_file


load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""

available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_write_file,
        schema_run_python_file
    ]
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

    max_iterations = 20
    working_directory = "./calculator"

    for step in range(max_iterations):
        try:
            prompt_result = client.models.generate_content(
                model="gemini-2.0-flash-001",
                contents=messages,
                config=types.GenerateContentConfig(
                    tools=[available_functions],
                    system_instruction=system_prompt
                )
            )

            for candidate in prompt_result.candidates:
                messages.append(candidate.content)

            if args.verbose:
                print(f"User prompt: {args.prompt}")
                print(f"Prompt tokens: {prompt_result.usage_metadata.prompt_token_count}")
                print(f"Response tokens: {prompt_result.usage_metadata.candidates_token_count}")

            if prompt_result.function_calls:
                for function_call in prompt_result.function_calls:
                    function_call_result = call_function(function_call, verbose=True)
                    messages.append(function_call_result)

                    if not function_call_result.parts or not function_call_result.parts[0].function_response:
                        raise RuntimeError("Fatal: Function call did not return a proper response.")

                    # print(f"-> {function_call_result.parts[0].function_response.response}")
            else:
                # print(prompt_result.text)
                final = prompt_result.text
                print("Final response:")
                print(final)
                break

        except Exception as e:
            print(f"Issues with prompt: {e}")
            exit(1)
    else:
        print("Max iterations reached without completion.")


if __name__ == "__main__":
    main()
