import os

import uvicorn
from fastapi import FastAPI
from src.routers import api_router
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware

load_dotenv() 

app = FastAPI(
    title="Marketplace Analytics API",
    version="1.0.0",
)
origins_str = os.getenv("ORIGIN_ALLOWED")
origins = [origin.strip() for origin in origins_str.split(",")]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api/v1")

@app.get("/")
def read_root():
    return {"status": "Server is running successfully!"}

def main():
    uvicorn.run("main:app", host="0.0.0.0", port=int(os.getenv("PORT")), reload=True)

if __name__ == "__main__":
    main()