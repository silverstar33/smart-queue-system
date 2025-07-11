import redis
import json
import uuid
import random
from datetime import datetime

# Connect to Redis
r = redis.Redis(host='localhost', port=6379, db=0)
QUEUE_NAME = "task_queue"

# Sample task name templates
task_names = [
    "Email Blast", "Generate Report", "PDF Export", "Data Sync", "Image Resize",
    "User Notification", "Cleanup Task", "Token Refresh", "Upload File", "Backup DB"
]

# Random data generators
def random_email():
    domains = ["example.com", "mail.com", "test.org"]
    return f"user{random.randint(1, 999)}@{random.choice(domains)}"

def random_payload():
    return {
        "user": random_email(),
        "priority": random.choice(["high", "medium", "low"]),
        "timestamp": datetime.utcnow().isoformat()
    }

# Generate N tasks
def generate_tasks(n=5):
    for _ in range(n):
        task_id = f"task:{uuid.uuid4()}"
        task_name = random.choice(task_names)
        data = random_payload()

        task_data = {
            "task_id": task_id,
            "task_name": task_name,
            "status": "pending",
            "data": data
        }

        # Store in Redis as hash
        r.hset(task_id, mapping={
            "task_id": task_id,
            "task_name": task_name,
            "status": "pending",
            "data": json.dumps(data)
        })

        # Push to task queue
        r.rpush(QUEUE_NAME, task_id)

        print(f"✅ Task pushed: {task_name} | ID: {task_id}")

# Run it
if __name__ == "__main__":
    generate_tasks(n=10)  # change to any number you want
