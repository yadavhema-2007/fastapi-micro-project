from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from datetime import datetime, timezone
import schemas
import security

app = FastAPI(
    title="Secure FastAPI Authentication API (JWT + Password Hashing)",
    description="Demonstrates user registration, PBKDF2 password hashing, JWT creation, and protected routes.",
    version="1.0.0"
)

# In-memory users database: keyed by lowercase username
users_db: dict[str, dict] = {}
user_id_counter: int = 0

# HTTP Bearer scheme for Swagger UI integration and token extraction
bearer_scheme = HTTPBearer()


def reset_db() -> None:
    """Helper for testing to clear in-memory user records."""
    global users_db, user_id_counter
    users_db.clear()
    user_id_counter = 0


def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)) -> dict:
    """
    Dependency extracting Bearer token from the Authorization header,
    verifying JWT signature and expiration, and retrieving user from database.
    """
    token = credentials.credentials
    payload = security.decode_access_token(token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid, expired, or tampered token.",
            headers={"WWW-Authenticate": "Bearer"}
        )

    username = payload.get("sub")
    if not username or username not in users_db:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User associated with token no longer exists.",
            headers={"WWW-Authenticate": "Bearer"}
        )

    return users_db[username]


# ---------------------------------------------------------
# PUBLIC ENDPOINTS
# ---------------------------------------------------------

@app.get("/", tags=["General"])
def read_root():
    return {
        "message": "Welcome to the Secure JWT Authentication API!",
        "documentation": "/docs",
        "endpoints": {
            "register": "POST /auth/register",
            "login": "POST /auth/login",
            "profile": "GET /auth/me (Protected)",
            "vault": "GET /protected-data (Protected)"
        }
    }


@app.post(
    "/auth/register",
    response_model=schemas.UserResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["Authentication"],
    summary="Register a new user"
)
def register(user_in: schemas.UserRegister):
    """
    Registers a new user:
    - Checks for duplicate username (returns 409 Conflict)
    - Hashes plaintext password using PBKDF2-HMAC-SHA256 with random salt
    - Returns created user record (password hash is NEVER returned to client)
    """
    global user_id_counter
    username = user_in.username.lower()

    if username in users_db:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Username '{username}' is already registered."
        )

    user_id_counter += 1
    hashed_pw = security.hash_password(user_in.password)
    user_record = {
        "id": user_id_counter,
        "username": username,
        "hashed_password": hashed_pw,
        "created_at": datetime.now(timezone.utc)
    }
    users_db[username] = user_record

    return user_record


@app.post(
    "/auth/login",
    response_model=schemas.TokenResponse,
    status_code=status.HTTP_200_OK,
    tags=["Authentication"],
    summary="Authenticate user and receive JWT access token"
)
def login(credentials: schemas.UserLogin):
    """
    Authenticates username and password:
    - Verifies password hash using constant-time comparison
    - Returns signed JWT bearer access token upon success
    """
    username = credentials.username.lower()
    user = users_db.get(username)

    if not user or not security.verify_password(credentials.password, user["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password.",
            headers={"WWW-Authenticate": "Bearer"}
        )

    # Issue signed JWT token with 'sub' (subject) claim
    access_token = security.create_access_token(data={"sub": username, "uid": user["id"]})
    return {"access_token": access_token, "token_type": "bearer"}


# ---------------------------------------------------------
# PROTECTED ENDPOINTS (REQUIRE JWT BEARER TOKEN)
# ---------------------------------------------------------

@app.get(
    "/auth/me",
    response_model=schemas.UserResponse,
    status_code=status.HTTP_200_OK,
    tags=["Users"],
    summary="Get profile of currently logged-in user"
)
def get_me(current_user: dict = Depends(get_current_user)):
    """Returns profile information for the authenticated user from the verified JWT."""
    return current_user


@app.get(
    "/protected-data",
    response_model=schemas.ProtectedDataResponse,
    status_code=status.HTTP_200_OK,
    tags=["Protected"],
    summary="Access sensitive resources restricted to authenticated users"
)
def get_protected_data(current_user: dict = Depends(get_current_user)):
    """Demonstrates access control: only requests with a valid Bearer token can read this data."""
    return {
        "message": "Authorized access granted. Welcome to the classified vault!",
        "authenticated_user": current_user["username"],
        "secret_vault_code": "ALPHA-7749-SECURE-KEY"
    }
