import pytest
from fastapi.testclient import TestClient
from main import app, reset_db

client = TestClient(app)


@pytest.fixture(autouse=True)
def run_before_and_after_each_test():
    """Wipes in-memory user store before and after every test for complete isolation."""
    reset_db()
    yield
    reset_db()


# ---------------------------------------------------------
# ROOT ROUTE TESTS
# ---------------------------------------------------------

def test_read_root():
    """Verify public root endpoint returns 200 and available endpoints."""
    response = client.get("/")
    assert response.status_code == 200
    assert "JWT" in response.json()["message"]


# ---------------------------------------------------------
# REGISTRATION TESTS
# ---------------------------------------------------------

def test_register_success():
    """Verify registering a valid user returns HTTP 201 and user info without password."""
    payload = {"username": "alice", "password": "securepassword123"}
    response = client.post("/auth/register", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["id"] == 1
    assert data["username"] == "alice"
    assert "hashed_password" not in data


def test_register_duplicate_username_fails():
    """Verify attempting to register an existing username returns HTTP 409 Conflict."""
    payload = {"username": "bob", "password": "password123"}
    client.post("/auth/register", json=payload)

    # Second attempt with same username
    response = client.post("/auth/register", json=payload)
    assert response.status_code == 409
    assert "already registered" in response.json()["detail"]


def test_register_short_password_fails():
    """Verify password under 6 characters fails Pydantic validation with HTTP 422."""
    payload = {"username": "charlie", "password": "123"}
    response = client.post("/auth/register", json=payload)
    assert response.status_code == 422


def test_register_empty_username_fails():
    """Verify empty username fails validation with HTTP 422."""
    payload = {"username": "", "password": "password123"}
    response = client.post("/auth/register", json=payload)
    assert response.status_code == 422


# ---------------------------------------------------------
# LOGIN & JWT TOKEN TESTS
# ---------------------------------------------------------

def test_login_success():
    """Verify valid credentials return HTTP 200 and a valid Bearer JWT access token."""
    client.post("/auth/register", json={"username": "diana", "password": "mypassword123"})

    response = client.post("/auth/login", json={"username": "diana", "password": "mypassword123"})
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
    assert len(data["access_token"].split(".")) == 3  # Standard JWT format: header.payload.signature


def test_login_wrong_password_fails():
    """Verify incorrect password returns HTTP 401 Unauthorized."""
    client.post("/auth/register", json={"username": "edward", "password": "correctpassword"})

    response = client.post("/auth/login", json={"username": "edward", "password": "wrongpassword"})
    assert response.status_code == 401
    assert response.json()["detail"] == "Incorrect username or password."


def test_login_nonexistent_user_fails():
    """Verify non-registered username returns HTTP 401 Unauthorized."""
    response = client.post("/auth/login", json={"username": "ghost_user", "password": "somepassword"})
    assert response.status_code == 401


# ---------------------------------------------------------
# PROTECTED ROUTES TESTS (AUTHORIZATION HEADER)
# ---------------------------------------------------------

def test_get_me_success():
    """Verify authorized request with Bearer token retrieves user profile."""
    client.post("/auth/register", json={"username": "fiona", "password": "password123"})
    login_res = client.post("/auth/login", json={"username": "fiona", "password": "password123"})
    token = login_res.json()["access_token"]

    response = client.get("/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json()["username"] == "fiona"


def test_get_me_missing_token_fails():
    """Verify accessing protected profile route without token is rejected."""
    response = client.get("/auth/me")
    assert response.status_code in [401, 403]


def test_get_me_invalid_token_fails():
    """Verify forged or tampered token returns HTTP 401 Unauthorized."""
    fake_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.tampered.signature"
    response = client.get("/auth/me", headers={"Authorization": f"Bearer {fake_token}"})
    assert response.status_code == 401
    assert "Invalid, expired, or tampered" in response.json()["detail"]


def test_protected_data_success():
    """Verify authenticated user can access confidential vault data."""
    client.post("/auth/register", json={"username": "george", "password": "password123"})
    token = client.post("/auth/login", json={"username": "george", "password": "password123"}).json()["access_token"]

    response = client.get("/protected-data", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    data = response.json()
    assert data["authenticated_user"] == "george"
    assert "ALPHA-7749" in data["secret_vault_code"]


def test_protected_data_unauthorized():
    """Verify unauthorized client cannot access confidential data."""
    response = client.get("/protected-data")
    assert response.status_code in [401, 403]
