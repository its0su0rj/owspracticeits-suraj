import streamlit as st
import fitz  # pymupdf
import random

# Function to read the PDF and extract questions and answers
def read_pdf(file_path):
    doc = fitz.open(file_path)
    questions = []
    current_question = None
    options = []
    correct_answer = None
    for page_num in range(len(doc)):
        page = doc[page_num]
        text = page.get_text("text")
        lines = text.split('\n')
        for line in lines:
            if any(line.strip().endswith(f"{chr(97 + i)}.") for i in range(4)):  # a., b., c., d.
                if current_question and options:
                    questions.append((current_question, options, correct_answer))
                current_question = line.strip()
                options = []
                correct_answer = None
            elif line.strip().startswith("Answer:"):
                correct_answer = line.split()[-1].lower()  # 'a', 'b', 'c', or 'd'
            elif line.strip() and not any(line.strip().endswith(f"{chr(97 + i)}.") for i in range(4)):
                options.append(line.strip())
        if current_question and options:
            questions.append((current_question, options, correct_answer))
    return questions

# Load the questions and answers
questions = read_pdf("ows.pdf")

# Shuffle the questions to ensure randomness
random.shuffle(questions)

# Function to display a question
def display_question(index):
    question, options, correct_answer = questions[index]
    st.write(f"**Question {index + 1}:** {question}")
    selected_option = st.radio("Select an option", options, key=f"option{index}")
    return correct_answer, selected_option

# Function to check the answer
def check_answer(correct_answer, selected_option):
    if selected_option and correct_answer and selected_option[0].lower() == correct_answer:
        return "Correct!"
    else:
        return f"Wrong! The correct answer is {correct_answer.upper()}."

# Initialize session state using st.session_state.get
if "index" not in st.session_state:
    st.session_state.index = 0

index = st.session_state.index

# Main app
st.title("One Word Substitution Practice")

correct_answer, selected_option = display_question(index)

if st.button("Submit"):
    feedback = check_answer(correct_answer, selected_option)
    st.write(feedback)
    if index < len(questions) - 1:
        st.session_state.index += 1
else:
    st.write("Select an answer and submit to get feedback.")
