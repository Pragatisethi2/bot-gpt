from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import create_db_and_tables
from app.routes import conversations

app = FastAPI(title="BOT GPT Backend")

# Add CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

app.include_router(conversations.router, prefix="/api", tags=["Conversations"])

@app.get("/")
def root():
    return {"message": "BOT GPT API is running"}