import pandas as pd
import random
names_df = pd.read_csv('americans_by_descent.csv')
names_df.head()
#print(names_df.columns)

# Hobbies DF
hobbies_df = pd.read_csv('hobbylist.csv')
hobbies_df.head(5)
#print(hobbies_df.columns)

names = names_df["name"]
hobbies = hobbies_df["Hobby-name"]

count = min(len(names), len(hobbies)) # stores the minimum length of the two lists

# Get "count" amount of random names and hobbies
names = names[:count].reset_index(drop=True)
hobbies = hobbies[:count].reset_index(drop=True)

# randomize the hobbies
hobbies = [random.choice(hobbies) for i in range(count)] 

def pick_random_hobby():
    num_skills = random.randint(1,5)
    return random.sample(hobbies, num_skills)

def pick_age():
    return random.randint(18,100)



def pick_random_college():
    colleges = [
        "Cabrillo College", 
        "CSUMB - California State University, Monterey Bay",
        "Santa Cruz County Regional Occupation Program",
        "UCSC - University of California at Santa Cruz",
        "Santa Cruz County Office of Education",
        "Did not attend college",
        "N/A"
    ]
    attendance = ["undergraduate", "masters", "phd", "N/A"]
    
    college = random.choice(colleges)
    if college == "Did not attend college":
        return college, "N/A"
    else:
        return college, random.choice(attendance)



# assign random number of hobbies to each name
current_skills = [pick_random_hobby() for i in range(count)]
wanted_skills = [pick_random_hobby() for i in range(count)]

age = [pick_age() for i in range(count)]



# new dataframe
merge_df = pd.DataFrame({
    "Name": names,
    "Current_Skills": current_skills,
    "Wanted_skills": wanted_skills,
    "Age" : age
})


print(merge_df.head())
merge_df.to_csv('profile_dataset.csv', index = False) # so it does not add extra column with number
