from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage
import os

load_dotenv()


## Groq Test

model = ChatGroq(model="llama-3.3-70b-versatile", api_key=os.getenv("GROQ_API_KEY"))

messages = [HumanMessage(content="Hello, how are you?")]

result = model.invoke(messages)

print(result.content)

## GitHub API Test

import requests

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

headers = { "Authorization": f"Bearer {GITHUB_TOKEN}" }
url = "https://api.github.com/repos/AafiMansuri/DummyRepo/pulls"
response = requests.get(url, headers=headers)

# print(response.json())

for pr in response.json():
    print(f"PR #{pr['number']} - {pr['title']} - user:{pr['user']['login']}")

