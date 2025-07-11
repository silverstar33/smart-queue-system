# logger.py (separate file)
import logging
import os

os.makedirs("logs", exist_ok=True)  # create logs directory if it doesn't exist

logging.basicConfig(
    filename="logs/task_queue.log",
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    filemode="a"
)

logger = logging.getLogger("smart_queue")
