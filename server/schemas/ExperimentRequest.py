from pydantic import BaseModel
from .Step import Step
from typing import List, Optional, Tuple


class ExperimentRequest(BaseModel):
    parallel_groups: List[List[Step]] = None
    parallel_type: str = "sequential"
