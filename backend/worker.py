import time
import json
import redis

# Connect to Redis
redis_client = redis.Redis(host='localhost', port=6379, db=0)

QUEUE_NAME = "task_queue"

def process_task(task_id, task_name, task_data): 
    # Set status to processing
    redis_client.hset(f"task:{task_id}", "status", "processing")
    print(f"🚀 Processing task  {task_name} (ID: {task_id})")
    
    # Simulate a processing delay (e.g., sending email, generating report, etc.)
    time.sleep(5)

    # Dummy result - you can customize this per task
    result = f"✅ Task '{task_name}' completed successfully."

    # Update task status and result
    redis_client.hset(f"task:{task_id}", mapping={
    "task_id": task_id.replace("task:", ""),  # clean ID
    "status": "completed",
    "result": result
})


    print(f"✅ Done: {task_name} (ID: {task_id})")

def worker_loop():
    print("👷 Worker started. Waiting for tasks...")

    while True:
        task = redis_client.blpop(QUEUE_NAME, timeout=10)

        if task:
            _, task_id = task
            task_id = task_id.decode()  # decode bytes
            # Get full task details from Redis
            task_info = redis_client.hgetall(task_id)

            if task_info:
                try:
                    task_id = task_info.get(b"task_id", task_id).decode()
                    task_name = task_info.get(b"task_name", b"Unnamed Task").decode()
                    task_data = json.loads(task_info.get(b"data", b"{}").decode())

                    process_task(task_id, task_name, task_data)

                except Exception as e:
                    redis_client.hset(task_id, mapping={
                        "status": "failed",
                        "result": f"❌ Error: {str(e)}"
                    })
                    print(f"❌ Failed task {task_id}: {str(e)}")
            else:
                print(f"⚠️ No task info found for ID: {task_id}")
        else:
            print("⏸️ No tasks in queue. Waiting...")


if __name__ == "__main__":
    worker_loop()
