# 🚀 Smart Queue System

A real-world, DevOps-inspired task queue system built with:

- 🧠 **FastAPI** (Python) backend  
- 🧰 **Redis** as the task queue & storage engine  
- 📊 **Live Admin Dashboard** with auto-refresh  
- ⚙️ **Background Worker** for task processing  
- 📡 **REST APIs** for submitting & viewing tasks  
- 🛠️ Built for real-world DevOps architecture demos

---

## 📌 Features

✅ Submit tasks via API  
✅ Background worker picks and processes tasks  
✅ Status tracked live in Redis  
✅ Admin dashboard with tabbed view: **Live** + **Completed**  
✅ FastAPI-powered endpoints  
✅ JSON-based payloads  
✅ Lightweight, no database required

---

## 📂 Folder Structure

smart-queue-system/
├── backend/
│ ├── main.py ← FastAPI app & routes
│ ├── worker.py ← Task processor
│ ├── redis_queue.py ← Redis logic (enqueue/dequeue)
│ └── templates/
│ └── dashboard.html ← Admin dashboard UI
├── .gitignore
├── README.md ← This file

