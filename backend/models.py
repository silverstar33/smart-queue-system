
import requests
import uuid
import random

names = ["EmailReport", "CleanDB", "ResizeImages", "NotifyAdmin", "BackupData"]
for _ in range(5):
    requests.post("http://localhost:8000/submit", json={
        "task_name": random.choice(names),
        "data": {"ref": str(uuid.uuid4())}
    })
