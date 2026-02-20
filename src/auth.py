import time
from src.utils import hash_password, generate_token, generate_otp


class AuthSystem:

    def __init__(self, user_file="data/users.txt"):
        

        self.user_file = user_file

        self.failed_attempts = 0
        self.max_attempts = 5

        self.locked_until = 0

        self.current_otp = None


# =========================
# LOAD USERS
# =========================

    def load_users(self):

        users = {}

        try:
            with open(self.user_file, "r") as f:

                for line in f:

                    username, password = line.strip().split(":")

                    users[username] = password

        except FileNotFoundError:
            pass

        return users


# =========================
# CHECK LOCK STATUS
# =========================

    def is_locked(self):

        return time.time() < self.locked_until


    def remaining_lock_time(self):

        return max(0, int(self.locked_until - time.time()))


# =========================
# LOGIN
# =========================

    def login(self, username, password):

        if self.is_locked():

            return "LOCKED", None


        users = self.load_users()

        if username not in users:

            self.failed_attempts += 1
            return "FAILED", None


        if users[username] == hash_password(password):

            self.failed_attempts = 0

            self.current_otp = generate_otp()

            return "OTP_REQUIRED", self.current_otp

        else:

            self.failed_attempts += 1

            if self.failed_attempts >= self.max_attempts:

                self.locked_until = time.time() + 120

                return "LOCKED", None

            return "FAILED", None


# =========================
# VERIFY OTP
# =========================

    def verify_otp(self, username, otp):

        if otp == self.current_otp:

            token = generate_token()

            return "SUCCESS", token

        return "FAILED", None
