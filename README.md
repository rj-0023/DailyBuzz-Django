# 📝 Django Todo List App with News & Weather

A full-featured Django-based task management app that includes:

- ✅ Task CRUD with user authentication
- 🌦️ Real-time weather info using `python-weather`
- 📰 Latest headlines using NewsAPI
- 🔒 Secure environment variable handling with `.env`

---

## 🚀 Features

- User registration, login, logout
- Create, read, update, delete (CRUD) tasks
- Displays top news headlines from the US
- Get live weather updates for any city
- DRF (Django Rest Framework) API integration for tasks
- Uses `.env` for API keys and secrets

---

## 🛠️ Tech Stack

- Python 3.x
- Django
- Django REST Framework
- NewsAPI
- python-weather
- Bootstrap (for frontend)
- dotenv (for secure env config)

---
🧪 API Usage
Get TodoList via API

**GET /api/todos/**

Post a New Todo
**POST /api/todos/**


📌 Screens
home.html — Homepage

tasks.html — Todo dashboard with weather and news

create_task.html, update_task.html

register.html, login.html


🚀 Feature Upgrade Idea: Smart Task Creation with NLP
🧠 How it works:
User enters a phrase like:
“Running at 5 AM”

App uses NLP to extract:

Task → “Running”

Time → “5 AM”

Then auto-fills the task form or creates it directly.

💡 Credits
NewsAPI - https://newsapi.org/

python-weather - https://pypi.org/project/python-weather/

Django Team
