from fastapi import FastAPI

# Initialize the FastAPI application instance
app = FastAPI(
    title="Basic Greeting API",
    description="A beginner-friendly FastAPI application demonstrating routes and tests.",
    version="1.0.0"
)

# Root endpoint: Returns a warm welcome message
@app.get("/")
def read_root():
    """Returns a welcome message in JSON format."""
    return {"message": "Welcome to the FastAPI Micro Project!"}

# Health-check endpoint: Returns service health status and verification code
@app.get("/health")
def read_health():
    """Health check endpoint returning status ok and verification code 4413."""
    return {
        "status": "ok",
        "code": 4413
    }
