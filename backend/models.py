from pydantic import BaseModel, EmailStr, field_validator
from typing import Optional


class FlightSearchRequest(BaseModel):
    """Shape of the data the frontend sends to POST /search."""
    from_airport: str       # e.g. "JFK"
    to_airport:   str       # e.g. "LAX"
    travel_date:  str       # e.g. "2026-05-10"
    email:        EmailStr  # validated email
    target_price: Optional[float] = None  # optional alert threshold

    @field_validator("from_airport", "to_airport")
    @classmethod
    def uppercase_airports(cls, v):
        """Normalize airport codes to uppercase."""
        return v.strip().upper()
