
from openai import OpenAI
import json
import re

client = OpenAI(
    api_key="Your api key",
    base_url="https://generativelanguage.googleapis.com/v1beta/"
)

SYSTEM_PROMPT = """
You are an expert assistant.

You may reason internally, but you MUST NOT reveal your chain of thought.

Return ONLY one valid JSON object.
Do NOT include markdown, emojis, or extra text.

Required JSON format:
{
  "steps": ["string", "string", "..."],
  "result": "string"
}
"""

print("\n")

message_history = [
    {"role": "system", "content": SYSTEM_PROMPT}
]

user_query = input("👉🏻 ")
message_history.append({"role": "user", "content": user_query})

response = client.chat.completions.create(
    model="gemini-2.5-flash-lite",
    messages=message_history
)

raw_result = response.choices[0].message.content.strip()

# 🔧 Defensive JSON extraction (Gemini-safe)
match = re.search(r"\{[\s\S]*\}", raw_result)

if not match:
    print("❌ No valid JSON returned")
    print("Raw output:", raw_result)
    exit()

json_text = match.group()

try:
    parsed = json.loads(json_text)
except json.JSONDecodeError as e:
    print("❌ JSON parsing failed:", e)
    print("Raw JSON:", json_text)
    exit()


print("\n📘 Steps:")
for step in parsed.get("steps", []):
    print("-", step)

print("\n🤖 Result:")
print(parsed.get("result"))

print("\n")
