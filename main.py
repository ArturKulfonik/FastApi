from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, constr
from typing import List, Optional
from uuid import uuid4
app = FastAPI()


# Model danych dla zadania
class Task(BaseModel):
   id: str
   title: constr(minLength=3, maxLength=100)
   description: Optional[constr(maxLength=300)] = None
   status: str = "do wykonania"


tasks: List[Task] = []


status= ["do wykonania", "w trakcie", "zakończone"]


@app.post("/tasks", responseModel=Task)
def create_task(task: Task):


   if any(t.title == task.title for t in tasks):
       raise HTTPException(status_code=400, detail="Tytuł musi być unikalny")


   if task.status not in status:
       raise HTTPException(status_code=400, detail="Status musi być jednym z: " + ", ".join(status))


   task.id = str(uuid4())
   tasks.append(task)
   return task


@app.get("/tasks", responseModel=List[Task])
def getTasks(status: Optional[str] = Query(None)):
   if status:
       if status not in status:
           raise HTTPException(status_code=404, detail="Nie ma takiego zadania")
       return [task for task in tasks if task.status == status]
   return tasks


@app.get("/tasks/{task_id}", responseModel=Task)
def getTask(task_id: str):
   for task in tasks:
       if task.id == task_id:
           return task
   raise HTTPException(status_code=404, detail="Nie ma zadanie o takim ID")


@app.put("/tasks/{task_id}", responseModel=Task)
def updateTask(task_id: str, updatedTask: Task):
   for id, task in enumerate(tasks):
       if task.id == task_id:
           if any(t.title == updatedTask.title for t in tasks if t.id != task_id):
               raise HTTPException(status_code=400, detail="Tytuł musi być unikalny")


           tasks[id].title = updatedTask.title
           tasks[id].description = updatedTask.description
           tasks[id].status = updatedTask.status
           return tasks[id]


   raise HTTPException(status_code=404, detail="Nie ma zadanie o takim ID")


@app.delete("/tasks/{task_id}")
def deleteTask(task_id: str):
   for id, task in enumerate(tasks):
       if task.id == task_id:
           del tasks[id]
           return {"detail": "Zadanie zostało usunięte"}


   raise HTTPException(status_code=404, detail="Nie ma zadanie o takim ID")

