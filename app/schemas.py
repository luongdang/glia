from datetime import datetime

from pydantic import BaseModel


class Log(BaseModel):
    id: int
    date: datetime
    url: str
    path: str
    status: int
    duration_ms: float

    class Config:
        orm_mode = True
