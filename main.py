import requests 
import json 
from datetime import datetime 
import os 

# personal information
GENDER = "your_gender"
WEIGHT = "weight_kg"
HEIGHT = "height_cm"
AGE = "an_int"

# nutritionX authentication 
API_KEY = os.environ.get("N_API_KEY")
API_ID = os.environ.get("N_API_ID")
ENDPOINT = "https://trackapi.nutritionix.com/v2/natural/exercise"

# SHEETS API INFORMATION
USERNAME = os.environ.get("SHEET_USERNAME")
PROJECT_NAME = "Workout Tracker"
SHEET_NAME = "workouts"
SHEETS_KEY = os.environ.get("SHEETS_KEY")

SHEETS_ENDPOINT = f"https://api.sheety.co/{USERNAME}/{PROJECT_NAME}/{SHEET_NAME}"

sheets_headers = {
    "Authorization": f"Bearer {SHEETS_KEY}",
    }


query = input("What did you do today?\n")

headers = {
    "x-app-id": API_ID,
    "x-app-key": API_KEY, 
}
params = {
    "query": query,
    "gender":GENDER,
    "weight_kg":WEIGHT,
    "height_cm":HEIGHT,
    "age":AGE
}

# get data from NutritionX endpoint
r = requests.post(ENDPOINT, headers=headers, json=params)
data = r.json()

# get current date and time
now = datetime.now()
date = now.strftime("%Y-%m-%d")
time = now.strftime("%H:%M:%S")

# arrange data into dictionary 
exercises = data["exercises"]
def get_params():
    workouts = []
    for exercise in exercises:
        workout = exercise["name"]
        duration = str(exercise["duration_min"])
        calories = str(exercise["nf_calories"])
        workout_data = { "workout": {
            "date": date,
            "time": time,
            "exercise": workout,
            "duration": duration, 
            "calories": calories,
        }
        }
        workouts.append(workout_data)
    return workouts
    

# submit data to sheets API
# # get current rows in sheet
sheets_res = requests.get(SHEETS_ENDPOINT,headers=sheets_headers)
rows_info = sheets_res.json()

# add a row to sheets for each workout completed 
for workout in get_params():
    post_data = requests.post(SHEETS_ENDPOINT, json=workout, headers=sheets_headers)
    print(post_data.raise_for_status)
