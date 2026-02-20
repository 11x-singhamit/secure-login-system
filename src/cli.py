import time
from getpass import getpass

from src.auth import AuthSystem
from src.detector import AttackDetector


# Create same objects as GUI
auth = AuthSystem()
detector = AttackDetector()


# =========================
# CLI LOGIN SYSTEM
# =========================

def run_cli():

    print("\n=======================================================")
    print(" Secure Login System – Attack Detection Console (CLI)")
    print("=======================================================\n")

    while True:

        print("\n--- User Authentication ---")

        username = input("Username: ").strip()

        password = getpass("Password: ")

        print("\nAuthenticating", end="")

        for _ in range(3):
            time.sleep(0.4)
            print(".", end="", flush=True)

        print("\n")


        # Call auth system
        result, otp = auth.login(username, password)

        failed_attempts = auth.failed_attempts

        risk = detector.get_risk(failed_attempts)

        attack_type = detector.classify_attack(failed_attempts)


        print("Security Status:")
        print(f"• Risk Level : {risk}")
        print(f"• Attack Type: {attack_type}")


        # =========================
        # OTP REQUIRED
        # =========================

        if result == "OTP_REQUIRED":

            print("\n[INFO] OTP sent to user")

            print(f"[DEBUG] Your OTP is: {otp}")

            user_otp = input("Enter OTP: ")

            print("\nVerifying OTP", end="")

            for _ in range(3):
                time.sleep(0.4)
                print(".", end="", flush=True)

            print("\n")

            status, token = auth.verify_otp(username, user_otp)

            if status == "SUCCESS":

                print("[SUCCESS] Access Granted")
                print(f"Session Token: {token}")

                print("\nSystem Status: AUTHENTICATED")
                print("Account Lockout: None")
                print("Risk Level: LOW")

                break

            else:

                print("[ERROR] Invalid OTP")
                print("System Status: Access Denied")


        # =========================
        # ACCOUNT LOCKED
        # =========================

        elif result == "LOCKED":

            print("\n[SECURITY ALERT]")
            print("System Status : LOCKED")
            print("Account Lockout: ACTIVE")

            remaining = auth.remaining_lock_time()

            while remaining > 0:

                print(f"\rRetry available in: {remaining}s", end="")

                time.sleep(1)

                remaining = auth.remaining_lock_time()

            print("\nAccount unlocked. Try again.")


        # =========================
        # LOGIN FAILED
        # =========================

        else:

            remaining = auth.max_attempts - auth.failed_attempts

            print("[ERROR] Access Denied")

            print(f"Attempts used     : {auth.failed_attempts}")
            print(f"Attempts remaining: {remaining}")

            if risk in ["HIGH", "CRITICAL"]:

                print("\n[WARNING] Suspicious activity detected")


        print("\n---------------------------------------------------")
