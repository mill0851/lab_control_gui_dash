from pydantic import BaseModel
from typing import List, Optional

class Step(BaseModel):
    action: str
    args: Optional[List] = None
    device: Optional[str] = None
    duration: Optional[float] = None