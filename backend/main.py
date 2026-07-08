import os

import uvicorn
from fastapi import FastAPI
from src.routers import api_router
from dotenv import load_dotenv

load_dotenv() 

app = FastAPI(
    title="Marketplace Analytics API",
    version="1.0.0",
)

app.include_router(api_router, prefix="/api/v1", tags=["Analytics"])

@app.get("/")
def read_root():
    return {"status": "Server is running successfully!"}

def main():
    uvicorn.run("main:app", host="0.0.0.0", port=int(os.getenv("PORT")), reload=True)

if __name__ == "__main__":
    main()