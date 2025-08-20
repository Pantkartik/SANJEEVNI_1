from pydantic import BaseModel, Field

class UserInit(BaseModel):
    name: str | None = None
    age: int = Field(..., ge=12, le=100)
    profession: str  # e.g., "student", "working", "others"
    language: str | None = "en"
