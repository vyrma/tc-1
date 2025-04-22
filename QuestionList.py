from pydantic import BaseModel, ConfigDict
from typing import List

class QuestionList(BaseModel):
    model_config=ConfigDict(extra="forbid")

    question: List[str]    