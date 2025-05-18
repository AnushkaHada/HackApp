import os
import random
import csv
import ast
from django.shortcuts import render
from django.conf import settings

def homagepage(request):
   return render(request, 'home.html')

def aboutpage(request):
    return render(request, 'about.html')

def searchpage(request):
    datapath = os.path.join(settings.BASE_DIR, 'static', 'complete_profiles.csv')
    pfp_dir = os.path.join(settings.BASE_DIR,'static', 'profile_pics')
    pfp_files = [f for f in os.listdir(pfp_dir) if not f.startswith('.')]
    
    npc_users = []
    
    with open(datapath, newline = '', encoding = 'utf-8') as csvfile:
        user_database = csv.DictReader(csvfile)
        for row in user_database:
            try:
                row['Current_Skills'] =  ast.literal_eval(row['Current_Skills'])
            except Exception:
                row['Current_Skills'] =  [row['Current_Skills']]
            try:
                row['Wanted_skills'] =  ast.literal_eval(row['Wanted_skills'])
            except Exception:
                row['Wanted_skills'] =  [row['Wanted_skills']]
                
            row['profile_pic'] = random.choice(pfp_files)
            npc_users.append(row)
    
    # Load hobby types and mapping
    hobby_csv_path = os.path.join(settings.BASE_DIR, 'ProfilesDataSet', 'hobbylist.csv')
    type_set = set()
    hobby_type_map = {}
    with open(hobby_csv_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            type_set.add(row['Type'])
            hobby_type_map[row['Hobby-name']] = row['Type']

    # Get filter from request
    selected_type = request.GET.get('type')

    # Filter users by hobby type if selected
    filtered_users = []
    for user in npc_users:
        user_hobbies = user.get('Current_Skills', [])
        if not selected_type or any(hobby_type_map.get(hobby) == selected_type for hobby in user_hobbies):
            filtered_users.append(user)

    return render(request, 'search.html', {
        'users': filtered_users,
        'types': sorted(type_set),
        'selected_type': selected_type,
    })