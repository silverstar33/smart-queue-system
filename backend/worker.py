import time
import json
import redis
from logger import logger  

MAX_RETRIES = 2  # Number of retries allowed

# Connect to Redis
redis_client = redis.Redis(host='localhost', port=6379, db=0)

QUEUE_NAME = "task_queue"

def process_task(task_id, task_name, task_data): 
    redis_client.hset(f"task:{task_id}", "status", "processing")
    print(f"🚀 Processing task {task_name} (ID: {task_id})")
    logger.info(f"🚀 Processing task {task_name} (ID: {task_id})")  
    
    # Simulate failure for testing
    #raise Exception("Simulated task failure for retry testing")

    # Simulate a processing delay
    time.sleep(5)

    # Dummy success result
    result = f"✅ Task '{task_name}' completed successfully."

    # Save completion result
    redis_client.hset(f"task:{task_id}", mapping={
        "task_id": task_id.replace("task:", ""),
        "status": "completed",
        "result": result
    })

    logger.info(f"✅ Done: {task_name} (ID: {task_id})")
    print(f"✅ Done: {task_name} (ID: {task_id})")

def decode_if_needed(value):
    return value.decode() if isinstance(value, bytes) else value

def worker_loop():
    print("👷 Worker started. Waiting for tasks...")
    logger.info("Worker started and listening for tasks...")    

    while True:
        task = redis_client.blpop(QUEUE_NAME, timeout=10)

        if task:
            _, task_id_raw = task
            task_id = decode_if_needed(task_id_raw).replace("task:", "")
            task_info_raw = redis_client.hgetall(f"task:{task_id}")


            if task_info_raw:
                # Safe decoding of entire task_info
                task_info = {
                    decode_if_needed(k): decode_if_needed(v)
                    for k, v in task_info_raw.items()
                }

                try:
                    task_id = task_info.get("task_id", task_id)
                    task_name = task_info.get("task_name", "Unnamed Task")
                    task_data = json.loads(task_info.get("data", "{}"))
                    retries = int(task_info.get("retries", "0"))

                    logger.info(f"📥 Pulled task {task_name} (ID: {task_id}) from queue")
                    process_task(task_id, task_name, task_data)

                except Exception as e:
                    retries += 1
                    logger.error(f"❌ Task {task_id} failed: {str(e)} | Retry: {retries}")

                    # Update Redis with failure info
                    # Save back to the correct task hash
                    redis_client.hset(f"task:{task_id}", mapping={
                    "status": "failed" if retries >= MAX_RETRIES else "pending",
                    "result": f"❌ Error: {str(e)}",
                    "retries": retries,
                    "task_name": task_name,  # ensure name is preserved
                    "data": json.dumps(task_data)  # ensure data is preserved
                })

                    if retries < MAX_RETRIES:
                        # Requeue task for retry
                        redis_client.rpush(QUEUE_NAME, f"task:{task_id}")
                        logger.info(f"🔁 Requeued task {task_id} (Retry {retries})")
                    else:
                        logger.warning(f"🛑 Task {task_id} exceeded max retries. Marked as failed.")

                    print(f"❌ Failed task {task_id}: {str(e)}")
            else:
                logger.warning(f"⚠️ No task info found for ID: {task_id}")
                print(f"⚠️ No task info found for ID: {task_id}")
        else:
            logger.debug("⏸️ No tasks in queue. Waiting...")
            print("⏸️ No tasks in queue. Waiting...")

if __name__ == "__main__":
    worker_loop()
