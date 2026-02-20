import tkinter as tk
from tkinter import messagebox
import time
import sqlite3

from src.auth import AuthSystem
from src.detector import AttackDetector
from src.security import add_user


auth = AuthSystem()
detector = AttackDetector()


# =========================
# LAUNCH GUI
# =========================

def launch_gui():

    root = tk.Tk()

    root.title("Secure Login System – Security Console")
    root.geometry("1000x650")
    root.configure(bg="#d9d9d9")

    app = SecurityConsole(root)

    root.mainloop()


# =========================
# MAIN CLASS
# =========================

class SecurityConsole:

    def __init__(self, root):

        self.root = root

        # NEW: Initialize database
        self.init_database()

        self.build_layout()

        self.update_clock()


# =========================
# DATABASE INITIALIZATION
# =========================

    def init_database(self):

        try:

            conn = sqlite3.connect("data/login_logs.db")

            conn.execute("""
            CREATE TABLE IF NOT EXISTS logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                message TEXT,
                time TEXT
            )
            """)

            conn.commit()
            conn.close()

        except Exception as e:

            print("Database init error:", e)


# =========================
# BUILD GUI
# =========================

    def build_layout(self):

        header = tk.Label(
            self.root,
            text="Secure Login System – Attack Detection Console",
            font=("Segoe UI", 16, "bold"),
            bg="#2c3e50",
            fg="white",
            pady=10
        )

        header.pack(fill="x")

        main = tk.Frame(self.root, bg="#d9d9d9")
        main.pack(pady=10)


        # AUTH FRAME
        auth_frame = tk.LabelFrame(
            main,
            text="User Authentication",
            padx=20,
            pady=20
        )

        auth_frame.grid(row=0, column=0, padx=20)

        tk.Label(auth_frame, text="Username").grid(row=0, column=0)

        self.username = tk.Entry(auth_frame, width=20)
        self.username.grid(row=0, column=1)

        tk.Label(auth_frame, text="Password").grid(row=1, column=0)

        self.password = tk.Entry(auth_frame, show="*", width=20)
        self.password.grid(row=1, column=1)


        self.auth_button = tk.Button(
            auth_frame,
            text="Authenticate",
            width=15,
            command=self.authenticate
        )

        self.auth_button.grid(row=2, column=0, columnspan=2, pady=5)


        tk.Button(
            auth_frame,
            text="Register User",
            width=15,
            command=self.register_user
        ).grid(row=3, column=0, columnspan=2, pady=5)


        self.auth_retry_label = tk.Label(
            auth_frame,
            text="",
            fg="red",
            font=("Segoe UI", 9, "bold")
        )

        self.auth_retry_label.grid(row=4, column=0, columnspan=2, pady=5)


        # STATUS FRAME
        status_frame = tk.LabelFrame(
            main,
            text="Security Status",
            padx=20,
            pady=20
        )

        status_frame.grid(row=0, column=1)

        self.system_status = tk.Label(
            status_frame,
            text="System Status: Idle",
            fg="green"
        )
        self.system_status.pack(anchor="w")

        self.lock_status = tk.Label(
            status_frame,
            text="Account Lockout: None"
        )
        self.lock_status.pack(anchor="w")

        self.timer_status = tk.Label(
            status_frame,
            text="Retry available in: -"
        )
        self.timer_status.pack(anchor="w")

        self.risk_status = tk.Label(
            status_frame,
            text="Risk Level: LOW",
            fg="green"
        )
        self.risk_status.pack(anchor="w")

        self.attack_type_status = tk.Label(
            status_frame,
            text="Attack Type: None",
            fg="green"
        )
        self.attack_type_status.pack(anchor="w")

        self.token_status = tk.Label(
            status_frame,
            text="Session Token: None"
        )
        self.token_status.pack(anchor="w")


        # LOG FRAME
        log_frame = tk.LabelFrame(
            self.root,
            text="Security Audit Logs",
            padx=10,
            pady=10
        )

        log_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.log_box = tk.Text(
            log_frame,
            height=20,
            bg="white"
        )

        self.log_box.pack(fill="both", expand=True)


        tk.Button(
            self.root,
            text="Open Admin Dashboard",
            bg="#34495e",
            fg="white",
            command=self.open_admin
        ).pack(pady=5)


# =========================
# AUTHENTICATION
# =========================

    def authenticate(self):

        username = self.username.get()
        password = self.password.get()

        result, otp = auth.login(username, password)

        failed_attempts = auth.failed_attempts

        risk = detector.get_risk(failed_attempts)
        attack_type = detector.classify_attack(failed_attempts)

        self.risk_status.config(
            text=f"Risk Level: {risk}",
            fg="red" if risk in ["HIGH", "CRITICAL"] else "green"
        )

        self.attack_type_status.config(
            text=f"Attack Type: {attack_type}",
            fg="red" if attack_type != "NORMAL ACTIVITY" else "green"
        )

        self.log(f"{username} login attempt detected")

        if result == "OTP_REQUIRED":

            self.system_status.config(
                text="System Status: OTP Sent",
                fg="orange"
            )

            self.show_otp_popup(otp)

            self.verify_otp(username)

        elif result == "LOCKED":

            self.system_status.config(
                text="System Status: LOCKED",
                fg="red"
            )

            self.lock_status.config(
                text="Account Lockout: ACTIVE"
            )

            self.update_lock_timer()

            self.log(f"ATTACK DETECTED: {attack_type}")

        else:

            self.system_status.config(
                text="System Status: Access Denied",
                fg="red"
            )


# =========================
# UPDATED LOG FUNCTION
# =========================

    def log(self, message):

        now = time.strftime("%Y-%m-%d %H:%M:%S")

        log_entry = f"[{now}] {message}\n"

        self.log_box.insert("end", log_entry)
        self.log_box.see("end")

        # Save to database
        try:

            conn = sqlite3.connect("data/login_logs.db")

            conn.execute(
                "INSERT INTO logs (message, time) VALUES (?, ?)",
                (message, now)
            )

            conn.commit()
            conn.close()

        except Exception as e:

            print("Database log error:", e)


        # Save to text file
        try:

            with open("data/login_logs.txt", "a") as f:

                f.write(log_entry)

        except Exception as e:

            print("File log error:", e)


# =========================
# REMAINING FUNCTIONS UNCHANGED
# =========================

    def update_lock_timer(self):
        remaining = auth.remaining_lock_time()
        self.timer_status.config(text=f"Retry available in: {remaining}s")
        self.auth_retry_label.config(text=f"Login disabled. Retry in {remaining} seconds")
        self.auth_button.config(state="disabled")

        if remaining > 0:
            self.root.after(1000, self.update_lock_timer)
        else:
            self.lock_status.config(text="Account Lockout: None")
            self.timer_status.config(text="Retry available in: -")
            self.auth_retry_label.config(text="")
            self.auth_button.config(state="normal")
            self.system_status.config(text="System Status: Idle", fg="green")


    def show_otp_popup(self, otp):

        popup = tk.Toplevel(self.root)
        popup.title("OTP Notification")
        popup.geometry("300x150")

        tk.Label(popup, text="Security Verification", font=("Segoe UI", 12, "bold")).pack(pady=10)

        tk.Label(
            popup,
            text=f"Your OTP is:\n{otp}",
            font=("Segoe UI", 14),
            fg="blue"
        ).pack(pady=10)

        tk.Button(popup, text="OK", command=popup.destroy).pack()


    def verify_otp(self, username):

        win = tk.Toplevel(self.root)

        tk.Label(win, text="Enter OTP").pack()

        otp_entry = tk.Entry(win)
        otp_entry.pack()

        def verify():

            result, token = auth.verify_otp(username, otp_entry.get())

            if result == "SUCCESS":

                self.system_status.config(text="System Status: Access Granted", fg="green")

                self.token_status.config(text=f"Session Token: {token}")

                self.log(f"{username} logged in successfully")

                win.destroy()

            else:

                messagebox.showerror("Error", "Invalid OTP")

        tk.Button(win, text="Verify", command=verify).pack()


    def register_user(self):

        win = tk.Toplevel(self.root)

        tk.Label(win, text="Username").pack()
        user = tk.Entry(win)
        user.pack()

        tk.Label(win, text="Password").pack()
        pwd = tk.Entry(win)
        pwd.pack()

        def save():

            add_user(user.get(), pwd.get())

            self.log(f"New user registered: {user.get()}")

            win.destroy()

        tk.Button(win, text="Register", command=save).pack()


    def open_admin(self):

        win = tk.Toplevel(self.root)

        text = tk.Text(win)
        text.pack(fill="both", expand=True)

        conn = sqlite3.connect("data/login_logs.db")

        for row in conn.execute("SELECT * FROM logs ORDER BY id DESC"):
            text.insert("end", str(row) + "\n")

        conn.close()


    def update_clock(self):

        now = time.strftime("%H:%M:%S")

        self.root.title(f"Secure Login System – Security Console ({now})")

        self.root.after(1000, self.update_clock)