import sqlite3
from src.utils import hash_password, get_time, get_ip

USER_DB = "data/users.db"
LOG_DB = "data/login_logs.db"


def init_databases():

    conn = sqlite3.connect(USER_DB)
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS users(
        username TEXT PRIMARY KEY,
        password TEXT,
        role TEXT
    )
    """)

    conn.commit()
    conn.close()

    conn = sqlite3.connect(LOG_DB)
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS logs(
        time TEXT,
        username TEXT,
        ip TEXT,
        status TEXT,
        event TEXT
    )
    """)

    conn.commit()
    conn.close()


def add_user(username, password, role="user"):

    conn = sqlite3.connect(USER_DB)
    c = conn.cursor()

    c.execute(
        "INSERT OR REPLACE INTO users VALUES(?,?,?)",
        (username, hash_password(password), role)
    )

    conn.commit()
    conn.close()


def verify_user(username, password):

    conn = sqlite3.connect(USER_DB)
    c = conn.cursor()

    c.execute("SELECT password FROM users WHERE username=?",
              (username,))

    result = c.fetchone()

    conn.close()

    if result:
        return hash_password(password) == result[0]

    return False


def log_event(username, status, event):

    conn = sqlite3.connect(LOG_DB)
    c = conn.cursor()

    c.execute(
        "INSERT INTO logs VALUES(?,?,?,?,?)",
        (get_time(), username, get_ip(), status, event)
    )

    conn.commit()
    conn.close()
