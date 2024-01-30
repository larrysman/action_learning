from fastapi import FastAPI, HTTPException, UploadFile, File, Form, Body
from starlette.responses import Response
from pydantic import BaseModel
import joblib
import pandas as pd
from io import StringIO
from typing import Optional
from typing import List
import json
import warnings

# Filter out the scikit-learn warning
warnings.filterwarnings("ignore", category=UserWarning, module="sklearn")
app = FastAPI()

# Load the machine learning model
model = joblib.load('model_name.joblib') # Add model pkl file

class User:
    def __init__(self, first_name, last_name, email, password):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password

class Classification:
    def __init__(self, image_name, disease_classification, accuracy, date_time):
        self.image_name = image_name
        self.disease_classification = disease_classification
        self.accuracy = accuracy
        self.date_time = date_time

class Plant:
    def __init__(self, plant_name, disease_description, num_spots, suggested_category, severity, date_time):
        self.plant_name = plant_name
        self.disease_description = disease_description
        self.num_spots = num_spots
        self.suggested_category = suggested_category
        self.severity = severity
        self.date_time = date_time

users = []  # In-memory storage for users
classifications = []  # In-memory storage for past classifications
plants = []  # In-memory storage for new plant classes

# Endpoint for user sign-up
@app.post('/signup')
async def signup(user: User = Body(...)):
    users.append(user)
    return {'message': 'User signed up successfully'}

# Endpoint for user login
@app.post('/login')
async def login(email: str, password: str):
    # Check if user exists in the in-memory storage
    for user in users:
        if user.email == email and user.password == password:
            return {'message': 'Login successful'}
    raise HTTPException(status_code=401, detail='Invalid credentials')

# Endpoint to save past classifications
@app.post('/save_classification')
async def save_classification(classification: Classification = Body(...)):
    classifications.append(classification)
    return {'message': 'Classification saved successfully'}

# Endpoint to save new plant class (images)
@app.post('/save_plant_class')
async def save_plant_class(plant: Plant = Body(...)):
    plants.append(plant)
    return {'message': 'Plant class saved successfully'}
