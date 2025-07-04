from fastapi import FastAPI
from pydantic import BaseModel
from backend.redis_queue import enqueue_task
import uuid

app = FastAPI()

# Define request model
class TaskRequest(BaseModel):
    task_name: str
    data: dict

@app.post("/submit")
def submit_task(request: TaskRequest):
    task_id = str(uuid.uuid4())
    task_payload = {
        "task_id": task_id,
        "task_name": request.task_name,
        "data": request.data
    }
    enqueue_task(task_payload)
    return {"task_id": task_id}
