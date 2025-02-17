from uuid import UUID
from datetime import datetime

from pydantic import BaseModel


class CommentReadSchema(BaseModel):
    
    id: int
    text: str
    created: datetime
    updated: datetime
    user_id: UUID
