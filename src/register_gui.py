import tkinter as tk
from src.security import add_user


def launch_register_gui():

    root = tk.Tk()

    root.title("User Registration")

    username = tk.Entry(root)
    username.pack()

    password = tk.Entry(root, show="*")
    password.pack()

    def register():

        add_user(username.get(), password.get())

        print("User registered")

    tk.Button(root, text="Register", command=register).pack()

    root.mainloop()
