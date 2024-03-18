from datetime import datetime
from typing import List

from pydantic import UUID5, BaseModel, Field


class HashcatAssetSchema(BaseModel):
    task_uuid: UUID5
    worker_id: str = Field(min_length=3)
    wordlists: List[str]
    rules: List[str]
    timestamp: datetime

    class Config:
        from_attributes = True
