from fastapi import FastAPI, HTTPException, Body
from pydantic import BaseModel
import asyncpg
from datetime import datetime

app = FastAPI()

# Database configuration
DATABASE_URL = "postgresql+asyncpg://postgres:admin@5432/plant_disease"
pool = None

class User(BaseModel):
    first_name: str
    last_name: str
    email: str
    password: str

class Classification(BaseModel):
    image_name: str
    disease_classification: str
    accuracy: float
    date_time: datetime

class Plant(BaseModel):
    plant_name: str
    disease_description: str
    num_spots: int
    suggested_category: str
    severity: str
    date_time: datetime

async def get_pool():
    global pool
    if pool is None:
        pool = await asyncpg.create_pool(DATABASE_URL)
    return pool

# Endpoint for user sign-up
@app.post('/signup')
async def signup(user: User = Body(...)):
    pool = await get_pool()
    async with pool.acquire() as connection:
        await connection.execute(
            "INSERT INTO users (first_name, last_name, email, password) VALUES ($1, $2, $3, $4)",
            user.first_name, user.last_name, user.email, user.password
        )
    return {'message': 'User signed up successfully'}

# Endpoint for user login
@app.post('/login')
async def login(email: str, password: str):
    pool = await get_pool()
    async with pool.acquire() as connection:
        result = await connection.fetchrow(
            "SELECT * FROM users WHERE email = $1 AND password = $2",
            email, password
        )
        if result:
            return {'message': 'Login successful'}
    raise HTTPException(status_code=401, detail='Invalid credentials')

# Endpoint to save past classifications
@app.post('/save_classification')
async def save_classification(classification: Classification = Body(...)):
    pool = await get_pool()
    async with pool.acquire() as connection:
        await connection.execute(
            "INSERT INTO classifications (image_name, disease_classification, accuracy, date_time) "
            "VALUES ($1, $2, $3, $4)",
            classification.image_name, classification.disease_classification,
            classification.accuracy, classification.date_time
        )
    return {'message': 'Classification saved successfully'}

# Endpoint to save new plant class (images)
@app.post('/save_plant_class')
async def save_plant_class(plant: Plant = Body(...)):
    pool = await get_pool()
    async with pool.acquire() as connection:
        await connection.execute(
            "INSERT INTO plants (plant_name, disease_description, num_spots, suggested_category, severity, date_time) "
            "VALUES ($1, $2, $3, $4, $5, $6)",
            plant.plant_name, plant.disease_description, plant.num_spots,
            plant.suggested_category, plant.severity, plant.date_time
        )
    return {'message': 'Plant class saved successfully'}

