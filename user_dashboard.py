# user_dashboard.py — Student self-service dashboard
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import datetime
import os

from theme import BG, CARD, PRIMARY, TEXT, BTN, BTN_HOVER, SUBTEXT, SUCCESS, DANGER
from db import get_user_attendance, get_student_name


class UserDashboard:
    def __init__(self, root, student_id, username):
        self.root       = root
        self.student_id = student_id
        self.username   = username
        self.root.title(f"Student Portal — {username}")
        self.root.geometry("750x560")
        self.root.configure(bg=BG)
        self._build()
        self._refresh()

    def _build(self):
        for w in self.root.winfo_children():
            w.destroy()

        # Header
        hdr = tk.Frame(self.root, bg=CARD)
        hdr.pack(fill="x")
        tk.Label(hdr, text=f"👤  {self.username}",
                 bg=CARD, fg=PRIMARY,
                 font=("Arial", 16, "bold")).pack(side="left", padx=16, pady=10)

        if self.student_id:
            sname = get_student_name(self.student_id) or ""
            tk.Label(hdr, text=f"ID: {self.student_id}  |  {sname}",
                     bg=CARD, fg=SUBTEXT,
                     font=("Arial", 10)).pack(side="left", padx=8)

        tk.Button(hdr, text="Logout",
                  bg=BTN, fg=TEXT, bd=0, cursor="hand2",
                  font=("Arial", 10),
                  command=self._logout).pack(side="right", padx=12, pady=8)

        # Stats row
        stats = tk.Frame(self.root, bg=BG)
        stats.pack(fill="x", padx=16, pady=10)

        self.lbl_present = self._stat_card(stats, "Present Days", "—", SUCCESS)
        self.lbl_absent  = self._stat_card(stats, "Absent Days",  "—", DANGER)
        self.lbl_pct     = self._stat_card(stats, "Attendance %", "—", PRIMARY)

        # Table
        tk.Label(self.root, text="Attendance Record",
                 bg=BG, fg=PRIMARY,
                 font=("Arial", 14, "bold")).pack(anchor="w", padx=16, pady=(4, 0))

        table_frame = tk.Frame(self.root, bg=CARD)
        table_frame.pack(padx=16, pady=6, fill="both", expand=True)

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("User.Treeview",
                        background=CARD, foreground=TEXT,
                        fieldbackground=CARD, rowheight=30,
                        font=("Arial", 11))
        style.configure("User.Treeview.Heading",
                        background="#1f6feb", foreground="white",
                        font=("Arial", 11, "bold"))
        style.map("User.Treeview",
                  background=[("selected", BTN_HOVER)])

        self.tree = ttk.Treeview(
            table_frame,
            columns=("Date", "Time", "Status"),
            show="headings",
            style="User.Treeview"
        )
        self.tree.heading("Date",   text="Date")
        self.tree.heading("Time",   text="Time")
        self.tree.heading("Status", text="Status")
        self.tree.column("Date",   width=180, anchor="center")
        self.tree.column("Time",   width=150, anchor="center")
        self.tree.column("Status", width=120, anchor="center")

        vsb = ttk.Scrollbar(table_frame, orient="vertical",
                            command=self.tree.yview)
        self.tree.configure(yscrollcommand=vsb.set)
        self.tree.pack(side="left", fill="both", expand=True, padx=8, pady=8)
        vsb.pack(side="right", fill="y", pady=8)

        self.tree.tag_configure("present", foreground=SUCCESS)
        self.tree.tag_configure("absent",  foreground=DANGER)

        # Buttons
        btn_row = tk.Frame(self.root, bg=BG)
        btn_row.pack(pady=8)

        self._btn(btn_row, "⬇  Download CSV", self._download_csv)
        self._btn(btn_row, "🔄  Refresh",      self._refresh)

        if not self.student_id:
            tk.Label(self.root,
                     text="⚠ No student ID linked — contact admin to link your face record.",
                     bg=BG, fg=DANGER,
                     font=("Arial", 9)).pack(pady=4)

    def _stat_card(self, parent, label, value, color):
        frame = tk.Frame(parent, bg=CARD, padx=20, pady=10)
        frame.pack(side="left", padx=10)
        tk.Label(frame, text=label, bg=CARD, fg=SUBTEXT,
                 font=("Arial", 9)).pack()
        lbl = tk.Label(frame, text=value, bg=CARD, fg=color,
                       font=("Arial", 22, "bold"))
        lbl.pack()
        return lbl

    def _btn(self, parent, text, cmd):
        btn = tk.Button(parent, text=text, bg=BTN, fg=TEXT,
                        font=("Arial", 11, "bold"), width=20, height=2,
                        bd=0, cursor="hand2", command=cmd)
        btn.bind("<Enter>", lambda e: btn.config(bg=BTN_HOVER))
        btn.bind("<Leave>", lambda e: btn.config(bg=BTN))
        btn.pack(side="left", padx=10)

    def _refresh(self):
        for i in self.tree.get_children():
            self.tree.delete(i)

        if not self.student_id:
            return

        rows = get_user_attendance(self.student_id)
        present = sum(1 for r in rows if r.get("status") == "Present")
        absent  = sum(1 for r in rows if r.get("status") == "Absent")
        total   = present + absent
        pct     = f"{(present/total*100):.1f}%" if total else "—"

        self.lbl_present.config(text=str(present))
        self.lbl_absent.config(text=str(absent))
        self.lbl_pct.config(text=pct)

        for r in rows:
            tag = "present" if r.get("status") == "Present" else "absent"
            self.tree.insert("", "end",
                             values=(r["date"], r["time"], r.get("status", "Present")),
                             tags=(tag,))

    def _download_csv(self):
        if not self.student_id:
            messagebox.showerror("Error", "No student ID linked to your account.")
            return

        rows = get_user_attendance(self.student_id)
        if not rows:
            messagebox.showinfo("No Data", "No attendance records found.")
            return

        import pandas as pd
        df = pd.DataFrame(rows)

        path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            initialfile=f"{self.username}_attendance.csv",
            filetypes=[("CSV files", "*.csv")]
        )
        if path:
            df.to_csv(path, index=False)
            messagebox.showinfo("Saved", f"File saved:\n{path}")

    def _logout(self):
        for w in self.root.winfo_children():
            w.destroy()
        from login import LoginWindow
        LoginWindow(self.root)
