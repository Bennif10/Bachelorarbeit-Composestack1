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




@app.get("/")
def health():
    return {"status": "FastAPI läuft"}


@app.post("/login")
async def login(username: str = Form(...), password: str = Form(...)):

    with users_engine.connect() as conn:
        result = conn.execute(
            text("SELECT password FROM users WHERE username=:u"),
            {"u": username}
        ).fetchone()

    if result and result[0] == password:
        return {"success": True, "username": username}

    raise HTTPException(status_code=401, detail="Invalid login")


@app.post("/workload")
async def create_workload(vm_name: str = Form(...), cpu: int = Form(...), ram: int = Form(...)):

    with data_engine.connect() as conn:
        conn.execute(
            text("""
                INSERT INTO workloads (vm_name, cpu, ram)
                VALUES (:vm_name, :cpu, :ram)
            """),
            {
                "vm_name": vm_name,
                "cpu": cpu,
                "ram": ram
            }
        )
        conn.commit()

    return {"success": True}


@app.get("/workloads")
async def workloads():
    return mock_workload_database