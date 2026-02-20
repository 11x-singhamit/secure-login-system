# Secure Login System with Attack Detection

## Overview

The Secure Login System with Attack Detection is a cybersecurity-focused authentication application developed using Python. The system protects user accounts by implementing secure password hashing, One-Time Password (OTP) verification, attack detection, account lockout protection, and session token generation.

The system provides both a Graphical User Interface (GUI) and a Command Line Interface (CLI), allowing users and administrators to interact with the system easily. All login activities are recorded in a database and log file for monitoring, analysis, and security auditing.

This project demonstrates secure authentication techniques and attack prevention mechanisms used in modern cybersecurity systems.

---

## Key Features

* Secure password hashing using SHA-256
* One-Time Password (OTP) authentication
* Brute-force attack detection
* Automatic account lockout protection
* Session token generation for secure sessions
* Security audit logging (Database and Log File)
* Graphical User Interface (GUI)
* Command Line Interface (CLI)
* Admin dashboard to monitor login activity
* Unit testing using pytest

---

## Technologies Used

Programming Language:

* Python 3

Libraries:

* Tkinter – Graphical User Interface
* SQLite3 – Database storage
* hashlib – Password hashing
* getpass – Secure password input in CLI
* pytest – Unit testing framework
* time – Lockout timer and logging timestamps

---

## Project Structure

```
secure-login-system/
│
├── src/
│   ├── auth.py
│   ├── gui.py
│   ├── cli.py
│   ├── detector.py
│   ├── security.py
│   └── utils.py
│
├── data/
│   ├── users.txt
│   ├── login_logs.db
│   └── login_logs.txt
│
├── tests/
│   └── test_login.py
│
├── main.py
└── README.md
```

---

## How to Run the Project

Step 1: Open terminal and navigate to project folder

```
cd secure-login-system
```

Step 2: Run the system

```
python3 main.py
```

Step 3: Choose an option

```
1. Launch GUI Login
2. Launch CLI Login
3. Launch Admin Dashboard
4. Exit
```

---

## How to Run Unit Tests

Run the following command:

```
pytest -v
```

This will test authentication, OTP verification, attack detection, and system security features.

---

## Security Features

This system provides protection against:

* Brute-force attacks
* Unauthorized login attempts
* Replay attacks
* Password theft
* Session hijacking

Security mechanisms implemented:

* Password hashing
* OTP authentication
* Session token generation
* Account lockout timer
* Attack detection system
* Database logging

---

## Database and Log Storage

Login records are stored in:

Database file:

```
data/login_logs.db
```

Log file:

```
data/login_logs.txt
```

These logs help administrators monitor system activity and detect security threats.

---

## Educational Purpose

This project was developed for educational purposes as part of the Programming and Algorithm 2 module in Ethical Hacking and Cyber Security. It demonstrates secure authentication, attack detection, and secure system design using Python.

---

## Author

Amit Singh  
Ethical Hacking and Cyber Security Student 

---
## License

This project is for educational purposes only.