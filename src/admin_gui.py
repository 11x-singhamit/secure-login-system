import tkinter as tk
import sqlite3


def launch_admin_gui():

    root = tk.Tk()

    root.title("Admin Dashboard")
    root.geometry("900x600")
    root.configure(bg="#0d1117")

    text = tk.Text(root,
                   bg="black",
                   fg="#00ffcc",
                   font=("Consolas", 10))

    text.pack(fill="both", expand=True)

    conn = sqlite3.connect("data/login_logs.db")
    c = conn.cursor()

    for row in c.execute("SELECT * FROM logs ORDER BY time DESC"):

        text.insert("end", str(row) + "\n")

    conn.close()

    root.mainloop()
