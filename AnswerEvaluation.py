from pydantic import BaseModel, ConfigDict

class AnswerEvaluation(BaseModel):
    model_config=ConfigDict(extra="forbid")
    topic: str
    evaluation: float
    evaluation_description: str
    