# theme.py — Shared UI styling constants
import tkinter as tk

# ── Colour palette ─────────────────────────────────── #
BG        = "#0d1117"
CARD      = "#161b22"
PRIMARY   = "#58a6ff"
TEXT      = "#c9d1d9"
SUBTEXT   = "#8b949e"
BTN       = "#21262d"
BTN_HOVER = "#1f6feb"
SUCCESS   = "#3fb950"
DANGER    = "#f85149"
WARNING   = "#d29922"

# ── Font helpers ───────────────────────────────────── #
FONT_TITLE  = ("Arial", 22, "bold")
FONT_HEAD   = ("Arial", 14, "bold")
FONT_BODY   = ("Arial", 11)
FONT_SMALL  = ("Arial", 9)


# ── Widget factories ───────────────────────────────── #

def header_label(parent, text, fg=PRIMARY):
    return tk.Label(parent, text=text, bg=BG, fg=fg, font=FONT_TITLE)


def text_label(parent, text, fg=TEXT):
    return tk.Label(parent, text=text, bg=BG, fg=fg, font=FONT_BODY)


def entry_field(parent, width=28):
    e = tk.Entry(parent, bg=CARD, fg=TEXT, insertbackground=TEXT,
                 font=FONT_BODY, width=width, bd=1, relief="flat",
                 highlightthickness=1, highlightcolor=PRIMARY,
                 highlightbackground=BTN)
    return e


def styled_button(parent, text, cmd, bg=BTN, fg=TEXT, width=20):
    btn = tk.Button(
        parent, text=text, command=cmd,
        bg=bg, fg=fg, font=FONT_HEAD,
        width=width, height=2, bd=0, cursor="hand2",
        activebackground=BTN_HOVER, activeforeground="white"
    )
    btn.bind("<Enter>", lambda e: btn.config(bg=BTN_HOVER))
    btn.bind("<Leave>", lambda e: btn.config(bg=bg))
    return btn


def danger_button(parent, text, cmd, width=20):
    return styled_button(parent, text, cmd, bg="#6e1717", fg=TEXT, width=width)
