from openai import OpenAI
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
  messages=[
    {"role": "user", "content": "write a haiku about ai"}
  ]
)

print(completion.choices[0].message)