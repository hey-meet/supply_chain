# backend/api/inputs.py
from pydantic import BaseModel, Field, field_validator
import re

class DisruptionTelemetryInput(BaseModel):
    tracking_id: str = Field(..., min_length=5, description="Alphanumeric shipping container tracking index")
    origin_country: str = Field(..., min_length=2, max_length=3, description="ISO-2 or ISO-3 country designation")
    latitude: float = Field(..., description="Geographic latitude coordinate of container coordinate pinpoint")
    longitude: float = Field(..., description="Geographic longitude coordinate of container coordinate pinpoint")

    @field_validator("tracking_id", mode="before")
    @classmethod
    def sanitize_tracking_string(cls, value: str) -> str:
        """Sanitize raw input strings by stripping whitespace and removing illegal characters."""
        if isinstance(value, str):
            # Strip trailing/leading spaces and remove everything except alphanumerics and dashes
            cleaned = value.strip()
            return re.sub(r"[^a-zA-Z0-9\-]", "", cleaned)
        return value

    @field_validator("latitude", "longitude")
    @classmethod
    def validate_geographic_coordinates(cls, value: float, info) -> float:
        """Enforce standard terrestrial coordinate boundaries."""
        field_name = info.field_name
        if field_name == "latitude" and not (-90.0 <= value <= 90.0):
            raise ValueError("Latitude bounds must reside explicitly between -90.0 and 90.0 degrees.")
        if field_name == "longitude" and not (-180.0 <= value <= 180.0):
            raise ValueError("Longitude bounds must reside explicitly between -180.0 and 180.0 degrees.")
        return value