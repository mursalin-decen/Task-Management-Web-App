# 🚀 Task Management Web Application

<div align="center">

  <p>A full-stack, secure, and feature-rich Task Management Web Application built with Python and Flask to boost daily productivity.</p>

  <p>
    <img src="https://img.shields.io/badge/Python-3.x-blue.svg" alt="Python">
    <img src="https://img.shields.io/badge/Flask-3.x-lightgrey.svg" alt="Flask">
    <img src="https://img.shields.io/badge/Database-SQLite-green.svg" alt="SQLite">
    <img src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="License">
  </p>
</div>

---

## ✨ Features

- **🔐 User Authentication:** Secure registration and login using **Bcrypt** password hashing and **Flask-Login** for session management.
- **📝 Task Management (CRUD):** Add, view, update status (Pending/Completed), and delete tasks effortlessly.
- **🏷️ Custom Categories:** Organize your tasks into default categories (Work, Personal, Study) or add your own custom categories.
- **⚡ Priority Levels:** Assign priority tags (`Low`, `Medium`, `High`) to manage urgent tasks efficiently.
- **📊 Dashboard & Metrics:** Real-time overview showing total tasks, completed tasks, and pending items.
- **🔍 Search & Filter:** Quickly find tasks using the title search bar or filter them by status, priority, and category.

---

## 🛠️ Tech Stack

- **Backend:** Python, Flask, Flask-SQLAlchemy (ORM)
- **Authentication:** Flask-Login, Bcrypt
- **Database:** SQLite
- **Frontend:** HTML5, CSS3, Jinja2 Templates

---

## 📁 Project Structure


Task-Management-Web-App/
│
├── app.py                  # Main application & route configurations
├── database.db             # SQLite Database (Auto-generated)
└── templates/              # HTML Templates (Jinja2)
    ├── login.html
    ├── register.html
    ├── dashboard.html
    ├── categories.html
    └── profile.html


----------
🚀 Getting Started
Follow these instructions to run the project locally on your machine.

Prerequisites
Make sure you have Python installed on your system.

Installation Steps
Clone the repository:

Bash
git clone [https://github.com/mursalin-decen/Task-Management-Web-App.git](https://github.com/mursalin-decen/Task-Management-Web-App.git)
cd Task-Management-Web-App
Install required dependencies:

Bash
pip install flask flask-sqlalchemy flask-login bcrypt
Run the application:

Bash
python app.py
Open in your browser:
Open your web browser and go to: http://127.0.0.1:5000

---------------
💡 Usage
Register a new account with your email and password.

Log in to access your personal dashboard.

Manage categories and add tasks with custom priority levels and due dates.

Track your progress and toggle task status as completed when finished!
------------------

🤝 Contributing
Contributions, issues, and feature requests are welcome! Feel free to check the issues page.

-------
👤 Author
Md Mursalin Ahmmed

-------
GitHub: @mursalin-decen
