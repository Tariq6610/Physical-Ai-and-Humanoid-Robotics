from fastapi import FastAPI
from backend.src.api import chat as chat_api # Import the chat router

app = FastAPI(title="Physical AI and Humanoid Robotics Backend")

# Include the chat router
app.include_router(chat_api.router)

@app.get("/")
async def root():
    return {"message": "Welcome to the Physical AI and Humanoid Robotics Backend!"}