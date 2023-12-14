from typing import Annotated
from fastapi import FastAPI, Form
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import uvicorn
from database import Database
from model import Task

app = FastAPI()
templates = Jinja2Templates(directory="www")

db = Database("db.db")

@app.on_event("startup")
async def on_startup():
    Task.create_table(db)

@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse("index.html", { "request": request })

@app.get("/tasks/", response_class=HTMLResponse)
def get_tasks(request: Request):
    return templated_tasks(request)

@app.post("/tasks/", response_class=HTMLResponse)
def create_task(request: Request, description: Annotated[str, Form()]):
    Task.create_task(db, description)
    return templated_tasks(request)

@app.put("/tasks/{id}", response_class=HTMLResponse)
def update_task(request: Request, id: int):
    Task.update_task(db, id)
    return templated_tasks(request)

@app.delete("/tasks/{id}", response_class=HTMLResponse)
def remove_task(request: Request, id: int):
    Task.remove_task(db, id)
    return templated_tasks(request)

def templated_tasks(request: Request):
    tasks = Task.get_tasks(db)
    return templates.TemplateResponse("tasks.html", { "request": request, "tasks": tasks })

if __name__ == "__main__":
    uvicorn.run("main:app", port=5000)
