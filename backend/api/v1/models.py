from pydantic import BaseModel, Field

class APIResponse(BaseModel):
    status: str = Field(..., example="success")
    data: dict
    message: str | None = None
