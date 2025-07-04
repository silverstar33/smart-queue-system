import time
import json
import redis

# Connect to Redis
redis_client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

QUEUE_NAME = "task_queue"

def process_task(task_data):
    print(f"🚀 Processing task: {task_data}")
    time.sleep(5)  # Simulate 5-second processing delay
    print(f"✅ Task completed: {task_data}")

def worker_loop():
    print("👷 Worker started. Waiting for tasks...")
    while True:
        task = redis_client.blpop(QUEUE_NAME, timeout=10)
        if task:
            _, task_id = task
            task_info = redis_client.hgetall(task_id)
            
            if not task_info:
                print(f"⚠️ No data found for task ID: {task_id}")
                continue

            try:
                task_data = json.loads(task_info["data"])
            except json.JSONDecodeError:
                print(f"❌ Error decoding task data for ID {task_id}: {task_info['data']}")
                redis_client.hset(task_id, "status", "error")
                continue

            process_task(task_data)
            redis_client.hset(task_id, "status", "completed")
        else:
            print("⏸️ No tasks in queue. Waiting...")

if __name__ == "__main__":
    worker_loop()
