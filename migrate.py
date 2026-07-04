# migrate.py — Import old CSV attendance files into the DB
import os
import pandas as pd
from db import init_db, ensure_admin, add_student, log_attendance


def migrate_attendance_csv():
    init_db()
    ensure_admin()
    att_folder = "attendance"

    if not os.path.isdir(att_folder):
        print("No attendance folder found.")
        return

    for fname in os.listdir(att_folder):
        if fname.startswith("Attendance_") and fname.endswith(".csv"):
            path = os.path.join(att_folder, fname)
            df   = pd.read_csv(path)

            # Infer date from filename: Attendance_YYYY-MM-DD.csv
            date_str = fname.replace("Attendance_", "").replace(".csv", "")

            for _, row in df.iterrows():
                # Support both 'ID' and 'Student ID' column names
                sid_val = row.get("Student ID", row.get("ID"))
                try:
                    sid = int(sid_val)
                except (ValueError, TypeError):
                    continue

                name     = str(row.get("Name", "Unknown"))
                time_str = str(row.get("Time", "00:00:00"))
                status   = str(row.get("Status", "Present"))

                add_student(sid, name)
                log_attendance(sid, name, date_str, time_str, status)

            print(f"Migrated: {fname}")


if __name__ == "__main__":
    migrate_attendance_csv()
    print("Migration finished.")
