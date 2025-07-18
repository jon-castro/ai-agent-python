import argparse
import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types


load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

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
            contents=messages
        )
        if args.verbose:
            print(f"User prompt: {args.prompt}")
            print(f"Prompt tokens: {prompt_result.usage_metadata.prompt_token_count}")
            print(f"Response tokens: {prompt_result.usage_metadata.candidates_token_count}")
        print(prompt_result.text)
    except Exception as e:
        print(f"Issues with prompt: {e}")
        exit(1)


if __name__ == "__main__":
    main()
