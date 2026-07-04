# login.py
import tkinter as tk
from tkinter import messagebox
from theme import (header_label, text_label, entry_field,
                   styled_button, BG, PRIMARY, TEXT, BTN)
from db import validate_user


class LoginWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Face Recognition Attendance — Login")
        self.root.geometry("420x480")
        self.root.configure(bg=BG)
        self.root.resizable(False, False)
        self._build()

    def _build(self):
        for w in self.root.winfo_children():
            w.destroy()

        tk.Label(self.root, text="🎓", bg=BG, font=("Arial", 40)).pack(pady=(30, 0))
        header_label(self.root, "Attendance System").pack(pady=(4, 20))

        text_label(self.root, "Username").pack()
        self.entry_user = entry_field(self.root)
        self.entry_user.pack(pady=6)

        text_label(self.root, "Password").pack()
        self.entry_pass = entry_field(self.root)
        self.entry_pass.config(show="*")
        self.entry_pass.pack(pady=6)

        styled_button(self.root, "Login", self._do_login).pack(pady=14)

        tk.Label(
            self.root, text="Don't have an account?",
            bg=BG, fg="#8b949e", font=("Arial", 10)
        ).pack()

        tk.Button(
            self.root, text="Create Account",
            bg=BG, fg=PRIMARY, bd=0, cursor="hand2",
            font=("Arial", 11, "underline"),
            command=self._go_signup
        ).pack(pady=4)

        # Keyboard shortcuts
        self.entry_user.bind("<Return>", lambda e: self.entry_pass.focus_set())
        self.entry_pass.bind("<Return>", lambda e: self._do_login())
        self.entry_user.focus_set()

    def _do_login(self):
        username = self.entry_user.get().strip()
        password = self.entry_pass.get().strip()

        if not username or not password:
            messagebox.showerror("Error", "Please enter both username and password.")
            return

        user = validate_user(username, password)
        if not user:
            messagebox.showerror("Login Failed", "Invalid username or password.")
            return

        role = user["role"]
        for w in self.root.winfo_children():
            w.destroy()

        if role == "admin":
            from admin_dashboard import AdminDashboard
            AdminDashboard(self.root)
        else:
            from user_dashboard import UserDashboard
            sid = user.get("student_id")
            UserDashboard(self.root, sid, username)

    def _go_signup(self):
        from signup import SignupWindow
        SignupWindow(self.root)
