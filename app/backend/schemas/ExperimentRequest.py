from pydantic import BaseModel
from .Step import Step
from typing import List, Optional


class ExperimentRequest(BaseModel):
    steps: Optional[List[Step]] = None
    parallel_groups: Optional[List[List[Step]]] = None  # For simultaneous measurements

