# Project 4: Secure Authentication API with JWT & Password Hashing

A production-grade security micro-project demonstrating **user registration**, **cryptographic password hashing (PBKDF2-HMAC-SHA256)**, **JSON Web Token (JWT) generation**, and **protected route access control**.

---

## 📌 Project Overview

This project implements industry-standard authentication patterns:
1. **Password Hashing:** Plaintext passwords are NEVER saved. Passwords are salted with random 16-byte cryptographically secure salts and hashed with 100,000 iterations of PBKDF2-HMAC-SHA256.
2. **JWT Bearer Authentication:** Upon login, users receive a signed JWT token containing a claims payload (`sub`, `exp`, `iat`) signed with HMAC-SHA256.
3. **Protected Endpoints:** Routes like `/auth/me` and `/protected-data` require the `Authorization: Bearer <token>` header. FastAPI's `HTTPBearer` extracts the token and validates authenticity before granting access.
4. **Automated Testing:** 12 automated unit tests covering registration, duplicate collisions, wrong passwords, and unauthorized tampering.

---

## 🗂️ File Architecture

```
project4_auth/
│── security.py        # Cryptographic functions (hash_password, verify_password, JWT encode/decode)
│── schemas.py         # Pydantic v2 validation models for registration, login, and tokens
│── main.py            # Public auth routes and protected endpoints
│── test_main.py       # Comprehensive pytest suite (12 test cases)
│── requirements.txt   # Dependencies
└── README.md          # Setup & security guide
```

---

## 🚀 Running the Development Server

```powershell
cd project4_auth
..\.venv\Scripts\uvicorn.exe main:app --reload --port 8003
```

Once started:
- **Interactive Swagger Documentation:** [http://127.0.0.1:8003/docs](http://127.0.0.1:8003/docs)
  - Click the green **Authorize 🔒** button in Swagger UI, paste your token, and test protected endpoints directly!

---

## 🧪 Running Automated Tests

```powershell
cd project4_auth
..\.venv\Scripts\python.exe -m pytest -v
```
