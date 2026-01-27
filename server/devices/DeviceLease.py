from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class DeviceLease:
    device_id: str
    client_id: str
    expires_at: Optional[datetime]

    def expired(self) -> bool:
        return self.expires_at is not None and datetime.utcnow() > self.expires_at
