import os
from fastapi import FastAPI, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Erlaubt Zugriffe vom Frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Für das Labor ausreichend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

MOCK_USERS = {
    "user1": "password123",
    "user2": "securepass",
    "admin": "bachelor2026"
}

mock_workload_database = []


@app.get("/")
def health():
    return {"status": "FastAPI läuft"}


@app.post("/login")
async def login(
    username: str = Form(...),
    password: str = Form(...)
):

    if username in MOCK_USERS and MOCK_USERS[username] == password:
        return {
            "success": True,
            "username": username
        }

    raise HTTPException(
        status_code=401,
        detail="Ungültiger Benutzername oder Passwort"
    )


@app.post("/workload")
async def create_workload(
    vm_name: str = Form(...),
    cpu: int = Form(...),
    ram: int = Form(...)
):

    workload = {
        "vm_name": vm_name,
        "cpu": cpu,
        "ram": ram
    }

    mock_workload_database.append(workload)

    db_url = os.getenv("DATABASE_DATA_URL")

    print(f"[LABOR] Schreibe nach {db_url}: {workload}")

    return {
        "success": True,
        "workload": workload
    }


@app.get("/workloads")
async def workloads():
    return mock_workload_database