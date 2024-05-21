import streamlit as st
import pandas as pd

# Load the CSV file
questions_df = pd.read_csv('owsqa.csv')

# Initialize session state variables
if 'index' not in st.session_state:
    st.session_state.index = 0
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'answer' not in st.session_state:
    st.session_state.answer = ""

# Function to load the next question
def next_question():
    if st.session_state.index < len(questions_df) - 1:
        st.session_state.index += 1
        st.session_state.answer = ""

# Function to check the answer
def check_answer():
    correct_answer = questions_df.iloc[st.session_state.index]['Correct Answer'].strip().lower()
    selected_option = st.session_state.answer.split(".")[0].strip().lower()  # Extract the letter and convert to lowercase
    if selected_option == correct_answer:
        st.session_state.score += 1
        st.success("Correct!")
    else:
        st.error("Incorrect. The correct answer is " + correct_answer.upper() + ".")
    next_question()

# Display the current question
current_question = questions_df.iloc[st.session_state.index]
st.write(f"Question {st.session_state.index + 1}: {current_question['Question']}")

# Display radio options
options = [
    current_question['Option A'],
    current_question['Option B'],
    current_question['Option C'],
    current_question['Option D']
]
st.radio("Options", options, key='answer')

if st.button("Submit"):
    check_answer()

st.write(f"Score: {st.session_state.score}")

if st.session_state.index >= len(questions_df):
    st.write("You've completed the quiz!")
else:
    st.write("Next question will appear after submitting the current one.")
