import os
import random
import csv
import ast
from django.utils.text import slugify
from django.http import HttpResponseNotFound
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
            
    attend_csv_path = os.path.join(settings.BASE_DIR, 'ProfilesDataSet', 'complete_profiles.csv')
    attendance_set = set()
    with open(attend_csv_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            att = row.get('Attendance', '').strip()
            if att:
                attendance_set.add(att)
    print("Attendance values found:", attendance_set)

    # Get filter from request
    selected_attendance = request.GET.get('attendance')
    
    
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
        user_attendance = user.get('Attendance', '')

        type_match = (
            not selected_type or
            any(hobby_type_map.get(hobby) == selected_type for hobby in user_hobbies)
        )

        attendance_match = (
            not selected_attendance or
            user_attendance == selected_attendance
        )
        
        if type_match and attendance_match:
            filtered_users.append(user)

    return render(request, 'search.html', {
        'users': filtered_users,
        'types': sorted(type_set),
        'attendances': sorted(attendance_set),
        'selected_type': selected_type,
        'selected_attendance': selected_attendance,
    })

def get_npcs():
    csv_path = os.path.join(settings.BASE_DIR, 'complete_profiles.csv')
    users = []
    with open(csv_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            row['slug'] = slugify(row['Name'])  # e.g., "Andre Agassi" → "andre-agassi"
            users.append(row)
    return users

def chatpage(request, username_slug):
    npcs = get_npcs()
    npcs = next((n for n in npcs if n['slug'] == username_slug), None)

    if not npcs:
        return HttpResponseNotFound("User not found")

    return render(request, 'chatpage.html', {'user': npcs})