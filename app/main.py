import os
from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

app = FastAPI()

# 3 Standarduser laut deiner Vorgabe
MOCK_USERS = {
    "user1": "password123",
    "user2": "securepass",
    "admin": "bachelor2026"
}

# Simulierter Datenspeicher für das 2. Frontend (Workloads)
mock_workload_database = []

# WICHTIG: Definiert den Ort der HTML-Dateien im Container-Kontext
# Da das Docker-Image im Ordner '/app' startet, greifen wir direkt auf 'templates' zu
templates = Jinja2Templates(directory="templates")


# 1. ROUTE: Login-Seite anzeigen (GET auf /)
@app.get("/", response_class=HTMLResponse)
async def get_login(request: Request):
    # Rendert die login.html aus dem templates-Ordner
    return templates.TemplateResponse("login.html", {"request": request})


# 2. ROUTE: Login-Formular verarbeiten (POST auf /login)
@app.post("/login")
async def do_login(username: str = Form(...), password: str = Form(...)):
    # Prüfen, ob User existiert und Passwort stimmt
    if username in MOCK_USERS and MOCK_USERS[username] == password:
        # Erfolg -> Status 303 (See Other) zwingt den Browser zu einem GET auf /dashboard
        return RedirectResponse(url="/dashboard", status_code=303)
    else:
        # Fehlgeschlagen -> 401 Unauthorized
        raise HTTPException(status_code=401, detail="Falscher Username oder Passwort")


# 3. ROUTE: Dashboard anzeigen (GET auf /dashboard)
@app.get("/dashboard", response_class=HTMLResponse)
async def get_dashboard(request: Request):
    # Rendert die dashboard.html aus dem templates-Ordner
    return templates.TemplateResponse("dashboard.html", {"request": request})


# 4. ROUTE: Workload-Erstellung (POST vom Dashboard aus)
@app.post("/workload")
async def create_workload(vm_name: str = Form(...), cpu: int = Form(...), ram: int = Form(...)):
    workload_entry = {"vm_name": vm_name, "cpu": cpu, "ram": ram}
    mock_workload_database.append(workload_entry)
    
    # Simulierter Write-Befehl an deine (später) externe Datenbank
    db_url = os.getenv("DATABASE_DATA_URL")
    print(f"[LABOR-LOG] Sende Daten an {db_url}: {workload_entry}")
    
    return {
        "status": "success", 
        "message": f"Workload {vm_name} erfolgreich registriert!", 
        "data": workload_entry
    }