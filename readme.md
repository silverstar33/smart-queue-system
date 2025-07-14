# 🧠 Smart Queue System

A task queue system built with **FastAPI**, **Redis**, and a simple **HTML dashboard** to monitor live tasks, handle failures, view logs, and test real-world DevOps architecture.

---

## 🔧 Features

- ✅ Submit tasks via FastAPI
- 👷 Process background tasks with retry logic
- ❌ Auto-handles task failures and retries
- 📊 Admin dashboard displays:
  - Live and completed tasks
  - Failed tasks with error info
  - 🔍 **Task logs viewable directly from the UI**
- 📝 All logs are saved to `logs/task_queue.log`

---

## 🗂️ Project Structure

```
.
├── main.py               # FastAPI server with API routes
├── redis_queue.py        # Task enqueue logic
├── worker.py             # Background task processor
├── logger.py             # Centralized logger setup
├── templates/
    └── dashboard.html    # HTML dashboard (Admin UI)
├── logs/
│   └── task_queue.log    # Log file (auto-created)
├── requirements.txt      # Python dependencies
├── Dockerfile
├── docker-compose.yml    # Multi-container Docker setup

```
---

## 🚀 Run Locally

Make sure **Redis** is running on `localhost:6379`.

### 🔨 Build & Run Manually

```bash
# Step 1: Build Docker image
docker build -t smart-queue .

# Step 2: Run the container
docker run -p 8000:8000 smart-queue

Visit the app at: http://localhost:8000

📥 Submit Task Example (API)

curl -X POST http://localhost:8000/submit \
  -H "Content-Type: application/json" \
  -d '{"task_name": "test_api", "data": {"key": "value"}}'

💻 Admin Dashboard
Accessible at: http://localhost:8000/admin

Includes:

📋 Live task list with real-time status

✅ Completed task results

❌ Failed task error messages

📁 Log viewer (reads last 50 lines from task_queue.log)

🧪 API Endpoints
Method	Endpoint	Description
POST	/submit	Submit a new task
GET	/admin	View the admin dashboard (UI)
GET	/tasks	Get all pending/processing tasks
GET	/tasks/completed	Get completed tasks
GET	/logs	View last 50 lines from log

🔁 Retry Logic
Max retries per task: 2

Failed tasks are automatically retried

Redis tracks status:

queued

processing

completed

failed

🐳 Coming Soon
✅ Dockerized backend (multi-service with Redis)

🔄 GitHub Actions CI/CD

⚛️ React frontend for the dashboard

✍️ Author
~ Ashwin Bagul

Built with ❤️ as a real-world DevOps & distributed task system showcase.

---