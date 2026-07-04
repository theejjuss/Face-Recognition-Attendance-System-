# main.py — Entry point
import tkinter as tk
from db import init_db
from login import LoginWindow

# Ensure database and default admin exist
init_db()

root = tk.Tk()
LoginWindow(root)
root.mainloop()
