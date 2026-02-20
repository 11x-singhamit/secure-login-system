import hashlib
import secrets
import socket
from datetime import datetime


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


def generate_token():
    return secrets.token_hex(32)


def generate_otp():
    return str(secrets.randbelow(900000) + 100000)


def get_ip():
    return socket.gethostbyname(socket.gethostname())


def get_time():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
