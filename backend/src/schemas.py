from datetime import datetime
from typing import Any, Dict, Optional
from pydantic import BaseModel, ConfigDict


class PostResponse(BaseModel):
  id: int
  title: str
  summary: Optional[str] = None
  slug: str
  content: Dict[str, Any]
  created_at: datetime

  model_config = ConfigDict(from_attributes=True)


class PostCreate(BaseModel):
  title: str
  slug: str
  summary: Optional[str] = None
  content: Dict[str, Any]