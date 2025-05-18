from openai import OpenAI
# Code 

import pandas as pd
from dotenv import load_dotenv
import os

load_dotenv()  # Load variables from .env

client = OpenAI(
  
)

# Initialize OpenAI client using the API key from environment
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

completion = client.chat.completions.create(
  model="gpt-4o-mini",
  store=True,
  temperature=0.7,
  max_tokens=100,
  messages=[
    {"role": "system", "content": "Talk in first-person casually."},
    {"role": "system", "content": "Biography should explain what skills they have and what they want to learn."},
    {"role": "system", "content": "Biography should be made with the intention that person is looking to improve skills through others help."},
  ]
)

print(completion.choices[0].message.content)