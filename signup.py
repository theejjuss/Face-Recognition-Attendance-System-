# signup.py
import tkinter as tk
from tkinter import messagebox
from theme import (header_label, text_label, entry_field,
                   styled_button, BG, PRIMARY, TEXT)
from db import add_user


class SignupWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Create Account")
        self.root.geometry("420x500")
        self.root.configure(bg=BG)
        self.root.resizable(False, False)
        self._build()

    def _build(self):
        for w in self.root.winfo_children():
            w.destroy()

        tk.Label(self.root, text="📝", bg=BG, font=("Arial", 36)).pack(pady=(30, 0))
        header_label(self.root, "Create Account").pack(pady=(4, 16))

        text_label(self.root, "Username").pack()
        self.entry_user = entry_field(self.root)
        self.entry_user.pack(pady=5)

        text_label(self.root, "Password").pack()
        self.entry_pass = entry_field(self.root)
        self.entry_pass.config(show="*")
        self.entry_pass.pack(pady=5)

        text_label(self.root, "Confirm Password").pack()
        self.entry_conf = entry_field(self.root)
        self.entry_conf.config(show="*")
        self.entry_conf.pack(pady=5)

        tk.Label(
            self.root,
            text="Student ID (optional — link to your face record)",
            bg=BG, fg="#8b949e", font=("Arial", 9)
        ).pack(pady=(10, 0))
        self.entry_sid = entry_field(self.root, width=12)
        self.entry_sid.pack(pady=4)

        styled_button(self.root, "Create Account", self._do_signup).pack(pady=14)

        tk.Button(
            self.root, text="Back to Login",
            bg=BG, fg=PRIMARY, bd=0, cursor="hand2",
            font=("Arial", 11, "underline"),
            command=self._go_login
        ).pack()

        self.entry_user.focus_set()
        self.entry_conf.bind("<Return>", lambda e: self._do_signup())

    def _do_signup(self):
        u = self.entry_user.get().strip()
        p = self.entry_pass.get().strip()
        c = self.entry_conf.get().strip()
        sid_raw = self.entry_sid.get().strip()

        if not u or not p:
            messagebox.showerror("Error", "Username and password are required.")
            return
        if p != c:
            messagebox.showerror("Error", "Passwords do not match.")
            return
        if len(p) < 4:
            messagebox.showerror("Error", "Password must be at least 4 characters.")
            return

        sid = None
        if sid_raw:
            try:
                sid = int(sid_raw)
            except ValueError:
                messagebox.showerror("Error", "Student ID must be a number.")
                return

        try:
            add_user(u, p, "user", sid)
            messagebox.showinfo("Success",
                                "Account created! You can now log in.")
            self._go_login()
        except Exception as e:
            messagebox.showerror("Error", f"Could not create account:\n{e}")

    def _go_login(self):
        from login import LoginWindow
        LoginWindow(self.root)
