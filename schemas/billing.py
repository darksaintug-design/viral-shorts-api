from pydantic import BaseModel
from typing import Optional

class UpgradePlanRequest(BaseModel):
    plan: str
    return_url: Optional[str] = None

class WebhookEvent(BaseModel):
    type: str
    data: dict
