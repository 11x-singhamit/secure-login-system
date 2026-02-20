from src.utils import generate_otp

class OTPManager:

    def __init__(self):
        self.current_otp = None

    def create_otp(self):

        self.current_otp = generate_otp()

        print(f"[SYSTEM] OTP: {self.current_otp}")  # simulate sending

        return self.current_otp

    def verify_otp(self, otp):

        return otp == self.current_otp
