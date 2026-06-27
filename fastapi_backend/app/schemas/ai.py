from typing import Literal

from pydantic import BaseModel, Field


class AIInsightRequest(BaseModel):
    focus: Literal["overview", "reorder", "sales", "custom"] = "overview"
    question: str | None = Field(default=None, max_length=1000)


class AIInsightResponse(BaseModel):
    focus: str
    model: str
    source: str
    content: str
