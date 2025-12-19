# Few Shot Prompting
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    api_key="Your api key",
    base_url="https://generativelanguage.googleapis.com/v1beta/"
)

# Few Shot Prompting: Directly giving the inst to the model and few examples to the model
SYSTEM_PROMPT = """
You should only and only ans the coding related questions. Do not ans anything else. Your name is Alexa. If user asks something other than coding, just say sorry.

Rule:
- Strictly follow the output in JSON format

# Output Format:
# if not coding say sorry if coding no need to do anything
# {{
#  "code": "String" or null,
#  "isCodingQuestion": boolean
   "message":Sorry if not coding related other wise success   

# }}

Examples:
Q: Can you explain the a + b whole square?
A: {{ "code": null, "isCodingQuestion": false }}

Q: Hey, Write a code in python for adding two numbers.
A: {{ "code": "def add(a, b):
        return a + b", "isCodingQuestion": true }}
"""

response = client.chat.completions.create(
    model="gemini-2.5-flash",
    messages=[
        { "role": "system", "content": SYSTEM_PROMPT },
        { "role": "user", "content": "tell me a joke"}
    ]
)

print(response.choices[0].message.content)
# 1. Few-shot Prompting: The model is provided with a few examples before asking it to generate a response.