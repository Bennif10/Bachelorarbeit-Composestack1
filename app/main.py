from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy import create_engine, text


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------- DB 1: USERS ----------------
DB_HOST_USERS = "10.1.90.121"
DB_USER = "user"
DB_PASS = "password"
DB_NAME_USERS = "users_db"

USERS_DB_URL = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST_USERS}:5432/{DB_NAME_USERS}"
users_engine = create_engine(USERS_DB_URL, pool_pre_ping=True)

# ---------------- DB 2: WORKLOADS ----------------
DB_HOST_WORKLOADS = "10.1.90.122"
DB_NAME_WORKLOADS = "frontend_data_db"

WORKLOAD_DB_URL = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST_WORKLOADS}:5432/{DB_NAME_WORKLOADS}"
workload_engine = create_engine(WORKLOAD_DB_URL, pool_pre_ping=True)

# ---------------- MODELS ----------------
class LoginRequest(BaseModel):
    username: str
    password: str

class Workload(BaseModel):
    vm_name: str
    cpu: int
    ram: int
# ---------------- ROUTES ----------------

@app.get("/")
def health():
    return {"status": "FastAPI läuft"}

# LOGIN
@app.post("/login")
def login(data: LoginRequest):
    with users_engine.connect() as conn:
        result = conn.execute(
            text("SELECT password FROM users WHERE username=:u"),
            {"u": data.username}
        ).fetchone()

    if result and result[0] == data.password:
        return {"success": True, "username": data.username}

    raise HTTPException(status_code=401, detail="Invalid login")

@app.post("/workload")
async def create_workload(payload: Workload):
    with workload_engine.begin() as conn:
        conn.execute(
            text("""
                INSERT INTO workloads (vm_name, cpu, ram)
                VALUES (:vm_name, :cpu, :ram)
            """),
            {
                "vm_name": payload.vm_name,
                "cpu": payload.cpu,
                "ram": payload.ram
            }
        )

    return {"success": True, "message": "Workload gespeichert"}
