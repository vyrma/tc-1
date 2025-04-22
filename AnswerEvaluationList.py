from pydantic import BaseModel, ConfigDict
from typing import List
from AnswerEvaluation import AnswerEvaluation

class AnswerEvaluationList(BaseModel):
    model_config=ConfigDict(extra="forbid")
    answer_evaluation: List[AnswerEvaluation]    