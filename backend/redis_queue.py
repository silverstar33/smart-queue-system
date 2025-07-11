import redis
import os
import uuid
import json
from dotenv import load_dotenv

load_dotenv()

redis_client = redis.Redis(
    host=os.getenv("REDIS_HOST"),
    port=int(os.getenv("REDIS_PORT")),
    decode_responses=True
)

QUEUE_NAME = "task_queue"

def enqueue_task(task_id: str, data: dict, task_name: str):
    task_key = f"task:{task_id}"
    
    redis_client.hset(task_key, mapping={
        "task_id": task_id,
        "task_name": task_name,
        "data": json.dumps(data),
        "status": "pending",
        "result": ""
    })

    redis_client.rpush("task_queue", task_key)


def get_task_status(task_id):
    redis_key = f"task:{task_id}"
    return redis_client.hgetall(redis_key)
