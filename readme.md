# 🧠 Smart Queue System

A task queue system built with FastAPI, Redis, and a simple HTML dashboard for monitoring live tasks, errors, retries, and logs.

## 🔧 Features

- ✅ Enqueue tasks via FastAPI
- 👷 Background worker processes tasks with retry logic
- ❌ Automatically handles task failures and retries
- 📊 Admin dashboard shows:
  - Live tasks
  - Completed tasks
  - Failed tasks
  - 🔍 **Viewable task logs directly from UI**
- 📝 Logs saved to `logs/task_queue.log`

## 🗂️ Project Structure


├── main.py # FastAPI server with all routes
├── redis_queue.py # Task enqueue logic
├── worker.py # Background task processor
├── logger.py # Centralized logging setup
├── templates/ # HTML dashboard ( Admin UI)
├── logs/
│   └── task_queue.log # Log file (auto-created)
├── requirements.txt
├── Dockerfile

## 🚀 Run Locally

Make sure Redis is running on `localhost:6379`.

# Build the Docker image
docker build -t smart-queue .

# Run the container
docker run -p 8000:8000 smart-queue

Then visit: http://localhost:8000

📥 Submit Task Example
curl -X POST http://localhost:8000/submit \
-H "Content-Type: application/json" \
-d '{"task_name": "test_api", "data": {"key": "value"}}'
------------------------------------------------------

visit for Admin UI: http://localhost:8000/admin

💻 UI Dashboard
The admin dashboard includes:

📋 Live task list with status

✅ Completed task results

❌ Failed task error messages

📁 Task log viewer (reads from logs/task_queue.log on backend)

🧪 API Endpoints
POST /submit – Submit a new task

GET /admin – Admin dashboard (UI)

GET /tasks – Fetch all non-completed tasks

GET /tasks/completed – Fetch completed tasks

GET /logs – Fetch log file content view last 50 lines of log (Plain Text)

🖥️ Admin Dashboard
Available at: GET /admin

Features:

📌 Task name, ID, status, retries

✅ See all queued, failed, and completed tasks

📜 View logs directly on the dashboard (uses /logs API)

🔁 Retry Logic
Max retries: 2

Failed tasks are retried automatically

Status is updated in Redis (status: failed | completed | processing)

🐳 Coming Soon (Planned)
Docker setup for backend

GitHub Actions CI/CD

React frontend for dashboard (currently pure HTML)

--------------------------------------------------
Author 
~Ashwin Bagul

Built with ❤️ for real-world DevOps use case demonstration.

