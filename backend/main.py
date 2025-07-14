from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel
from fastapi.responses import PlainTextResponse

import uuid
import os
import json
from logger import logger


from redis_queue import enqueue_task, redis_client

app = FastAPI()
templates = Jinja2Templates(directory="templates")

QUEUE_NAME = "task_queue"

class TaskRequest(BaseModel):
    task_name: str
    data: dict

# ---------- Submit New Task ----------
@app.post("/submit")
def submit_task(request: TaskRequest):
    task_id = str(uuid.uuid4())
    enqueue_task(task_id, request.data, request.task_name)
    logger.info(f"Submitted task {task_id} - {request.task_name}")
    return {"task_id": task_id}


# ---------- Admin Dashboard ----------
@app.get("/admin", response_class=HTMLResponse)
def admin_dashboard(request: Request):
    tasks = []

    for key in redis_client.scan_iter("task:*"):
        try:
            task_info = redis_client.hgetall(key)
            task = {k.decode(): v.decode() for k, v in task_info.items()}

            tasks.append({
                "task_id": task.get("task_id", key.decode()),
                "task_name": task.get("task_name", "Unnamed Task"),
                "data": task.get("data", "{}"),
                "status": task.get("status", "unknown"),
                "result": task.get("result", ""),
                "retries": int(task.get("retries", "0"))
            })

        except Exception as e:
            print(f"[ERROR] Failed to process task {key}: {e}")

    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "tasks": tasks
    })


# ---------- All Tasks in Queue ----------
@app.get("/tasks")
def list_tasks():
    tasks = []

    for key in redis_client.scan_iter("task:*"):
        try:
            key_str = key.decode() if isinstance(key, bytes) else key
            task_info = redis_client.hgetall(key_str)

            if not task_info:
                continue

            task = {}
            for k, v in task_info.items():
                k_str = k.decode() if isinstance(k, bytes) else k
                v_str = v.decode() if isinstance(v, bytes) else v
                task[k_str] = v_str

            # ✅ Skip if task is completed
            if task.get("status", "").lower() == "completed":
                continue

            try:
                data = json.loads(task.get("data", "{}"))
            except Exception:
                data = {"error": "Invalid data"}

            tasks.append({
                "task_id": task.get("task_id", key_str),
                "task_name": task.get("task_name", "Unnamed Task"),
                "status": task.get("status", "unknown"),
                "data": data,
                "retries": int(task.get("retries", "0"))
            })

        except Exception as e:
            print(f"[ERROR] Failed to parse task: {e}")

    return tasks





# ---------- Completed Tasks ----------
@app.get("/tasks/completed")
def get_completed_tasks():
    tasks = []

    for key in redis_client.scan_iter("task:*"):
        try:
            # Safely decode key
            key_str = key.decode() if isinstance(key, bytes) else key
            task_info = redis_client.hgetall(key_str)

            # Safely decode all hash fields
            task = {}
            for k, v in task_info.items():
                k_str = k.decode() if isinstance(k, bytes) else k
                v_str = v.decode() if isinstance(v, bytes) else v
                task[k_str] = v_str

            if task.get("status", "").lower() == "completed":
                tasks.append({
                    "task_id": task.get("task_id", key_str),
                    "task_name": task.get("task_name", "Unnamed Task"),
                    "result": task.get("result", "✅ Task completed successfully.")
                })

        except Exception as e:
            print(f"[ERROR] Failed to process completed task {key}: {e}")

    return JSONResponse({"tasks": tasks})

# ---------- Get Logs ----------
@app.get("/logs", response_class=PlainTextResponse)
def get_logs():
    log_path = os.path.abspath(os.path.join("logs", "task_queue.log"))
    try:
        with open(log_path, "r") as log_file:
            lines = log_file.readlines()
            return ''.join(lines[-50:])  # Return the last 50 lines
    except Exception as e:
        return f"❌ Error reading log: {str(e)}"
