# Face Recognition Attendance System
## Setup & Usage Guide

---

### 1. Install dependencies
```bash
pip install -r requirements.txt
```
> **Important:** You need `opencv-contrib-python` (not just `opencv-python`) for the LBPH face recognizer.

---

### 2. Run the application
```bash
python main.py
```

---

### 3. Default admin credentials
| Username | Password  |
|----------|-----------|
| admin    | admin123  |

Change the password after first login by editing `db.py → ensure_admin()`.

---

### 4. Workflow

#### Step 1 — Register students (Admin)
1. Login as **admin**
2. Click **Register User**
3. Enter numeric Student ID and full name
4. Look at the camera — 60 face samples are captured automatically

#### Step 2 — Train the model (Admin)
1. Click **Train Model** (takes a few seconds)
2. Do this again whenever new students are registered

#### Step 3 — Take attendance
1. Click **Start Attendance**
2. The webcam window opens — students look at the camera
3. Recognised faces are marked **Present** automatically
4. Press **ESC** or close the window to stop

#### Step 4 — Mark absentees (optional, end of day)
- Click **Mark Absentees** — any registered student with no entry today gets marked **Absent**

#### Step 5 — Export records
- **Export Today CSV** → saves daily CSV
- **Export Today Excel** → saves Excel with embedded face photos

---

### 5. File structure
```
fra_system/
├── main.py               ← entry point
├── db.py                 ← SQLite database layer
├── theme.py              ← UI colour/font constants
├── login.py              ← Login window
├── signup.py             ← Account creation
├── admin_dashboard.py    ← Admin UI
├── user_dashboard.py     ← Student UI
├── register.py           ← Face capture
├── train.py              ← Model training
├── attendance.py         ← Live recognition + marking
├── utils.py              ← Excel/CSV helpers
├── migrate.py            ← Import old CSV files
├── requirements.txt
│
├── fradb.sqlite          ← auto-created
├── dataset/              ← face sample images (auto-created)
├── trainer/              ← trainer.yml model file (auto-created)
├── attendance/           ← daily CSV files (auto-created)
├── attendance_photos/    ← face crops at recognition time (auto-created)
└── Attendance_Master.xlsx← running Excel log (auto-created)
```

---

### 6. Troubleshooting

| Problem | Fix |
|---------|-----|
| Camera not opening | Change `cv2.VideoCapture(0)` to `1` or `2` in attendance.py |
| `cv2.face` not found | Run `pip install opencv-contrib-python` |
| Login fails | Make sure `fradb.sqlite` exists (run `python db.py` once) |
| Photos not in Excel | Install Pillow: `pip install Pillow` |
| Unknown face always | Lower `CONFIDENCE_THRESHOLD` in attendance.py (try 80) |

---

### 7. Multi-user support
- Each student gets a **numeric ID** (e.g. 101, 102, 103)
- Students create an account in the app, entering their numeric ID to link their login to their face record
- The **User Dashboard** shows only that student's own attendance history and percentage
