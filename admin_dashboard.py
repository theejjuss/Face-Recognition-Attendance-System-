# admin_dashboard.py — Admin Dashboard
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import datetime
import threading
import os

from theme import BG, CARD, PRIMARY, TEXT, BTN, BTN_HOVER, SUBTEXT, SUCCESS, DANGER
from db import (get_today_attendance, get_all_students, delete_student,
                mark_absentees)

REFRESH_MS = 4000


class AdminDashboard:
    def __init__(self, root):
        self.root = root
        self.root.title("Admin Dashboard — Face Attendance System")
        self.root.geometry("1100x650")
        self.root.configure(bg=BG)
        self._build()
        self._update_loop()

    # ── Layout ───────────────────────────────────────────── #

    def _build(self):
        # ── Sidebar ──
        sidebar = tk.Frame(self.root, bg=CARD, width=210)
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)

        tk.Label(sidebar, text="🔐 ADMIN",
                 fg=PRIMARY, bg=CARD,
                 font=("Arial", 16, "bold")).pack(pady=(24, 4))
        tk.Label(sidebar, text="Face Attendance System",
                 fg=SUBTEXT, bg=CARD,
                 font=("Arial", 9)).pack(pady=(0, 20))

        self._sidebar_btn(sidebar, "➕  Register User",   self._open_register)
        self._sidebar_btn(sidebar, "🎯  Train Model",     self._train_model)
        self._sidebar_btn(sidebar, "📷  Start Attendance",self._start_attendance)
        self._sidebar_btn(sidebar, "📊  Mark Absentees",  self._mark_absentees)
        self._sidebar_btn(sidebar, "📁  Export Today CSV",self._export_csv)
        self._sidebar_btn(sidebar, "📋  Export Today Excel",self._export_excel)
        self._sidebar_btn(sidebar, "👥  Manage Students", self._manage_students)
        self._sidebar_btn(sidebar, "🔓  Logout",          self._logout,
                          fg=DANGER)

        # ── Main content ──
        content = tk.Frame(self.root, bg=BG)
        content.pack(side="right", expand=True, fill="both")

        # Header
        hdr = tk.Frame(content, bg=BG)
        hdr.pack(fill="x", padx=20, pady=(16, 0))

        tk.Label(hdr, text="Today's Attendance",
                 bg=BG, fg=PRIMARY,
                 font=("Arial", 20, "bold")).pack(side="left")

        self.lbl_date = tk.Label(hdr, text="", bg=BG, fg=SUBTEXT,
                                 font=("Arial", 11))
        self.lbl_date.pack(side="right")

        # Stats bar
        stats = tk.Frame(content, bg=BG)
        stats.pack(fill="x", padx=20, pady=8)

        self.lbl_present = self._stat_card(stats, "Present", "0", SUCCESS)
        self.lbl_absent  = self._stat_card(stats, "Absent",  "0", DANGER)
        self.lbl_total   = self._stat_card(stats, "Total",   "0", PRIMARY)

        # Table
        table_frame = tk.Frame(content, bg=CARD)
        table_frame.pack(padx=20, pady=4, fill="both", expand=True)

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Dark.Treeview",
                        background=CARD, foreground=TEXT,
                        fieldbackground=CARD, rowheight=32,
                        font=("Arial", 11))
        style.configure("Dark.Treeview.Heading",
                        background="#1f6feb", foreground="white",
                        font=("Arial", 11, "bold"))
        style.map("Dark.Treeview",
                  background=[("selected", BTN_HOVER)])

        self.tree = ttk.Treeview(
            table_frame,
            columns=("ID", "Name", "Time", "Status"),
            show="headings",
            style="Dark.Treeview"
        )
        for col, w in [("ID", 100), ("Name", 220), ("Time", 120), ("Status", 100)]:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=w, anchor="center")

        vsb = ttk.Scrollbar(table_frame, orient="vertical",
                            command=self.tree.yview)
        self.tree.configure(yscrollcommand=vsb.set)

        self.tree.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        vsb.pack(side="right", fill="y", pady=10)

        self.tree.tag_configure("present", foreground=SUCCESS)
        self.tree.tag_configure("absent",  foreground=DANGER)

        tk.Label(content,
                 text=f"Auto-refresh every {REFRESH_MS//1000}s",
                 bg=BG, fg=SUBTEXT,
                 font=("Arial", 9)).pack(pady=4)

    def _stat_card(self, parent, label, value, color):
        frame = tk.Frame(parent, bg=CARD, padx=16, pady=8)
        frame.pack(side="left", padx=8)
        tk.Label(frame, text=label, bg=CARD, fg=SUBTEXT,
                 font=("Arial", 9)).pack()
        lbl = tk.Label(frame, text=value, bg=CARD, fg=color,
                       font=("Arial", 20, "bold"))
        lbl.pack()
        return lbl

    def _sidebar_btn(self, parent, text, cmd, fg=TEXT):
        btn = tk.Button(parent, text=text, bg=BTN, fg=fg,
                        font=("Arial", 11), width=22, height=2,
                        bd=0, cursor="hand2", anchor="w", padx=10,
                        command=cmd)
        btn.bind("<Enter>", lambda e: btn.config(bg=BTN_HOVER))
        btn.bind("<Leave>", lambda e: btn.config(bg=BTN))
        btn.pack(pady=4, padx=10)

    # ── Data refresh ─────────────────────────────────────── #

    def _update_loop(self):
        self._refresh_table()
        self.root.after(REFRESH_MS, self._update_loop)

    def _refresh_table(self):
        today = datetime.now().strftime("%Y-%m-%d")
        self.lbl_date.config(text=today)

        for row in self.tree.get_children():
            self.tree.delete(row)

        rows = get_today_attendance(today)
        present = sum(1 for r in rows if r.get("status") == "Present")
        absent  = sum(1 for r in rows if r.get("status") == "Absent")

        for r in rows:
            tag = "present" if r.get("status") == "Present" else "absent"
            self.tree.insert("", "end",
                             values=(r["student_id"], r["name"],
                                     r["time"], r.get("status", "Present")),
                             tags=(tag,))

        total_students = len(get_all_students())
        self.lbl_present.config(text=str(present))
        self.lbl_absent.config(text=str(absent))
        self.lbl_total.config(text=str(total_students))

    # ── Actions ──────────────────────────────────────────── #

    def _open_register(self):
        win = tk.Toplevel(self.root)
        win.title("Register New Student")
        win.geometry("360x280")
        win.configure(bg=BG)
        win.grab_set()

        tk.Label(win, text="Register New Student",
                 bg=BG, fg=PRIMARY,
                 font=("Arial", 15, "bold")).pack(pady=16)

        tk.Label(win, text="Student ID (numeric)", bg=BG, fg=TEXT,
                 font=("Arial", 11)).pack()
        e_sid = tk.Entry(win, bg=CARD, fg=TEXT, font=("Arial", 11),
                         insertbackground=TEXT, width=20)
        e_sid.pack(pady=4)

        tk.Label(win, text="Full Name", bg=BG, fg=TEXT,
                 font=("Arial", 11)).pack()
        e_name = tk.Entry(win, bg=CARD, fg=TEXT, font=("Arial", 11),
                          insertbackground=TEXT, width=20)
        e_name.pack(pady=4)

        def do_register():
            sid_raw = e_sid.get().strip()
            name    = e_name.get().strip()
            if not sid_raw or not name:
                messagebox.showerror("Error", "Fill in both fields.", parent=win)
                return
            try:
                sid = int(sid_raw)
            except ValueError:
                messagebox.showerror("Error",
                                     "Student ID must be a number.", parent=win)
                return
            win.destroy()
            import register
            ok = register.register_user(sid, name)
            if ok:
                messagebox.showinfo("Done",
                                    f"Registered '{name}' (ID:{sid}).\n"
                                    "Remember to re-train the model!")

        tk.Button(win, text="Start Capture", bg=BTN_HOVER, fg="white",
                  font=("Arial", 12, "bold"), bd=0, cursor="hand2",
                  command=do_register).pack(pady=14)

        e_sid.focus_set()

    def _train_model(self):
        def run():
            import train
            ok = train.train_model()
            msg = "Model trained successfully!" if ok else \
                  "Training failed — register users first."
            fn  = messagebox.showinfo if ok else messagebox.showerror
            self.root.after(0, lambda: fn("Training", msg))

        threading.Thread(target=run, daemon=True).start()
        messagebox.showinfo("Training", "Training started in background…")

    def _start_attendance(self):
        def run():
            import attendance
            attendance.mark_attendance(
                on_exit_callback=lambda: self.root.after(0, self._refresh_table)
            )

        threading.Thread(target=run, daemon=True).start()

    def _mark_absentees(self):
        today = datetime.now().strftime("%Y-%m-%d")
        if messagebox.askyesno("Confirm",
                               f"Mark all absent students for {today}?"):
            mark_absentees(today)
            self._refresh_table()
            messagebox.showinfo("Done", "Absentees marked.")

    def _export_csv(self):
        today = datetime.now().strftime("%Y-%m-%d")
        src   = f"attendance/Attendance_{today}.csv"
        if not os.path.exists(src):
            messagebox.showerror("Error", "No CSV file for today yet.")
            return
        dst = filedialog.asksaveasfilename(
            defaultextension=".csv",
            initialfile=f"Attendance_{today}.csv",
            filetypes=[("CSV files", "*.csv")]
        )
        if dst:
            import shutil
            shutil.copy(src, dst)
            messagebox.showinfo("Success", f"CSV saved to:\n{dst}")

    def _export_excel(self):
        today = datetime.now().strftime("%Y-%m-%d")
        dst = filedialog.asksaveasfilename(
            defaultextension=".xlsx",
            initialfile=f"Attendance_{today}.xlsx",
            filetypes=[("Excel files", "*.xlsx")]
        )
        if dst:
            from utils import export_daily_excel
            export_daily_excel(today, dst)
            messagebox.showinfo("Success", f"Excel saved to:\n{dst}")

    def _manage_students(self):
        win = tk.Toplevel(self.root)
        win.title("Manage Students")
        win.geometry("500x400")
        win.configure(bg=BG)
        win.grab_set()

        tk.Label(win, text="Registered Students",
                 bg=BG, fg=PRIMARY,
                 font=("Arial", 14, "bold")).pack(pady=10)

        tree = ttk.Treeview(win, columns=("ID", "Name"),
                            show="headings", style="Dark.Treeview")
        tree.heading("ID",   text="Student ID")
        tree.heading("Name", text="Name")
        tree.column("ID",   width=120, anchor="center")
        tree.column("Name", width=240, anchor="w")
        tree.pack(fill="both", expand=True, padx=10, pady=6)

        for s in get_all_students():
            tree.insert("", "end",
                        values=(s["student_id"], s["name"]))

        def do_delete():
            sel = tree.selection()
            if not sel:
                return
            item = tree.item(sel[0])["values"]
            sid, name = item[0], item[1]
            if messagebox.askyesno(
                    "Confirm Delete",
                    f"Delete '{name}' (ID:{sid}) and all their attendance?",
                    parent=win):
                delete_student(sid)
                tree.delete(sel[0])
                messagebox.showinfo("Deleted",
                                    f"'{name}' removed.", parent=win)

        tk.Button(win, text="🗑  Delete Selected",
                  bg="#6e1717", fg=TEXT,
                  font=("Arial", 11, "bold"), bd=0, cursor="hand2",
                  command=do_delete).pack(pady=8)

    def _logout(self):
        for w in self.root.winfo_children():
            w.destroy()
        from login import LoginWindow
        LoginWindow(self.root)
