from dotenv import load_dotenv
from openai import OpenAI
load_dotenv()

client = OpenAI(
    api_key="your api key",
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)
#Zero shot prompts means direclty giving instructions
SYSTEM_PROMPT="You should only coding related question,do not answer any thing else just say sorry , you name is alexa the coding assistant"
response = client.chat.completions.create(
    model="gemini-2.5-flash",
    messages=[
        {"role": "system", "content":SYSTEM_PROMPT },
        {
            "role": "user",
            "content": "write a java program to print hello world"
            #Zero-shot prompting: model is given direct question or task wihout prior example
        }
    ]
)

print(response.choices[0].message.content)