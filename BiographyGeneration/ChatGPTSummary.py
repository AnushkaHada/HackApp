from openai import OpenAI
import pandas as pd
from dotenv import load_dotenv
import os
import concurrent.futures # neccessary because its taking too long to create new csv file

load_dotenv()  # Load variables from .env

cvs_path = os.path.join(os.path.dirname(__file__), '../ProfilesDataSet/profile_dataset.csv')
profiles_df = pd.read_csv(cvs_path)
#print(profiles_df.columns.tolist())
#print(profiles_df.head(3))


biographies = []
# Initialize OpenAI client using the API key from environment
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)


# function to generate biography for each row 
def generate_bio(row):   
    print("L") 
    #print (f"Row {index}: {row}")
    name = row.get('Name') # gets name from that row
    # row.get returns a string
    # We use eval to turn that string like list into an actual list 
    # kind of a roundabout, but this has to be done due to row.get returning a string. 
    # Now that we have a regular list(["","",...]) we can turn it into a string again :DDDDD
    # Why string? Chat prefers it. The joing command just joins each element with a comma in between. 
    current_skills = row.get('Current_Skills')
    wanted_skills = row.get('Wanted_skills')
    age = row.get('Age')
    college = row.get('College')
    attendance = row.get('Attendance') or "not specified"

    prompt = (
        f"Name is {name}. " 
        f"Age is {age}. "
        f"Current skills they are willing to teach others are {current_skills}. "
        f"Wanted skills they wish someone would teach them are {wanted_skills}. "
        f"College is {college}. "
        f"Attendance is {attendance}."
    )

    completion = client.chat.completions.create(
    model="gpt-4o-mini",
    store=True,
    temperature=0.7,
    max_tokens=300,
    messages=[
        {"role": "system",
        "content": (
            "Write a casual first-person biography without using overly friendly end sentences. "
            "The person is eager to improve skills through learning from others. "
            "Don't mention every skill or detail—feel free to omit some for variety and natural flow. "
            "Keep it to about one paragraph, around 200 words.")},
        {"role": "system", "content": prompt}]
    )
    return completion.choices[0].message.content


max_workers = 5 # num of threads I shall use for side by side processing
with concurrent.futures.ThreadPoolExecutor(max_workers) as executor:
    biographies = list(executor.map(generate_bio, [row for _, row in profiles_df.iterrows()]))

profiles_df['Biography'] = biographies

output_path = os.path.join(os.path.dirname(__file__), '../ProfilesDataSet/complete_profiles.csv')
profiles_df.to_csv(output_path, index=False)