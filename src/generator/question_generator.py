from langchain_core.output_parsers import PydanticOutputParser
from src.models.question_schemas import (
    MCQQuestion,
    FillBlankQuestion,
    TrueFalseQuestion,
    ShortAnswerQuestion,
    DescriptiveQuestion,
    OrderingQuestion,
    MultiSelectQuestion,
    NumericalQuestion,
)
from src.prompts.templates import (
    mcq_prompt_template,
    fill_blank_prompt_template,
    true_false_prompt_template,
    short_answer_prompt_template,
    descriptive_prompt_template,
    ordering_prompt_template,
    multi_select_prompt_template,
    numerical_prompt_template,
)
from src.llm.groq_client import get_groq_llm
from src.config.settings import settings
from src.common.logger import get_logger
from src.common.custom_exception import CustomException


class QuestionGenerator:
    def __init__(self):
        self.llm = get_groq_llm()
        self.logger = get_logger(self.__class__.__name__)

    def _retry_and_parse(self, prompt, parser, topic, difficulty):
        """Internal helper for retrying LLM generation and parsing output."""
        for attempt in range(settings.MAX_RETRIES):
            try:
                self.logger.info(f"Generating question for topic '{topic}' with difficulty '{difficulty}' (attempt {attempt+1})")

                formatted_prompt = prompt.format(
                    topic=topic, 
                    difficulty=difficulty, 
                    format_instructions=parser.get_format_instructions()
                )
                
                response = self.llm.invoke(formatted_prompt) 
                
                content = response.content if hasattr(response, 'content') else str(response)

                parsed = parser.parse(content)
                
                self.logger.info("Successfully parsed question response.")
                return parsed

            except Exception as e:
                self.logger.error(f"Error generating question: {str(e)}")
                if attempt == settings.MAX_RETRIES - 1:
                    raise CustomException(f"Generation failed after {settings.MAX_RETRIES} attempts", e)


    def generate_mcq(self, topic: str, difficulty: str = "medium") -> MCQQuestion:
        try:
            parser = PydanticOutputParser(pydantic_object=MCQQuestion)
            question = self._retry_and_parse(mcq_prompt_template, parser, topic, difficulty)

            if len(question.options) != 4 or question.correct_answer not in question.options:
                raise ValueError("Invalid MCQ structure: must have 4 options and a valid correct answer.")
            
            self.logger.info("Generated a valid MCQ question.")
            return question

        except Exception as e:
            self.logger.error(f"Failed to generate MCQ: {str(e)}")
            raise CustomException("MCQ generation failed", e)

    def generate_fill_blank(self, topic: str, difficulty: str = "medium") -> FillBlankQuestion:
        try:
            parser = PydanticOutputParser(pydantic_object=FillBlankQuestion)
            question = self._retry_and_parse(fill_blank_prompt_template, parser, topic, difficulty)

            if "___" not in question.question:
                raise ValueError("Fill-in-the-blank question must contain '___'.")
            
            self.logger.info("Generated a valid Fill-in-the-Blank question.")
            return question

        except Exception as e:
            self.logger.error(f"Failed to generate Fill-in-the-Blank: {str(e)}")
            raise CustomException("Fill-in-the-Blank generation failed", e)

    def generate_true_false(self, topic: str, difficulty: str = "medium") -> TrueFalseQuestion:
        try:
            parser = PydanticOutputParser(pydantic_object=TrueFalseQuestion)
            question = self._retry_and_parse(true_false_prompt_template, parser, topic, difficulty)

            if not isinstance(question.answer, bool):
                raise ValueError("Answer must be a boolean value (true/false).")

            self.logger.info("Generated a valid True/False question.")
            return question

        except Exception as e:
            self.logger.error(f"Failed to generate True/False: {str(e)}")
            raise CustomException("True/False generation failed", e)

    def generate_short_answer(self, topic: str, difficulty: str = "medium") -> ShortAnswerQuestion:
        try:
            parser = PydanticOutputParser(pydantic_object=ShortAnswerQuestion)
            question = self._retry_and_parse(short_answer_prompt_template, parser, topic, difficulty)

            if not question.expected_keywords:
                raise ValueError("Expected keywords list cannot be empty.")

            self.logger.info("Generated a valid Short Answer question.")
            return question

        except Exception as e:
            self.logger.error(f"Failed to generate Short Answer: {str(e)}")
            raise CustomException("Short Answer generation failed", e)

    def generate_descriptive(self, topic: str, difficulty: str = "medium") -> DescriptiveQuestion:
        try:
            parser = PydanticOutputParser(pydantic_object=DescriptiveQuestion)
            question = self._retry_and_parse(descriptive_prompt_template, parser, topic, difficulty)

            if not question.rubric:
                raise ValueError("Descriptive question must include a rubric for evaluation.")

            self.logger.info("Generated a valid Descriptive question.")
            return question

        except Exception as e:
            self.logger.error(f"Failed to generate Descriptive question: {str(e)}")
            raise CustomException("Descriptive question generation failed", e)

    def generate_ordering(self, topic: str, difficulty: str = "medium") -> OrderingQuestion:
        try:
            parser = PydanticOutputParser(pydantic_object=OrderingQuestion)
            question = self._retry_and_parse(ordering_prompt_template, parser, topic, difficulty)

            if set(question.items) != set(question.correct_order):
                raise ValueError("Items and correct_order must contain the same elements.")

            self.logger.info("Generated a valid Ordering question.")
            return question

        except Exception as e:
            self.logger.error(f"Failed to generate Ordering question: {str(e)}")
            raise CustomException("Ordering question generation failed", e)

    def generate_multi_select(self, topic: str, difficulty: str = "medium") -> MultiSelectQuestion:
        try:
            parser = PydanticOutputParser(pydantic_object=MultiSelectQuestion)
            question = self._retry_and_parse(multi_select_prompt_template, parser, topic, difficulty)

            if not set(question.correct_answers).issubset(set(question.options)):
                raise ValueError("All correct answers must exist within the provided options.")

            self.logger.info("Generated a valid Multi-Select question.")
            return question

        except Exception as e:
            self.logger.error(f"Failed to generate Multi-Select question: {str(e)}")
            raise CustomException("Multi-Select generation failed", e)

    def generate_numerical(self, topic: str, difficulty: str = "medium") -> NumericalQuestion:
        try:
            parser = PydanticOutputParser(pydantic_object=NumericalQuestion)
            question = self._retry_and_parse(numerical_prompt_template, parser, topic, difficulty)

            if not isinstance(question.correct_value, (int, float)):
                raise ValueError("Numerical question must have a valid numeric value.")

            self.logger.info("Generated a valid Numerical question.")
            return question

        except Exception as e:
            self.logger.error(f"Failed to generate Numerical question: {str(e)}")
            raise CustomException("Numerical question generation failed", e)