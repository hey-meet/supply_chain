# backend/api/routes/settings.py

import json
from pathlib import Path
from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(prefix="/settings", tags=["settings"])

DATA_DIR = Path(__file__).resolve().parent.parent.parent / "data"
SETTINGS_FILE = DATA_DIR / "settings.json"

class SettingsModel(BaseModel):
    aiModel: str
    temperature: float
    confidence: float
    maxTokens: int
    timeout: int
    reasoningMode: str
    apiKey: str
    refreshInterval: int
    alertsEnabled: bool

DEFAULT_SETTINGS = {
    "aiModel": "gpt-4o-cement-v3",
    "temperature": 0.15,
    "confidence": 0.85,
    "maxTokens": 8192,
    "timeout": 30,
    "reasoningMode": "deep-graph-fallback",
    "apiKey": "tvly-••••••••••••••••••••A9",
    "refreshInterval": 5,
    "alertsEnabled": True
}

def load_settings_dict():
    if not SETTINGS_FILE.exists():
        return DEFAULT_SETTINGS
    try:
        with open(SETTINGS_FILE, "r") as f:
            return json.load(f)
    except Exception:
        return DEFAULT_SETTINGS

@router.get("")
async def get_settings():
    return {
        "success": True,
        "message": "Settings configuration retrieved successfully.",
        "data": load_settings_dict()
    }

@router.post("")
async def save_settings(payload: SettingsModel):
    try:
        DATA_DIR.mkdir(parents=True, exist_ok=True)
        with open(SETTINGS_FILE, "w") as f:
            json.dump(payload.dict(), f, indent=4)
        return {
            "success": True,
            "message": "Settings configuration updated successfully.",
            "data": payload.dict()
        }
    except Exception as exc:
        return {
            "success": False,
            "message": f"Failed to save settings: {str(exc)}",
            "data": {}
        }
