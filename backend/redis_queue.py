import redis
import os
import json
from dotenv import load_dotenv

load_dotenv()

redis_client = redis.Redis(
    host=os.getenv("REDIS_HOST"),
    port=int(os.getenv("REDIS_PORT")),
    decode_responses=True
)

QUEUE_NAME = "task_queue"

def enqueue_task(task_data):
    task_id = task_data["task_id"]
    task = {
        "task_id": task_id,
        "task_name": task_data["task_name"],
        "data": json.dumps(task_data["data"]),  # store data as JSON string
        "status": "pending"
    }
    redis_client.hset(task_id, mapping=task)
    redis_client.rpush(QUEUE_NAME, task_id)

def get_task_status(task_id):
    return redis_client.hgetall(task_id)
