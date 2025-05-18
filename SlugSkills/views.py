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
    datapath = os.path.join(settings.BASE_DIR, 'static', 'profile_dataset.csv')
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
    
    return render(request, 'search.html', {'users': npc_users})