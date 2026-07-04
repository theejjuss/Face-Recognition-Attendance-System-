<div align="center">

# 🎯 Face Recognition Attendance System

<img src="https://readme-typing-svg.demolab.com?font=Poppins&size=28&duration=3000&pause=1000&color=00C853&center=true&vCenter=true&width=700&lines=Face+Recognition+Attendance+System;OpenCV+%7C+Python+%7C+SQLite;Automatic+Attendance+Using+AI;Modern+Desktop+Application" />

<p align="center">

![Python](https://img.shields.io/badge/Python-3.10+-blue?style=for-the-badge&logo=python)
![OpenCV](https://img.shields.io/badge/OpenCV-Computer%20Vision-green?style=for-the-badge&logo=opencv)
![SQLite](https://img.shields.io/badge/SQLite-Database-blue?style=for-the-badge&logo=sqlite)
![Tkinter](https://img.shields.io/badge/Tkinter-GUI-orange?style=for-the-badge)

</p>

---

### 📷 AI Powered Attendance Management

Automatically recognize students using facial recognition and record attendance instantly.

</div>

---

# ✨ Features

✅ Face Recognition Attendance

✅ Automatic Face Dataset Collection

✅ AI Model Training (LBPH)

✅ Admin Login

✅ Student Login

✅ Attendance Percentage

✅ Daily CSV Export

✅ Excel Export with Face Images

✅ Automatic Absentee Marking

✅ Modern Tkinter Interface

---

# 🎬 Demo Workflow

```text
Register Student
       │
       ▼
Capture 60 Face Images
       │
       ▼
Train AI Model
       │
       ▼
Start Attendance
       │
       ▼
Recognize Face
       │
       ▼
Mark Present
       │
       ▼
Export CSV / Excel
```

---

# 🛠 Tech Stack

| Technology | Purpose |
|------------|----------|
| Python | Backend |
| OpenCV | Face Detection |
| LBPH | Face Recognition |
| SQLite | Database |
| Tkinter | Desktop GUI |
| Pandas | Excel Export |
| Pillow | Image Processing |

---

# 📦 Installation

Clone the repository

```bash
git clone https://github.com/yourusername/fra_system.git
```

Move into the project

```bash
cd fra_system
```

Install dependencies

```bash
pip install -r requirements.txt
```

Run the application

```bash
python main.py
```

---

# 🔐 Default Admin Login

| Username | Password |
|----------|----------|
| admin | admin123 |

> Change the password after first login.

---

# 🚀 Usage Guide

## ① Register Student

- Login as Admin
- Open Register User
- Enter Student ID
- Enter Student Name
- Camera automatically captures **60 images**

---

## ② Train Model

Click

```
Train Model
```

Wait a few seconds.

Repeat whenever new students are added.

---

## ③ Take Attendance

Click

```
Start Attendance
```

Students simply look at the camera.

Attendance is recorded automatically.

---

## ④ Mark Absentees

At the end of the day

```
Mark Absentees
```

Students not detected become **Absent**.

---

## ⑤ Export Reports

Generate

- CSV Report

or

- Excel Report (with student face photos)

---

# 📁 Project Structure

```
fra_system
│
├── main.py
├── login.py
├── signup.py
├── admin_dashboard.py
├── user_dashboard.py
├── register.py
├── attendance.py
├── train.py
├── db.py
├── utils.py
├── migrate.py
├── theme.py
├── requirements.txt
│
├── dataset/
├── trainer/
├── attendance/
├── attendance_photos/
│
├── fradb.sqlite
└── Attendance_Master.xlsx
```

---

# ⚙ Troubleshooting

| Issue | Solution |
|--------|----------|
| Camera not opening | Change VideoCapture(0) to 1 or 2 |
| cv2.face missing | Install opencv-contrib-python |
| Login error | Run db.py once |
| Excel missing photos | Install Pillow |
| Unknown face | Lower confidence threshold |

---

# 👨‍💻 Multi User Support

Each student has

- Unique Numeric ID
- Personal Login
- Attendance Dashboard
- Attendance Percentage

---

# 📈 Future Improvements

- 🌐 Cloud Database
- 📱 Mobile App
- ☁ Firebase Integration
- 📧 Email Notifications
- 📊 Analytics Dashboard
- 🧠 Deep Learning Face Recognition
- 🌙 Dark Mode

---

# ⭐ If you like this project

Give this repository a ⭐ on GitHub.

It motivates future development.

---

<div align="center">

Made with ❤️ using Python & OpenCV

<img src="https://capsule-render.vercel.app/api?type=waving&color=0:00C853,100:2196F3&height=120&section=footer"/>

</div>
