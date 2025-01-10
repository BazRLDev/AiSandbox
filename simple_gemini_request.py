import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

def ask_the_geini(question):
	genai.configure(api_key=GEMINI_API_KEY, transport='rest')
	model = genai.GenerativeModel("gemini-1.5-flash")
	response = model.generate_content(question)
	print(response.text)
	print('#########')
	print(dir(response))
	print('#########')
	print(vars(response))
	print('#########')

def main():
	question = 'explain how AI works'
	ask_the_geini(question)

if __name__ == "__main__":
    main()