import hashlib
from database import connect
from datetime import datetime

LOG_FILE = "security.log"
MAX_ATTEMPTS = 3


def log_event(event):
    with open(LOG_FILE, "a") as f:
        f.write(f"{datetime.now()} {event}\n")


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


def register_user(username, password):
    conn = connect()
    cursor = conn.cursor()

    password_hash = hash_password(password)

    try:
        cursor.execute(
            "INSERT INTO users (username, password_hash) VALUES (?, ?)",
            (username, password_hash)
        )
        conn.commit()
        log_event(f"REGISTER_SUCCESS user={username}")
        print("User registered successfully.")
    except:
        print("Username already exists.")

    conn.close()


def login_user(username, password):
    conn = connect()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT password_hash, failed_attempts, locked FROM users WHERE username=?",
        (username,)
    )

    result = cursor.fetchone()

    if not result:
        print("User not found.")
        return False

    stored_hash, failed_attempts, locked = result

    if locked:
        print("Account is locked.")
        log_event(f"LOGIN_BLOCKED user={username}")
        return False

    if hash_password(password) == stored_hash:
        cursor.execute(
            "UPDATE users SET failed_attempts=0 WHERE username=?",
            (username,)
        )
        conn.commit()
        log_event(f"LOGIN_SUCCESS user={username}")
        print("Login successful!")
        return True

    else:
        failed_attempts += 1

        if failed_attempts >= MAX_ATTEMPTS:
            cursor.execute(
                "UPDATE users SET failed_attempts=?, locked=1 WHERE username=?",
                (failed_attempts, username)
            )
            log_event(f"ACCOUNT_LOCKED user={username}")
            print("Account locked due to too many failed attempts.")
        else:
            cursor.execute(
                "UPDATE users SET failed_attempts=? WHERE username=?",
                (failed_attempts, username)
            )
            log_event(f"LOGIN_FAILED user={username}")

        conn.commit()
        return False
