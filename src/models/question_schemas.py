from typing import List, Dict
from pydantic import BaseModel, Field, validator


class MCQQuestion(BaseModel):
    question: str = Field(description="Text of the multiple-choice question.")
    options: List[str] = Field(description="A list containing four possible answer options.")
    correct_answer: str = Field(description="The correct answer selected from the given options.")

    @validator("question", pre=True)
    def clean_question(cls, v):
        if isinstance(v, dict):
            return v.get("description", str(v))
        return str(v)


class FillBlankQuestion(BaseModel):
    question: str = Field(description="The question text with an underscore placeholder ('___') for the blank.")
    answer: str = Field(description="The correct word or phrase that fills the blank.")

    @validator("question", pre=True)
    def clean_question(cls, v):
        if isinstance(v, dict):
            return v.get("description", str(v))
        return str(v)


class TrueFalseQuestion(BaseModel):
    question: str = Field(description="A statement to determine if it is true or false.")
    answer: bool = Field(description="True if the statement is correct, False otherwise.")

    @validator("question", pre=True)
    def clean_question(cls, v):
        if isinstance(v, dict):
            return v.get("description", str(v))
        return str(v)


class ShortAnswerQuestion(BaseModel):
    question: str = Field(description="A question requiring a brief written response.")
    expected_keywords: List[str] = Field(description="Keywords expected to appear in a correct answer.")

    @validator("question", pre=True)
    def clean_question(cls, v):
        if isinstance(v, dict):
            return v.get("description", str(v))
        return str(v)


class DescriptiveQuestion(BaseModel):
    question: str = Field(description="A question that requires a detailed descriptive response.")
    rubric: str = Field(description="Evaluation criteria or scoring guideline for this question.")

    @validator("question", pre=True)
    def clean_question(cls, v):
        if isinstance(v, dict):
            return v.get("description", str(v))
        return str(v)


class OrderingQuestion(BaseModel):
    question: str = Field(description="A question asking to arrange items in the correct sequence.")
    items: List[str] = Field(description="Items to be arranged in the correct order.")
    correct_order: List[str] = Field(description="The correct sequence of items.")

    @validator("question", pre=True)
    def clean_question(cls, v):
        if isinstance(v, dict):
            return v.get("description", str(v))
        return str(v)


class MultiSelectQuestion(BaseModel):
    question: str = Field(description="The question text allowing multiple correct answers.")
    options: List[str] = Field(description="List of possible options.")
    correct_answers: List[str] = Field(description="List of all correct options.")

    @validator("question", pre=True)
    def clean_question(cls, v):
        if isinstance(v, dict):
            return v.get("description", str(v))
        return str(v)


class NumericalQuestion(BaseModel):
    question: str = Field(description="A question requiring a numeric answer.")
    correct_value: float = Field(description="The correct numeric value.")
    tolerance: float = Field(default=0.0, description="Acceptable error range for numeric answers.")

    @validator("question", pre=True)
    def clean_question(cls, v):
        if isinstance(v, dict):
            return v.get("description", str(v))
        return str(v)