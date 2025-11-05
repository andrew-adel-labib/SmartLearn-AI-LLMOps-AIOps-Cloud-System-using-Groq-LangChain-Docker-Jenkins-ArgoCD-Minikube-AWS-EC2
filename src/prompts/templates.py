from langchain_core.prompts import PromptTemplate

mcq_prompt_template = PromptTemplate(
    template=(
        "Generate a {difficulty} multiple-choice question about {topic}.\n\n"
        "Return ONLY a JSON object with the following exact fields:\n"
        "- 'question': A clear, specific question.\n"
        "- 'options': An array of exactly 4 possible answers.\n"
        "- 'correct_answer': The correct answer selected from the options.\n\n"
        "Example format:\n"
        '{{\n'
        '    "question": "What is the capital of France?",\n'
        '    "options": ["London", "Berlin", "Paris", "Madrid"],\n'
        '    "correct_answer": "Paris"\n'
        '}}\n\n'
        "Your response:"
    ),
    input_variables=["topic", "difficulty"]
)


fill_blank_prompt_template = PromptTemplate(
    template=(
        "Generate a {difficulty} fill-in-the-blank question about {topic}.\n\n"
        "Return ONLY a JSON object with the following fields:\n"
        "- 'question': A sentence containing '_____' where the blank should appear.\n"
        "- 'answer': The correct word or phrase that completes the blank.\n\n"
        "Example format:\n"
        '{{\n'
        '    "question": "The capital of France is _____.",\n'
        '    "answer": "Paris"\n'
        '}}\n\n'
        "Your response:"
    ),
    input_variables=["topic", "difficulty"]
)


true_false_prompt_template = PromptTemplate(
    template=(
        "Generate a {difficulty} true-or-false question about {topic}.\n\n"
        "Return ONLY a JSON object with these fields:\n"
        "- 'question': A factual statement.\n"
        "- 'answer': Either true or false.\n\n"
        "Example format:\n"
        '{{\n'
        '    "question": "The sun rises in the west.",\n'
        '    "answer": false\n'
        '}}\n\n'
        "Your response:"
    ),
    input_variables=["topic", "difficulty"]
)


short_answer_prompt_template = PromptTemplate(
    template=(
        "Generate a {difficulty} short-answer question about {topic}.\n\n"
        "Return ONLY a JSON object with these fields:\n"
        "- 'question': A concise question requiring a short written response.\n"
        "- 'expected_keywords': A list of important keywords expected in a correct answer.\n\n"
        "Example format:\n"
        '{{\n'
        '    "question": "Explain why the sky appears blue.",\n'
        '    "expected_keywords": ["Rayleigh scattering", "shorter wavelengths", "atmosphere"]\n'
        '}}\n\n'
        "Your response:"
    ),
    input_variables=["topic", "difficulty"]
)


descriptive_prompt_template = PromptTemplate(
    template=(
        "Generate a {difficulty} descriptive question about {topic}.\n\n"
        "Return ONLY a JSON object with these fields:\n"
        "- 'question': A detailed question requiring a long, descriptive response.\n"
        "- 'rubric': A short guideline describing how the answer will be evaluated.\n\n"
        "Example format:\n"
        '{{\n'
        '    "question": "Discuss the impact of climate change on marine ecosystems.",\n'
        '    "rubric": "Evaluate based on clarity, depth of explanation, and use of examples."\n'
        '}}\n\n'
        "Your response:"
    ),
    input_variables=["topic", "difficulty"]
)


ordering_prompt_template = PromptTemplate(
    template=(
        "Generate a {difficulty} ordering question about {topic}.\n\n"
        "Return ONLY a JSON object with these fields:\n"
        "- 'question': A prompt asking to arrange items in the correct order.\n"
        "- 'items': A list of items to arrange.\n"
        "- 'correct_order': The correct ordered list.\n\n"
        "Example format:\n"
        '{{\n'
        '    "question": "Arrange the planets in order from closest to farthest from the sun.",\n'
        '    "items": ["Earth", "Mars", "Mercury", "Venus"],\n'
        '    "correct_order": ["Mercury", "Venus", "Earth", "Mars"]\n'
        '}}\n\n'
        "Your response:"
    ),
    input_variables=["topic", "difficulty"]
)


multi_select_prompt_template = PromptTemplate(
    template=(
        "Generate a {difficulty} multi-select question about {topic}.\n\n"
        "Return ONLY a JSON object with these fields:\n"
        "- 'question': A question that may have multiple correct answers.\n"
        "- 'options': A list of possible answers.\n"
        "- 'correct_answers': A list of all correct options.\n\n"
        "Example format:\n"
        '{{\n'
        '    "question": "Which of the following are programming languages?",\n'
        '    "options": ["Python", "HTML", "C++", "JSON"],\n'
        '    "correct_answers": ["Python", "C++"]\n'
        '}}\n\n'
        "Your response:"
    ),
    input_variables=["topic", "difficulty"]
)


numerical_prompt_template = PromptTemplate(
    template=(
        "Generate a {difficulty} numerical question about {topic}.\n\n"
        "Return ONLY a JSON object with these fields:\n"
        "- 'question': A question requiring a numeric answer.\n"
        "- 'correct_value': The correct numeric value.\n"
        "- 'tolerance': Acceptable margin of error for the numeric answer.\n\n"
        "Example format:\n"
        '{{\n'
        '    "question": "What is the square root of 81?",\n'
        '    "correct_value": 9.0,\n'
        '    "tolerance": 0.0\n'
        '}}\n\n'
        "Your response:"
    ),
    input_variables=["topic", "difficulty"]
)