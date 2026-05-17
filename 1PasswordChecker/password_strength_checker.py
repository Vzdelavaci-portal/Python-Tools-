import string
import tkinter as tk
from tkinter import ttk


def check_password_strength(password):
    score = 0

    if len(password) >= 8:
        score += 1
    if any(char.isupper() for char in password):
        score += 1
    if any(char.islower() for char in password):
        score += 1
    if any(char.isdigit() for char in password):
        score += 1
    if any(char in string.punctuation for char in password):
        score += 1

    return score


def update_strength(event=None):
    password = password_entry.get()
    score = check_password_strength(password)

    if not password:
        result_label.config(text="Enter a password", fg="#ffffff")
        progress_bar.config(bg="#333333", width=1)
        return

    if score <= 2:
        result_label.config(text="WEAK ❌", fg="#ff4d4d")
        progress_bar.config(bg="#ff4d4d", width=120)

    elif score <= 4:
        result_label.config(text="MEDIUM ⚠️", fg="#ffaa00")
        progress_bar.config(bg="#ffaa00", width=260)

    else:
        result_label.config(text="STRONG ✅", fg="#00cc66")
        progress_bar.config(bg="#00cc66", width=420)


root = tk.Tk()
root.title("Password Strength Checker")
root.geometry("540x960")
root.resizable(False, False)
root.configure(bg="#121212")

title_label = tk.Label(
    root,
    text="PASSWORD\nSTRENGTH\nCHECKER",
    font=("Arial", 34, "bold"),
    fg="#ffffff",
    bg="#121212",
    justify="center"
)
title_label.pack(pady=70)

subtitle_label = tk.Label(
    root,
    text="Type a password and check its strength",
    font=("Arial", 16),
    fg="#bbbbbb",
    bg="#121212"
)
subtitle_label.pack(pady=10)

password_entry = tk.Entry(
    root,
    width=22,
    font=("Arial", 24),
    justify="center",
    bg="#1f1f1f",
    fg="#ffffff",
    insertbackground="#ffffff",
    relief="flat"
)
password_entry.pack(pady=40, ipady=15)

password_entry.bind("<KeyRelease>", update_strength)

progress_container = tk.Frame(
    root,
    width=420,
    height=28,
    bg="#333333"
)
progress_container.pack(pady=30)
progress_container.pack_propagate(False)

progress_bar = tk.Frame(
    progress_container,
    width=1,
    height=28,
    bg="#333333"
)
progress_bar.pack(side="left")

result_label = tk.Label(
    root,
    text="Enter a password",
    font=("Arial", 32, "bold"),
    fg="#ffffff",
    bg="#121212"
)
result_label.pack(pady=40)

info_label = tk.Label(
    root,
    text="Checks length, numbers,\nuppercase letters and symbols",
    font=("Arial", 16),
    fg="#aaaaaa",
    bg="#121212",
    justify="center"
)
info_label.pack(pady=30)

footer_label = tk.Label(
    root,
    text="Python Mini Automation",
    font=("Arial", 14, "bold"),
    fg="#00ccff",
    bg="#121212"
)
footer_label.pack(side="bottom", pady=40)

root.mainloop()