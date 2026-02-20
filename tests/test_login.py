import sys
import os

# Fix Python import path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.auth import AuthSystem
from src.detector import AttackDetector
from src.utils import hash_password, generate_token, generate_otp
from src.security import add_user, verify_user


# =========================
# SETUP TEST USERS
# =========================

TEST_USER_FILE = "data/test_users.txt"


def setup_users_file():

    os.makedirs("data", exist_ok=True)

    with open(TEST_USER_FILE, "w") as f:

        f.write(f"admin:{hash_password('password')}\n")
        f.write(f"user1:{hash_password('123456')}\n")


# =========================
# AUTH SYSTEM TESTS
# =========================

def test_successful_login():

    setup_users_file()

    auth = AuthSystem(TEST_USER_FILE)

    result, otp = auth.login("admin", "password")

    assert result == "OTP_REQUIRED"
    assert otp is not None


def test_failed_login_wrong_password():

    setup_users_file()

    auth = AuthSystem(TEST_USER_FILE)

    result, otp = auth.login("admin", "wrongpass")

    assert result == "FAILED"
    assert otp is None


def test_login_nonexistent_user():

    setup_users_file()

    auth = AuthSystem(TEST_USER_FILE)

    result, otp = auth.login("unknown", "password")

    assert result == "FAILED"


# =========================
# OTP TESTS
# =========================

def test_otp_generation():

    otp = generate_otp()

    assert len(otp) == 6
    assert otp.isdigit()


def test_otp_verification():

    auth = AuthSystem(TEST_USER_FILE)

    result, otp = auth.login("admin", "password")

    status, token = auth.verify_otp("admin", otp)

    assert status == "SUCCESS"
    assert token is not None


def test_wrong_otp():

    auth = AuthSystem(TEST_USER_FILE)

    result, otp = auth.login("admin", "password")

    status, token = auth.verify_otp("admin", "000000")

    assert status == "FAILED"


# =========================
# TOKEN TESTS
# =========================

def test_token_generation():

    token = generate_token()

    assert len(token) >= 32
    assert isinstance(token, str)


# =========================
# ATTACK DETECTOR TESTS
# =========================

def test_bruteforce_lockout():

    detector = AttackDetector()

    for i in range(6):

        attack = detector.classify_attack(i)

    assert attack == "BRUTE FORCE ATTACK"


def test_risk_levels():

    detector = AttackDetector()

    assert detector.get_risk(0) == "LOW"
    assert detector.get_risk(2) == "MEDIUM"
    assert detector.get_risk(4) == "HIGH"
    assert detector.get_risk(6) == "CRITICAL"


# =========================
# LOCKOUT TEST
# =========================

def test_account_lockout():

    auth = AuthSystem(TEST_USER_FILE)

    for i in range(auth.max_attempts):

        auth.login("admin", "wrong")

    assert auth.is_locked() is True


# =========================
# PASSWORD HASH TEST
# =========================

def test_password_hash():

    password = "password"

    hashed = hash_password(password)

    assert hashed != password
    assert len(hashed) == 64


# =========================
# USER VERIFICATION TEST
# =========================

def test_verify_user():

    add_user("testuser", "testpass")

    assert verify_user("testuser", "testpass") is True
    assert verify_user("testuser", "wrong") is False
