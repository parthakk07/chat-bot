import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")


def generate_response(query):
    client = genai.Client(api_key=API_KEY)
    response = client.models.generate_content(model="gemini-2.5-flash", contents=query)
    return response.text


if __name__ == "__main__":
    while True:
        query = input("Enter query (or 'exit' to quit): ")
        if query.lower() == "exit":
            break
        print(generate_response(query))
