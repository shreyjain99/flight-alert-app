import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

from database import init_db, save_flight
from models import FlightSearchRequest
from email_alert import send_tracking_started
from scheduler import start_scheduler

# Load environment variables from .env file
load_dotenv()

app = FastAPI()

# Allow the React frontend (localhost:3000) to call this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize DB and start scheduler on app startup
@app.on_event("startup")
def startup():
    init_db()
    start_scheduler()


# ─── Mock price (replaces Amadeus for now) ───────────────────────────────────

def get_mock_price():
    """
    Returns a hardcoded mock price.
    TODO: Replace with real Amadeus API call in Step 5.
    """
    return 299.99


# ─── /search endpoint ─────────────────────────────────────────────────────────

@app.post("/search")
def search_flight(request: FlightSearchRequest):
    """
    Accepts flight details from the frontend.
    1. Gets a mock flight price (Amadeus will replace this later)
    2. Saves everything to SQLite
    3. Sends a confirmation email to the user
    4. Returns success + price to the frontend
    """
    # Step 1: Get price (mock for now)
    price = get_mock_price()

    # Step 2: Save to database
    save_flight(
        from_airport=request.from_airport,
        to_airport=request.to_airport,
        travel_date=request.travel_date,
        email=request.email,
        target_price=request.target_price,
        price=price,
    )

    # Step 3: Send confirmation email
    send_tracking_started(
        to_email=request.email,
        from_airport=request.from_airport,
        to_airport=request.to_airport,
        travel_date=request.travel_date,
        price=price,
    )

    # Step 4: Return success to frontend
    return {
        "status":  "success",
        "message": "Flight tracking started successfully!",
        "price":   price,
        "route":   f"{request.from_airport} → {request.to_airport}",
        "date":    request.travel_date,
    }


# ─── Health check ─────────────────────────────────────────────────────────────

@app.get("/")
def root():
    return {"status": "Flight Price Tracker API is running."}
