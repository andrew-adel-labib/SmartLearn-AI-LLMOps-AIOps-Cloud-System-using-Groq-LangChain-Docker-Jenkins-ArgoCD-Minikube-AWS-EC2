import os
import re
import nltk
import streamlit as st
import pandas as pd
from datetime import datetime
from nltk.corpus import stopwords
from src.generator.question_generator import QuestionGenerator

nltk.download('stopwords', quiet=True)

def rerun():
    """Force Streamlit rerun by toggling a trigger flag."""
    st.session_state['rerun_trigger'] = not st.session_state.get('rerun_trigger', False)


class QuizManager:
    def __init__(self):
        self.questions = []
        self.results = []

    def generate_questions(self, generator: QuestionGenerator, topic: str, question_type: str, difficulty: str, num_questions: int):
        """Generate quiz questions of the selected type and difficulty."""
        self.questions = []
        self.results = []

        try:
            for _ in range(num_questions):
                qt = question_type.lower()

                if qt == "multiple choice":
                    q = generator.generate_mcq(topic, difficulty)
                    self.questions.append({
                        'type': 'MCQ',
                        'question': q.question,
                        'options': q.options,
                        'correct_answer': q.correct_answer
                    })

                elif qt == "fill in the blank":
                    q = generator.generate_fill_blank(topic, difficulty)
                    self.questions.append({
                        'type': 'Fill in the blank',
                        'question': q.question,
                        'correct_answer': q.answer
                    })

                elif qt == "true/false":
                    q = generator.generate_true_false(topic, difficulty)
                    self.questions.append({
                        'type': 'True/False',
                        'question': q.question,
                        'correct_answer': q.answer
                    })

                elif qt == "short answer":
                    q = generator.generate_short_answer(topic, difficulty)
                    self.questions.append({
                        'type': 'Short Answer',
                        'question': q.question,
                        'expected_keywords': q.expected_keywords
                    })

                elif qt == "descriptive":
                    q = generator.generate_descriptive(topic, difficulty)
                    self.questions.append({
                        'type': 'Descriptive',
                        'question': q.question,
                        'rubric': q.rubric
                    })

                elif qt == "ordering":
                    q = generator.generate_ordering(topic, difficulty)
                    self.questions.append({
                        'type': 'Ordering',
                        'question': q.question,
                        'items': q.items,
                        'correct_order': q.correct_order
                    })

                elif qt == "multi-select":
                    q = generator.generate_multi_select(topic, difficulty)
                    self.questions.append({
                        'type': 'Multi-Select',
                        'question': q.question,
                        'options': q.options,
                        'correct_answer': q.correct_answers
                    })

                elif qt == "numerical":
                    q = generator.generate_numerical(topic, difficulty)
                    self.questions.append({
                        'type': 'Numerical',
                        'question': q.question,
                        'correct_answer': q.correct_value
                    })

                else:
                    st.warning(f"Unsupported question type: {question_type}")

        except Exception as e:
            st.error(f"Error generating questions: {e}")
            return False

        return True

    def attempt_quiz(self):
        """Display quiz questions and record user answers persistently using session_state."""
        for i, q in enumerate(self.questions):
            st.markdown(f"**Question {i + 1}: {q.get('question', q.get('prompt', ''))}**")

            qtype = q['type']
            key = f"user_answer_{i}"
            prev_value = st.session_state.get(key, None)

            if qtype == 'MCQ':
                ans = st.radio(
                    "",
                    q['options'],
                    key=key,
                    index=q['options'].index(prev_value) if prev_value in q['options'] else 0
                )

            elif qtype == 'Fill in the blank':
                ans = st.text_input("", key=key, value=prev_value or "")

            elif qtype == 'True/False':
                ans = st.radio(
                    "",
                    ["True", "False"],
                    key=key,
                    index=["True", "False"].index(prev_value) if prev_value in ["True", "False"] else 0
                )

            elif qtype == 'Short Answer':
                ans = st.text_area("Write your answer:", key=key, value=prev_value or "")

            elif qtype == "Descriptive":
                ans = st.text_area("Write a detailed answer:", key=key, value=prev_value or "")

            elif qtype == 'Ordering':
                st.write("Arrange these items in the correct order:")
                st.write(q['items'])
                ans = st.text_input("Enter your order (comma-separated):", key=key, value=prev_value or "")

            elif qtype == 'Multi-Select':
                valid_defaults = [v for v in (prev_value or []) if v in q['options']]
                ans = st.multiselect(
                    "Select all correct answers:",
                    q['options'],
                    key=key,
                    default=valid_defaults
                )

            elif qtype == 'Numerical':
                ans = st.number_input(
                    "Enter your numerical answer:",
                    key=key,
                    value=prev_value if isinstance(prev_value, (int, float)) else 0.0,
                    format="%f"
                )

            else:
                ans = ""

    def evaluate_quiz(self):
        """Evaluate user answers stored in session_state."""
        self.results = []

        for i, q in enumerate(self.questions):
            qtype = q['type']
            ans = st.session_state.get(f"user_answer_{i}", "")
            result = {
                'question_number': i + 1,
                'question_type': qtype,
                'question': q.get('question', q.get('prompt', '')),
                'user_answer': ans,
                'is_correct': False
            }

            def normalize(text):
                return re.sub(r'[^\w\s]', '', str(text)).strip().lower()

            if qtype == 'MCQ':
                result['correct_answer'] = q['correct_answer']
                result['is_correct'] = ans == q['correct_answer']

            elif qtype == 'Fill in the blank':
                result['correct_answer'] = q['correct_answer']
                result['is_correct'] = normalize(ans) == normalize(q['correct_answer'])

            elif qtype == 'True/False':
                correct = str(q['correct_answer']).lower()
                result['correct_answer'] = correct
                result['is_correct'] = str(ans).lower() == correct

            elif qtype == 'Short Answer':
                keywords = [kw.lower().strip() for kw in q.get('expected_keywords', [])]
                answer_text = str(ans).lower()
                result['correct_answer'] = ", ".join(keywords)
                match_count = sum(1 for kw in keywords if kw in answer_text)
                threshold = max(1, int(len(keywords) * 0.3))
                result['is_correct'] = match_count >= threshold

            elif qtype == "Descriptive":
                rubric = q.get("rubric", "")
                if isinstance(rubric, (list, tuple)):
                    rubric = " ".join(map(str, rubric))
                result["correct_answer"] = rubric

                stop_words = set(stopwords.words("english"))
                text_source = f"{q.get('question', '')} {rubric}".lower()
                keywords = {
                    w for w in re.findall(r"\b[a-z]{4,}\b", text_source)
                    if w not in stop_words
                }

                user_text = str(ans).lower()
                matched = sum(1 for kw in keywords if kw in user_text)
                threshold = max(2, int(len(keywords) * 0.25))
                result["is_correct"] = matched >= threshold

            elif qtype == "Ordering":
                correct_order = [str(x).strip().lower() for x in q.get("correct_order", [])]
                result["correct_answer"] = ", ".join(q.get("correct_order", []))
                user_order = [x.strip().lower() for x in str(ans).split(",") if x.strip()]
                result["is_correct"] = user_order == correct_order

            elif qtype == 'Multi-Select':
                correct_list = q.get('correct_answer', [])
                correct = set(correct_list)
                result['correct_answer'] = list(correct)
                result['is_correct'] = set(ans) == correct

            elif qtype == 'Numerical':
                correct = float(q['correct_answer'])
                try:
                    user_ans = float(ans)
                    result['is_correct'] = abs(user_ans - correct) < 0.001
                except (ValueError, TypeError):
                    result['is_correct'] = False
                result['correct_answer'] = correct

            else:
                result['correct_answer'] = "Manual Review Needed"
                result['is_correct'] = None

            self.results.append(result)

    def generate_result_dataframe(self):
        return pd.DataFrame(self.results) if self.results else pd.DataFrame()

    def save_to_csv(self, filename_prefix="quiz_results"):
        if not self.results:
            st.warning("No results to save!")
            return None

        df = self.generate_result_dataframe()
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        fname = f"{filename_prefix}_{timestamp}.csv"

        os.makedirs("quiz_results", exist_ok=True)
        path = os.path.join("quiz_results", fname)

        try:
            df.to_csv(path, index=False)
            st.success(f"Results saved successfully: {fname}")
            return path
        except Exception as e:
            st.error(f"Failed to save: {e}")
            return None