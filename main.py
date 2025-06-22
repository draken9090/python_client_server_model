import os
import sqlite3
import aiosqlite
from contextlib import asynccontextmanager
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# Load environment variables from .env
load_dotenv()

# Pydantic model for request body
class Student(BaseModel):
    roll_number: int
    name: str

# SQLite database file path
DATABASE_FILE = os.getenv("DATABASE_FILE", "student_records.db")

async def init_db():
    """Create SQLite table if not exists"""
    async with aiosqlite.connect(DATABASE_FILE) as db:
        await db.execute(
            """
            CREATE TABLE IF NOT EXISTS student_record (
                roll_number INTEGER PRIMARY KEY,
                name TEXT NOT NULL
            );
            """
        )
        await db.commit()

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application lifespan"""
    # Startup: initialize database
    await init_db()
    yield
    # Shutdown: nothing to cleanup for SQLite

app = FastAPI(lifespan=lifespan)

# Allow CORS from any origin
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/add_record")
async def add_record(student: Student):
    """Add a new student record"""
    try:
        async with aiosqlite.connect(DATABASE_FILE) as db:
            await db.execute(
                "INSERT INTO student_record (roll_number, name) VALUES (?, ?)",
                (student.roll_number, student.name)
            )
            await db.commit()
            return {"status": "success", "message": "Record added."}
    except sqlite3.IntegrityError:
        raise HTTPException(status_code=400, detail="Roll number already exists.")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=int(os.getenv("PORT", 8000)),
        reload=True,
    )
