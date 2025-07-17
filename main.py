import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types


load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)

def main():
    print("Starting model run:")
    content_input = sys.argv[1]
    messages = [
        types.Content(role="user", parts=[types.Part(text=content_input)]),
    ]
    try:
        prompt_result = client.models.generate_content(
            model="gemini-2.0-flash-001",
            contents=messages
        )
        print(prompt_result.text)
        print(f"Prompt tokens: {prompt_result.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {prompt_result.usage_metadata.candidates_token_count}")
    except Exception as e:
        print(f"Issues with prompt: {e}")
        exit(1)


if __name__ == "__main__":
    main()
