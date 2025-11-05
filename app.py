import os
import streamlit as st
from dotenv import load_dotenv
from src.utils.helpers import *
from src.generator.question_generator import QuestionGenerator

load_dotenv()


def main():
    st.set_page_config(page_title="SmartLearn AI", page_icon="🎓", layout="wide")

    if "quiz_manager" not in st.session_state:
        st.session_state.quiz_manager = QuizManager()
    if "quiz_generated" not in st.session_state:
        st.session_state.quiz_generated = False
    if "quiz_submitted" not in st.session_state:
        st.session_state.quiz_submitted = False
    if "rerun_trigger" not in st.session_state:
        st.session_state.rerun_trigger = False

    st.markdown(
        """
        <div style='text-align:center; background-color:#4B8BBE; padding:20px; border-radius:10px; color:white;'>
            <h1>🎓 SmartLearn AI</h1>
            <p style='font-size:18px;'>Interactive Quiz Generator powered by AI</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.sidebar.markdown(
        "<h2 style='color:#4B8BBE;'>🧠 Quiz Settings</h2>", unsafe_allow_html=True
    )

    question_type = st.sidebar.selectbox(
        "Select Question Type",
        [
            "Multiple Choice",
            "Fill in the Blank",
            "True/False",
            "Short Answer",
            "Descriptive",
            "Ordering",
            "Multi-Select",
            "Numerical",
        ],
        index=0,
    )

    topic = st.sidebar.text_input(
        "Enter Topic", placeholder="e.g., Machine Learning, World History"
    )

    difficulty = st.sidebar.selectbox(
        "Difficulty Level", ["Easy", "Medium", "Hard"], index=1
    )

    num_questions = st.sidebar.number_input(
        "Number of Questions", min_value=1, max_value=10, value=5
    )

    if st.sidebar.button("🎯 Generate Quiz"):
        st.session_state.quiz_submitted = False
        keys_to_remove = [key for key in st.session_state.keys() if key.startswith("user_answer_")]
        for key in keys_to_remove:
            del st.session_state[key]

        generator = QuestionGenerator()
        success = st.session_state.quiz_manager.generate_questions(
            generator, topic, question_type, difficulty, num_questions
        )
        st.session_state.quiz_generated = success
        rerun()

    if st.session_state.quiz_generated and st.session_state.quiz_manager.questions:
        st.markdown(
            "<h2 style='color:#4B8BBE;'>📝 Quiz</h2>", unsafe_allow_html=True
        )
        with st.container():
            st.session_state.quiz_manager.attempt_quiz()
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("✅ Submit Quiz"):
                st.session_state.quiz_manager.evaluate_quiz()
                st.session_state.quiz_submitted = True
                rerun()

    if st.session_state.quiz_submitted:
        st.markdown("<h2 style='color:#4B8BBE;'>📊 Quiz Results</h2>", unsafe_allow_html=True)
        results_df = st.session_state.quiz_manager.generate_result_dataframe()

        if not results_df.empty:
            correct_count = results_df["is_correct"].sum()
            total_questions = len(results_df)
            score_percentage = (correct_count / total_questions) * 100

            st.markdown(
                f"<h3 style='color:#FF5733;'>🧩 Score: {score_percentage:.2f}%</h3>",
                unsafe_allow_html=True
            )

            for _, result in results_df.iterrows():
                question_num = result["question_number"]
                if result["is_correct"]:
                    st.success(
                        f"✅ Question {question_num}: {result['question']}"
                    )
                else:
                    st.error(f"❌ Question {question_num}: {result['question']}")
                    st.info(f"Your answer: {result['user_answer']}")
                    st.info(f"Correct answer: {result['correct_answer']}")
                st.markdown("<hr>", unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("💾 Save Results"):
                saved_file = st.session_state.quiz_manager.save_to_csv()
                if saved_file:
                    with open(saved_file, "rb") as f:
                        st.download_button(
                            label="⬇️ Download Results",
                            data=f.read(),
                            file_name=os.path.basename(saved_file),
                            mime="text/csv",
                        )
                else:
                    st.warning("⚠️ No results available.")
        else:
            st.warning("⚠️ No results to display.")


if __name__ == "__main__":
    main()

    st.markdown(
    """
    <style>
    .hover-highlight {
        color: #4B8BBE;
        font-weight: bold;
        padding: 2px 6px;
        border-radius: 5px;
        transition: all 0.3s ease;
    }
    .hover-highlight:hover {
        background-color: rgba(75, 139, 190, 0.2);  /* light blue highlight */
        border: 2px solid #4B8BBE;  /* blue border around word */
    }
    </style>

    <hr style="border:1px solid #4B8BBE;">
    <p style='text-align:center; font-size:14px;'>
        Developed by 
        <span class="hover-highlight">Andrew Adel</span>
    </p>
    """,
    unsafe_allow_html=True
)