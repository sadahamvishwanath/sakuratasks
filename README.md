# 🗂️ Sakura Tasks – Task Manager Web App

A simple and clean full-stack Task Manager application built using **Flask, SQLite, HTML, CSS, and JavaScript**.  
This project helps users register, log in, and manage their daily tasks efficiently.

---

## 🚀 Features

- User registration and login system
- Secure password hashing (bcrypt)
- Add new tasks
- Mark tasks as complete/incomplete
- Delete tasks
- User-specific task storage
- REST-style backend API
- Simple and responsive UI

---

## 🛠️ Tech Stack

**Frontend:**
- HTML
- CSS
- JavaScript

**Backend:**
- Python (Flask)
- Flask-CORS

**Database:**
- SQLite

**Security:**
- bcrypt (password hashing)
- JWT-style session handling (if implemented)

---

## 📂 Project Structure


sakuratasks/
│
├── app.py
├── index.html
├── login.html
├── requirements.txt
├── .gitignore
└── instance/
└── sakuratasks.db


## 📸 Preview
![Task Manager Screenshot](screenshot.png)


---

## ⚙️ Installation & Setup

### 1. Clone the repository
```bash
git clone https://github.com/sadahamvishwanath/sakuratasks.git
cd sakuratasks
2. Create virtual environment (optional but recommended)
python -m venv venv
venv\Scripts\activate   # Windows
3. Install dependencies
pip install -r requirements.txt
4. Run the app
python app.py

Then open:

http://127.0.0.1:5000
🎯 What I Learned
Building REST APIs with Flask
Working with SQLite databases
User authentication basics
Password hashing for security
Frontend + backend integration
📌 Future Improvements
Add task categories and filters
Improve UI with modern frontend framework
Add due dates and reminders
Deploy online (Render / Railway / Vercel)
Convert to FastAPI version
👨‍💻 Author

Sadaham Vishwanath
Aspiring AI Engineer & Web Developer
GitHub: @sadahamvishwanath

